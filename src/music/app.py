import streamlit as st
import asyncio
import sys
import os
import nest_asyncio

# Adjust sys.path to include the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Apply nest_asyncio to allow re-entrant event loops
nest_asyncio.apply()

# Now import from music.main (absolute import)
from music.main import kickoff, UserProfile

st.set_page_config(page_title="Learning Plan Generator", layout="wide")

def main():
    st.title("🎹 AI Piano Teacher - Learning Plan Generator")

    with st.form(key="user_profile_form"):
        st.subheader("Tell us about yourself")

        current_level = st.selectbox("What is your current skill level?", 
                                    ["Beginner", "Intermediate", "Advanced"])
        reading_sheet_music = st.selectbox("How well can you read sheet music?", 
                                        ["Beginner", "Intermediate", "Advanced"])
        frequency_of_practice = st.selectbox("How often do you practice?", 
                                            ["Rarely", "A few times a week", "Daily"])
        time_commitment = st.selectbox("How much time can you dedicate per session?", 
                                    ["<30 min", "30-60 min", "1-2 hours", "More than 2 hours"])
        goals = st.text_area("What is your main goal?", "")

        submit = st.form_submit_button("Generate Learning Plan")

    if submit:
        st.success("Generating your learning plan... Please wait.")

        user_profile = UserProfile(
            current_level=current_level,
            reading_sheet_music=reading_sheet_music,
            frequency_of_practice=frequency_of_practice,
            time_commitment=time_commitment,
            goals=goals
        )
        
        # Use the existing event loop to run the async function
        loop = asyncio.get_event_loop()
        learning_plan = loop.run_until_complete(kickoff(user_profile))

        # Display the learning plan in markdown format
        st.markdown("## Learning Plan")
        for module in learning_plan:
            st.markdown(f"### Month {module.month}, Week {module.week}")
            st.markdown(f"**Title:** {module.title}")
            st.markdown(f"**Content:** {module.content}")
            st.markdown("---")

if __name__ == "__main__":
    main()