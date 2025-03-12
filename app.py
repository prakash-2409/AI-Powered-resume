from flask import Flask, render_template, request
import openai
import os
import pdfplumber
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Resume analysis function
def analyze_resume(resume_text, job_description):
    prompt = f"""
    Analyze the following resume and match it against the job description. Extract key skills, education, experience, and give a match percentage.
    Resume: {resume_text}
    Job Description: {job_description}

    Output the result as:
    1. Skills Match:
    2. Education Match:
    3. Experience Match:
    4. Match Score (0-100):
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files['resume']
        job_description = request.form['job_description']

        # Extract text based on file type
        if resume_file.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            try:
                resume_text = resume_file.read().decode('utf-8')
            except UnicodeDecodeError:
                return "Error: Unsupported file encoding. Please upload a valid PDF or UTF-8 text file."

        # Analyze the resume
        analysis = analyze_resume(resume_text, job_description)
        return render_template('results.html', analysis=analysis)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
