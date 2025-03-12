from flask import Flask, render_template, request
import openai
import os
import pdfplumber

app = Flask(__name__)

# Set OpenAI API Key from Render Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

# Function to analyze resume with OpenAI
def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an AI resume analyst. Compare the resume against the job description and provide a detailed analysis.

    Resume: {resume_text}

    Job Description: {job_description}

    Output:
    1. Key Skills Match (list):
    2. Education Match (degree and specialization):
    3. Work Experience Match (years and relevance):
    4. Overall Match Percentage (0-100):
    5. Suggestions for Improvement:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error during analysis: {str(e)}"

# Flask route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("resume")
        job_description = request.form.get("job_description")

        if not file or not job_description:
            return "Please upload a resume and provide a job description.", 400

        # Handle PDF or Text file
        if file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file)
        else:
            resume_text = file.read().decode("utf-8", errors="ignore")

        # Analyze the resume
        analysis = analyze_resume(resume_text, job_description)

        return render_template("results.html", analysis=analysis)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
