import asyncio
from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from src.music.crews.create_learning_module_crew.learning_module_crew import WriteLearningModuleCrew
from src.music.types import Module, ModuleOutline, UserProfile
from src.music.crews.learning_plan_crew.learning_crew import LearningPlanOutlineCrew


class LearningPlanState(BaseModel):
    userprofile: List[UserProfile] = []
    learning_plan: List[Module] = []
    learning_plan_outline: List[ModuleOutline] = []
    goal: str = """
        The goal of this modular learning planner is to provide effective and interactive lessons with 
        musical theories, examples, and practice guidelines that will help the student to learn piano and become a great pianist.
    """


class LearningPlanFlow(Flow[LearningPlanState]):
    def __init__(self, state: LearningPlanState):
        super().__init__(state=state)

    @start()
    async def generate_learning_plan_outline(self):
        output = (
            LearningPlanOutlineCrew()
            .crew()
            .kickoff(inputs={"userprofile": self.state.userprofile, "goal": self.state.goal})
        )
        self.state.learning_plan_outline = output["modules"]

    @listen(generate_learning_plan_outline)
    async def write_modules(self):
        tasks = []

        async def write_single_module(module_outline):
            output = (
                WriteLearningModuleCrew()
                .crew()
                .kickoff(
                    inputs={
                        "userprofile": self.state.userprofile,
                        "goal": self.state.goal,
                        "module_week": module_outline.week,
                        "module_title": module_outline.title,
                        "module_description": module_outline.description,
                        "learning_plan_outline": [
                            module_outline.model_dump_json()
                            for module_outline in self.state.learning_plan_outline
                        ],
                    }
                )
            )
            return Module(
                month=output["month"],
                week=output["week"],
                title=output["title"],
                content=output["content"]
            )

        tasks = [asyncio.create_task(write_single_module(module)) for module in self.state.learning_plan_outline]
        self.state.learning_plan = await asyncio.gather(*tasks)

    @listen(write_modules)
    async def return_learning_plan(self):
        return self.state.learning_plan

    async def kickoff(self):
        await self.generate_learning_plan_outline()
        await self.write_modules()
        return self.state.learning_plan


async def kickoff(user_profile: UserProfile):
    state = LearningPlanState(userprofile=[user_profile])
    learning_plan_flow = LearningPlanFlow(state=state)
    learning_plan = await learning_plan_flow.kickoff()
    return learning_plan