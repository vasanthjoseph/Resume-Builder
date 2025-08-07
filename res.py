import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from fpdf import FPDF

# Load GPT-2 Model and Tokenizer
model_name = "gpt2"  # GPT-2 small model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to generate text using GPT-2
def generate_resume_content(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, top_p=0.9, temperature=0.7)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Streamlit UI
st.title("AI Resume Generator")
st.write("Generate a professional resume using GPT-2")

# Input fields for user data
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
address = st.text_area("Address")
education = st.text_area("Education (e.g., Degree, University, Year)")
skills = st.text_area("Skills (e.g., Python, JavaScript, Data Science, etc.)")
work_experience = st.text_area("Work Experience (e.g., Job Title, Company, Duration)")

# Generate Resume Button
if st.button("Generate Resume"):
    # Create prompt for GPT-2 to generate a professional summary
    prompt = f"Create a professional resume for {name}, a skilled individual with expertise in {skills}. They have completed {education} and have worked at {work_experience}. Generate a professional summary."
    
    # Get GPT-2 generated resume content
    resume_content = generate_resume_content(prompt)
    
    # Display the generated resume content
    st.subheader("Generated Resume")
    st.write(resume_content)

    # Option to download the resume as PDF
    if st.button("Download Resume as PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Resume", ln=True, align='C')

        # Add Name
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)

        # Add Contact Info
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
        pdf.cell(200, 10, txt=f"Address: {address}", ln=True)

        # Add Education
        pdf.cell(200, 10, txt=f"Education: {education}", ln=True)

        # Add Skills
        pdf.cell(200, 10, txt=f"Skills: {skills}", ln=True)

        # Add Work Experience
        pdf.cell(200, 10, txt=f"Work Experience: {work_experience}", ln=True)

        # Add Resume Content from GPT-2
        pdf.multi_cell(0, 10, txt=f"Professional Summary: \n{resume_content}")

        # Save PDF
        pdf_output_path = "generated_resume.pdf"
        pdf.output(pdf_output_path)

        # Provide download link
        st.download_button(
            label="Download PDF",
            data=open(pdf_output_path, "rb").read(),
            file_name=pdf_output_path,
            mime="application/pdf"
        )

