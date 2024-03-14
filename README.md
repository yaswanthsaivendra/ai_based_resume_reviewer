# ai_based_resume_reviewer
ChatGPT to review resumes.


## Setup

Initial requirements : poetry, pip, python3 

1. Activate Environment
```
poetry shell
```
2. Install the requirements
```
poetry install --no-root
```
3. Inside core directory under the root of the project, create a .env file with the below contents
```
OPENAI_API_KEY=your_open_api_key
```

### Usage

1. To run server
```
python3 manage.py runserver
```

2. At http://127.0.0.1:8000/ (home), upload a job description(more than 100 chars) along with the resume, click on the submit button.

