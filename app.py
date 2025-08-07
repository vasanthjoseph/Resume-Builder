import streamlit as st
from fpdf import FPDF

# Function to generate PDF
def generate_pdf(name, email, phone, linkedin, github, summary, experience, education, skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add personal details
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=name, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Email: {email} | Phone: {phone}", ln=True, align='C')
    if linkedin:
        pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=True, align='C')
    if github:
        pdf.cell(200, 10, txt=f"GitHub: {github}", ln=True, align='C')
    pdf.ln(10)

    # Add summary
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Professional Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf.ln(5)

    # Add work experience
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Work Experience:", ln=True)
    pdf.set_font("Arial", size=12)
    for exp in experience:
        pdf.cell(0, 10, f"{exp['role']} at {exp['company']} ({exp['duration']})", ln=True)
        pdf.multi_cell(0, 10, f"Responsibilities: {exp['responsibilities']}")
        pdf.ln(3)

    # Add education
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Education:", ln=True)
    pdf.set_font("Arial", size=12)
    for edu in education:
        pdf.cell(0, 10, f"{edu['degree']} from {edu['institution']} ({edu['year']})", ln=True)
    pdf.ln(5)

    # Add skills
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Skills:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, ", ".join(skills))

    # Save PDF
    pdf_file = "resume.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Main function
def main():
    st.title("AI Resume Builder")
    st.write("Fill in the details below to generate your resume.")

    # Personal Information
    st.header("Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile URL")
    github = st.text_input("GitHub Profile URL (optional)")

    # Professional Summary
    st.header("Professional Summary")
    summary = st.text_area("Briefly describe yourself (2-3 sentences)")

    # Work Experience
    st.header("Work Experience")
    experience = []
    with st.expander("Add Work Experience"):
        num_jobs = st.number_input("How many jobs to add?", min_value=0, max_value=10, step=1)
        for i in range(num_jobs):
            st.subheader(f"Job {i + 1}")
            company = st.text_input(f"Company Name (Job {i + 1})", key=f"company_{i}")
            role = st.text_input(f"Role (Job {i + 1})", key=f"role_{i}")
            duration = st.text_input(f"Duration (e.g., Jan 2020 - Dec 2021)", key=f"duration_{i}")
            responsibilities = st.text_area(f"Responsibilities (Job {i + 1})", key=f"responsibilities_{i}")
            if company and role:
                experience.append({
                    "company": company,
                    "role": role,
                    "duration": duration,
                    "responsibilities": responsibilities
                })

    # Education
    st.header("Education")
    education = []
    with st.expander("Add Education"):
        num_edu = st.number_input("How many education entries to add?", min_value=0, max_value=10, step=1)
        for i in range(num_edu):
            st.subheader(f"Education {i + 1}")
            institution = st.text_input(f"Institution Name (Edu {i + 1})", key=f"institution_{i}")
            degree = st.text_input(f"Degree (e.g., B.Tech in Computer Science)", key=f"degree_{i}")
            year = st.text_input(f"Year of Graduation", key=f"year_{i}")
            if institution and degree:
                education.append({
                    "institution": institution,
                    "degree": degree,
                    "year": year
                })

    # Skills
    st.header("Skills")
    skills = st.text_area("Enter your skills (comma-separated)").split(',')

    # Generate Resume
    if st.button("Generate Resume"):
        st.subheader("Your Resume Preview")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email} | **Phone:** {phone}")
        st.write(f"**LinkedIn:** {linkedin}")
        if github:
            st.write(f"**GitHub:** {github}")
        st.write("\n### Professional Summary")
        st.write(summary)
        st.write("\n### Work Experience")
        for exp in experience:
            st.write(f"- **{exp['role']}** at {exp['company']} ({exp['duration']})")
            st.write(f"  - {exp['responsibilities']}")
        st.write("\n### Education")
        for edu in education:
            st.write(f"- **{edu['degree']}** from {edu['institution']} ({edu['year']})")
        st.write("\n### Skills")
        st.write(", ".join(skill.strip() for skill in skills))
        
        # Generate PDF
        pdf_file = generate_pdf(name, email, phone, linkedin, github, summary, experience, education, skills)
        st.success("Resume generated successfully!")
        with open(pdf_file, "rb") as f:
            st.download_button(label="Download Resume as PDF", data=f, file_name="resume.pdf", mime="application/pdf")

# Run the Streamlit app
if __name__ == "__main__":
    main()
