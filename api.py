import os
import uuid
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from main import create_crew
import asyncio
import json

app = FastAPI(title="Job Application Crew System")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Temporary directory
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/loading", response_class=HTMLResponse)
async def loading(request: Request):
    return templates.TemplateResponse("loading.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    try:
        # Read the generated files
        resume_content = ""
        interview_content = ""
        resume_size = 0
        interview_size = 0
        
        # Read resume file
        if os.path.exists("tailored_resume.md"):
            with open("tailored_resume.md", "r", encoding="utf-8") as f:
                resume_content = f.read()
                resume_size = len(resume_content.encode('utf-8')) // 1024
        
        # Read interview materials file
        if os.path.exists("interview_materials.md"):
            with open("interview_materials.md", "r", encoding="utf-8") as f:
                interview_content = f.read()
                interview_size = len(interview_content.encode('utf-8')) // 1024
        
        return templates.TemplateResponse("results.html", {
            "request": request,
            "resume_content": resume_content,
            "interview_content": interview_content,
            "resume_size": resume_size,
            "interview_size": interview_size
        })
    except Exception as e:
        # Fallback to empty results if files don't exist
        return templates.TemplateResponse("results.html", {
            "request": request,
            "resume_content": "No resume generated yet.",
            "interview_content": "No interview materials generated yet.",
            "resume_size": 0,
            "interview_size": 0
        })

@app.post("/api/analyze")
async def analyze_job_application(
    job_url: str = Form(...),
    github_url: str = Form(...),
    linkedin_url: str = Form(...),
    resume_type: str = Form(...),
    resume_file: UploadFile = File(None),
    resume_content: str = Form(None),
    linkedin_type: str = Form(...),
    linkedin_file: UploadFile = File(None),
    linkedin_content: str = Form(None)
):
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Handle Resume
        resume_path = None
        if resume_type == "file" and resume_file:
            resume_path = os.path.join(TEMP_DIR, f"resume_{session_id}.md")
            with open(resume_path, "wb") as f:
                f.write(resume_file.file.read())
        elif resume_type == "text" and resume_content:
            resume_path = os.path.join(TEMP_DIR, f"resume_{session_id}.md")
            with open(resume_path, "w", encoding="utf-8") as f:
                f.write(resume_content)
        else:
            # Use default resume if no input provided
            resume_path = "fake_resume.md"
        
        # Handle LinkedIn
        linkedin_path = None
        if linkedin_type == "file" and linkedin_file:
            linkedin_path = os.path.join(TEMP_DIR, f"linkedin_{session_id}.txt")
            with open(linkedin_path, "wb") as f:
                f.write(linkedin_file.file.read())
        elif linkedin_type == "text" and linkedin_content:
            linkedin_path = os.path.join(TEMP_DIR, f"linkedin_{session_id}.txt")
            with open(linkedin_path, "w", encoding="utf-8") as f:
                f.write(linkedin_content)
        else:
            # Use default LinkedIn if no input provided
            linkedin_path = "linkedin_backup.txt"
        
        # Create new crew
        job_application_crew = create_crew()
        
        # Update inputs for CrewAI
        inputs = {
            'job_posting_url': job_url,
            'github_url': github_url,
            'linkedin_url': linkedin_url
        }
        
        # Run CrewAI analysis
        print("🚀 Starting the job-application crew...")
        result = job_application_crew.kickoff(inputs=inputs)
        
        # Clean up temporary files
        if resume_path and resume_path != "fake_resume.md":
            try:
                os.remove(resume_path)
            except:
                pass
        if linkedin_path and linkedin_path != "linkedin_backup.txt":
            try:
                os.remove(linkedin_path)
            except:
                pass
        
        return {"status": "success", "result": str(result), "redirect": "/results"}
        
    except Exception as e:
        # Clean up on error
        if 'resume_path' in locals() and resume_path and resume_path != "fake_resume.md":
            try:
                os.remove(resume_path)
            except:
                pass
        if 'linkedin_path' in locals() and linkedin_path and linkedin_path != "linkedin_backup.txt":
            try:
                os.remove(linkedin_path)
            except:
                pass
        
        print(f"Error in API: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    allowed_files = ["tailored_resume.md", "interview_materials.md"]
    
    if filename not in allowed_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = f"./{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type="text/markdown")
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
