import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = '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'
# Function to generate resume using ChatGPT
def generate_resume(name, email, phone, summary, skills, experience, education):
    prompt = f"""
    Generate a professional resume based on the following details:
    Name: {name}
    Email: {email}
    Phone: {phone}
    Professional Summary: {summary}
    Skills: {skills}
    Work Experience: {experience}
    Education: {education}
    The resume should be in a clean, professional format.
    """

    # Call OpenAI API to generate resume content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    resume_content = response['choices'][0]['message']['content']
    return resume_content

# Streamlit App to interact with the user
def main():
    st.title("AI-Based Resume Builder")

    # User inputs
    name = st.text_input("Enter your Name:")
    email = st.text_input("Enter your Email:")
    phone = st.text_input("Enter your Phone Number:")
    summary = st.text_area("Enter your Professional Summary:")
    skills = st.text_area("Enter your Skills (comma separated):")
    experience = st.text_area("Enter your Work Experience (separate each job with a new line):")
    education = st.text_area("Enter your Education (separate each entry with a new line):")

    # Button to generate resume
    if st.button("Generate Resume"):
        if name and email and phone and summary and skills and experience and education:
            # Generate the resume using the details provided
            resume_content = generate_resume(name, email, phone, summary, skills, experience, education)
            st.subheader("Generated Resume:")
            st.text(resume_content) # Display the generated resume content
        else:
            st.warning("Please fill all the fields.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
