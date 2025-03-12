from flask import Flask, render_template, request
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Set your DeepSeek API key and base URL
openai.api_key = os.getenv("DEEPSEEK_API_KEY")
openai.api_base = "https://api.deepseek.com"

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
        model="deepseek-chat",  # Use DeepSeek's chat model
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume'].read().decode('utf-8')
        job_description = request.form['job_description']
        analysis = analyze_resume(resume, job_description)
        return render_template('results.html', analysis=analysis)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
