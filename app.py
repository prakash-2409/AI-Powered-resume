from flask import Flask, render_template, request
import fitz  # PyMuPDF for PDF text extraction
import re

app = Flask(__name__)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_document = fitz.open(pdf_file)
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

# Basic Resume Analyzer (Skill & Experience Extraction)
def analyze_resume(resume_text, job_description):
    skills = ["Python", "Java", "Machine Learning", "AI", "Data Science", "SQL", "Flask"]
    found_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
    
    experience_years = re.findall(r"(\d+)\s*(years|year|yrs|yr)\s*(experience)?", resume_text.lower())
    total_experience = sum(int(year[0]) for year in experience_years) if experience_years else 0
    
    return {
        "skills_matched": found_skills,
        "total_experience": total_experience,
        "job_description": job_description
    }

# Flask Route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return "No file uploaded."
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if resume_file.filename == '':
            return "Empty file uploaded."
        
        resume_text = extract_text_from_pdf(resume_file)
        analysis = analyze_resume(resume_text, job_description)
        
        return render_template('results.html', analysis=analysis)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
