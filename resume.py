import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

# Custom PDF Class
class PDF(FPDF):
    def header(self):
        # Profile Image
        if os.path.exists("profile.jpg"):
            self.image("profile.jpg", 10, 8, 25)
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, self.name, ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, f"{self.email} | {self.phone}", ln=True, align="C")
        self.cell(0, 10, f"{self.linkedin} | {self.github}", ln=True, align="C")
        self.ln(10)

    def add_section(self, title, body):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, ln=True)
        self.set_font("Helvetica", "", 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, body)
        self.ln(3)

    def add_project_list(self, projects):
        self.set_font("Helvetica", "", 12)
        for proj in projects:
            self.set_font("Helvetica", "B", 12)
            self.cell(0, 8, f"- {proj['title']}", ln=True)
            self.set_font("Helvetica", "", 11)
            self.multi_cell(0, 8, f"  {proj['description']}")
            self.ln(2)

# Streamlit Interface
st.title("📝 Resume Builder with Photo & Projects")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
linkedin = st.text_input("LinkedIn")
github = st.text_input("GitHub")
about = st.text_area("About You")

st.markdown("### Upload Your Profile Photo")
photo = st.file_uploader("Choose a JPG image", type=["jpg", "jpeg"])

# Projects
st.markdown("### Add Projects")
projects = []
for i in range(3):  # Allow up to 3 projects
    st.markdown(f"**Project {i+1}**")
    title = st.text_input(f"Project {i+1} Title", key=f"title_{i}")
    desc = st.text_area(f"Project {i+1} Description", key=f"desc_{i}")
    if title and desc:
        projects.append({"title": title, "description": desc})

if st.button("Generate Resume"):
    # Save uploaded image
    if photo:
        image = Image.open(photo)
        image.save("profile.jpg")

    pdf = PDF()
    pdf.name = name
    pdf.email = email
    pdf.phone = phone
    pdf.linkedin = linkedin
    pdf.github = github
    pdf.add_page()

    pdf.add_section("About Me", about)
    pdf.add_section("Projects", "")
    pdf.add_project_list(projects)

    filename = "generated_resume.pdf"
    pdf.output(filename)

    with open(filename, "rb") as f:
        st.success("✅ Resume Generated!")
        st.download_button("📄 Download Resume", f, file_name=filename)

