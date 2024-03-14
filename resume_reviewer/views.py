import openai
from django.shortcuts import render
from PyPDF2 import PdfReader

from core.settings import OPENAI_API_KEY

# OpenAI API client
openai.api_key = OPENAI_API_KEY


def home(request):
    """
    View for home page
    GET - returns home page
    POST - takes job description and resume through form and evaluates it.
    """
    if request.method == "GET":
        return render(request, "resume_reviewer/home.html")
    elif request.method == "POST":
        job_description = request.POST.get("job_description")
        resume = request.FILES.get("resume")
        if resume is not None and len(job_description) > 100:
            pdf_file = PdfReader(resume)
            pdf_text = ""
            for page in pdf_file.pages:
                pdf_text += page.extract_text() + "\n"
            resume_data = extract_resume_data(pdf_text, job_description)
            data = {}
            if resume_data:
                data["education"] = int(resume_data.get("education", 0))
                data["company_fit"] = int(resume_data.get("company_fit", 0))
                data["technical_skills"] = int(resume_data.get("technical_skills", 0))
                data["soft_skills"] = int(resume_data.get("soft_skills", 0))
                data["projects"] = int(resume_data.get("projects", 0))
                data["name"] = resume_data.get("name")
                data["relevant_skills"] = resume_data.get("relevant_skills")
                data["summary"] = resume_data.get("summary")
            return render(request, "resume_reviewer/output.html", {"resume_data": data})
        return render(request, "resume_reviewer/home.html")


def extract_resume_data(pdf_text, job_desc):
    gpt_response = get_gpt_response(pdf_text, job_desc)
    print(gpt_response)
    response_message = gpt_response["choices"][0]["message"]
    reviews = response_message.get("function_call")
    result = reviews.get("arguments")
    return result


def get_gpt_response(pdf_text, job_desc):

    prompt = f"""You are a professional HR recruiter and your job is to give ratings to a prospect based on the
            job description. Do not output anything else.
            The job description is as follows: {job_desc}
            The prospect's resume is as follows: {pdf_text}
            """

    function_descriptions = [
        {
            "name": "extract_resume_ratings",
            "description": "Extract information ratings from resume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Extract prospect name",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Write a 80 word summary of the resume",
                    },
                    "years_of_experience": {
                        "type": "number",
                        "description": "Extract prospect total years of experience",
                    },
                    "relevant_skills": {
                        "type": "string",
                        "description": "Extract list of relevant skills to the job",
                    },
                    "company_fit": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect is a fit for the position: [1, 2, ..., 9, 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                    "education": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's education matches with the position: [1, 2, ..., 9, 10] 1 being completely unrelated education and 10 being a perfect matched education for the job",
                    },
                    "technical_skills": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's technical skills area a fit for the position: [1, 2, ..., 9, 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                    "soft_skills": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's soft skills are a fit for the position: [1, 2,..., 9, 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                    "projects": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's projects are a fit for the position: [1, 2,..., 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                },
                "required": ["name", "years_of_experience"],
            },
        }
    ]

    messages = [{"role": "user", "content": prompt}]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=function_descriptions,
        function_call="auto",
    )

    return response
