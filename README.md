# ATS-checker
AI-powered ATS Resume Checker built with Streamlit and Google Gemini — analyze resumes, get match scores, and improve your job-fit instantly.
# 1. Clone this repository
git clone https://github.com/<your-username>/ats-resume-expert.git
cd ats-resume-expert

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Google API key
# Create a .env file in the root directory:
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 4. Run the app
streamlit run app.py
