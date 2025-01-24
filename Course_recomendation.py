import streamlit as st
import google.generativeai as genai

st.title("Course Recommendation System Using AI")

# Directly setting the Gemini API Key
GOOGLE_API_KEY = "AIzaSyBWyvKUaTQLGhaiwYuNexY_6VvuulW6fhw"
genai.configure(api_key=GOOGLE_API_KEY)

# Define the function to call the Gemini API
def generate_text_with_gemini(prompt, model="gemini-1.5-flash"):
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel(model)
        
        # Use the model to generate content with the given prompt
        response = model.generate_content(prompt)
        
        # Return the generated text
        return response.text
    except Exception as e:
        st.error(f"Error in generating text: {e}")
        return ""

# Input fields for course recommendation
col1, col2 = st.columns(2)
with col1:
    core_subject = st.text_input("What is your core subject? (e.g., Data Science, AI, Web Development)")
    current_role = st.text_input("What is your current role? (e.g., Data Engineer, Software Developer)")
    career_goal = st.text_input("What career goal are you aiming for? (e.g., Machine Learning Engineer, Web Developer)")
    
with col2:
    desired_skills = st.text_area(
        "What specific skills do you want to develop? (e.g., Cloud Computing, Data Visualization)",
        placeholder="List the skills you want to learn..."
    )

# Ensure current_skillset is stored in session_state
if "current_skillset" not in st.session_state:
    st.session_state.current_skillset = []

st.subheader("Current Skillset and Levels")

# Input fields for adding a new skill
skill = st.text_input("Enter a skill (e.g., Python):")
skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])

if st.button("Add Skill"):
    if skill and skill_level:
        # Append to the session_state list
        st.session_state.current_skillset.append((skill, skill_level))
    else:
        st.warning("Please provide both a skill and its level.")

# Display the current skillset from session_state
if st.session_state.current_skillset:
    st.subheader("Your Current Skillset")
    for s, level in st.session_state.current_skillset:
        st.text(f"- {s}: {level}")

# Generate a string representation of the skillset for use in the prompt
skillset_str = ", ".join([f"{s} ({level})" for s, level in st.session_state.current_skillset])

# User's data summary
user_data = f"""
- Core Subject: {core_subject}
- Current Role: {current_role}
- Career Goal: {career_goal}
- Current Skillset: {skillset_str if skillset_str else 'None provided'}
- Desired Skills: {desired_skills}
"""

# For debugging
print("check1:", skillset_str)

# Prompt for course recommendation generation
prompt = f"""
Given the following user data:

{user_data}

Based on this information, suggest a detailed course recommendation in the following format:

# Course Recommendation

## Understanding Your Situation:
- **Core Subject**: {core_subject}
- **Current Role**: {current_role}
- **Career Goal**: {career_goal}
- **Current Skillset**: {skillset_str if skillset_str else 'None provided'}
- **Desired Skills**: {desired_skills}

## Suggested Courses:
1. **Course Name**: Name of the course  /n
   **Platform**: Platform where the course is available /n 
   **Details**: What the course teaches and why it is relevant.  /n
   **Why This Course?**: How this course aligns with the user's goals and desired skills.
   **Course link**: Provide one Specific valid links for each course (get it from google search engine)
   
   
2. (Additional recommendations based on their goals and skillset...)

## Additional Considerations:
- Highlight courses or certifications in areas where the user's skills are already strong but can be further advanced.
- Recommend foundational courses for skills the user wants to develop.

## Disclaimer:
- Recommendations are based on your input. Consult with a career advisor or mentor to tailor the plan further.
"""

if st.button("Generate Course Recommendations"):
    with st.spinner("Generating Recommendations..."):
        # Call the Gemini API to generate the course recommendations
        generated_recommendations = generate_text_with_gemini(prompt, model="gemini-1.5-flash")
        
        # Display the recommendations
        st.subheader("Course Recommendations")
        st.markdown(generated_recommendations)
