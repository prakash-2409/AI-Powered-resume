from flask import Flask, render_template, request
import openai
import os
import pdfplumber

app = Flask(__name__)

# Set OpenAI API Key from Render Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def analyze_resume(resume_text, job_description):
    prompt = f"""
    Analyze the following resume and match it against the job description.
    Extract key skills, education, experience, and give a match percentage.
    
    Resume: {resume_text}
    Job Description: {job_description}
    
    Output:
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        job_description = request.form["job_description"]

        if file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file)
        else:
            resume_text = file.read().decode("utf-8")

        analysis = analyze_resume(resume_text, job_description)
        return render_template("results.html", analysis=analysis)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
