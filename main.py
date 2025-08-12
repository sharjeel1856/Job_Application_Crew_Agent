# main.py
import os
import warnings
from crewai import Agent, Task, Crew
from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    MDXSearchTool,
    SerperDevTool
)
from utils import get_openai_api_key, get_serper_api_key

warnings.filterwarnings('ignore')

# -----------------------
# 1) Set API keys + model
# -----------------------
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
os.environ["SERPER_API_KEY"] = get_serper_api_key()

# -----------------------
# 2) Tools (will be updated dynamically)
# -----------------------
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Default file paths (will be overridden by API)
default_resume_path = './fake_resume.md'
default_linkedin_path = './linkedin_backup.txt'

# Initialize tools with default paths
read_resume = FileReadTool(file_path=default_resume_path)
semantic_search_resume = MDXSearchTool(mdx=default_resume_path)
read_linkedin_backup = FileReadTool(file_path=default_linkedin_path)

# Function to update tools with new file paths
def update_tools(resume_path=None, linkedin_path=None):
    global read_resume, semantic_search_resume, read_linkedin_backup
    
    if resume_path:
        read_resume = FileReadTool(file_path=resume_path)
        semantic_search_resume = MDXSearchTool(mdx=resume_path)
    
    if linkedin_path:
        read_linkedin_backup = FileReadTool(file_path=linkedin_path)

# -----------------------
# 3) Agents (backstory added)
# -----------------------
def create_agents():
    researcher = Agent(
        role="Tech Job Researcher",
        goal="Analyze job postings for required skills and qualifications",
        backstory="A seasoned researcher specializing in the tech job market, skilled at identifying required skills, experience, and qualifications from job postings.",
        tools=[scrape_tool, search_tool],
        verbose=True
    )

    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Research GitHub, LinkedIn, and resume to build a detailed profile",
        backstory="An expert profiler who analyzes online professional presence to create a complete and accurate profile of the candidate.",
        tools=[scrape_tool, search_tool, read_resume, semantic_search_resume, read_linkedin_backup],
        verbose=True
    )

    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Tailor resume to match job requirements using available profile data",
        backstory="A resume expert who crafts targeted resumes that align perfectly with job descriptions while maintaining accuracy.",
        tools=[scrape_tool, search_tool, read_resume, semantic_search_resume, read_linkedin_backup],
        verbose=True
    )

    interview_preparer = Agent(
        role="Engineering Interview Preparer",
        goal="Create interview questions and talking points based on tailored resume and job",
        backstory="An experienced interview coach who prepares candidates with realistic questions, STAR responses, and talking points.",
        tools=[scrape_tool, search_tool, read_resume, semantic_search_resume, read_linkedin_backup],
        verbose=True
    )
    
    return researcher, profiler, resume_strategist, interview_preparer

# -----------------------
# 4) Tasks
# -----------------------
def create_tasks(researcher, profiler, resume_strategist, interview_preparer):
    research_task = Task(
        description=(
            "Analyze the job posting URL ({job_posting_url}) and extract key skills, "
            "qualifications, responsibilities, and nice-to-have items."
        ),
        expected_output="Structured list of job requirements (skills, years, responsibilities).",
        agent=researcher,
        async_execution=True
    )

    profile_task = Task(
        description=(
            "Compile a comprehensive candidate profile using:\n"
            "- GitHub ({github_url})\n"
            "- LinkedIn ({linkedin_url}) — attempt to scrape LinkedIn first; if scraping fails, "
            "use the content of linkedin_backup.txt (local backup).\n"
            "- resume (fake_resume.md) and personal_writeup.\n\n"
            "Return a clear profile: summary, skills, projects, roles, education, certificates."
        ),
        expected_output="Candidate profile document.",
        agent=profiler,
        async_execution=True
    )

    resume_strategy_task = Task(
        description=(
            "Using outputs from the research_task (job requirements) and profile_task (candidate profile), "
            "tailor fake_resume.md to produce a targeted resume. Update summary, skills, experience bullets. "
            "Do NOT invent facts — prefer 'based on profile' statements."
        ),
        expected_output="A tailored resume file.",
        output_file="tailored_resume.md",
        context=[research_task, profile_task],
        agent=resume_strategist
    )

    interview_preparation_task = Task(
        description=(
            "Create interview questions, STAR examples, and talking points based on tailored resume "
            "and job requirements. Focus on the top 8-12 likely interview prompts and suggested responses."
        ),
        expected_output="Interview materials document.",
        output_file="interview_materials.md",
        context=[research_task, profile_task, resume_strategy_task],
        agent=interview_preparer
    )
    
    return research_task, profile_task, resume_strategy_task, interview_preparation_task

# -----------------------
# 5) Crew
# -----------------------
def create_crew():
    researcher, profiler, resume_strategist, interview_preparer = create_agents()
    research_task, profile_task, resume_strategy_task, interview_preparation_task = create_tasks(
        researcher, profiler, resume_strategist, interview_preparer
    )
    
    job_application_crew = Crew(
        agents=[researcher, profiler, resume_strategist, interview_preparer],
        tasks=[research_task, profile_task, resume_strategy_task, interview_preparation_task],
        verbose=True
    )
    
    return job_application_crew

# Create the crew instance
job_application_crew = create_crew()

# -----------------------
# 6) Inputs (for backward compatibility)
# -----------------------
job_application_inputs = {
    'job_posting_url': 'https://www.linkedin.com/posts/codeminer_flutterdeveloper-hiringnow-joinourteam-activity-7359913599596716032-PU4h',
    'github_url': 'https://github.com/sharjeel1856',
    'linkedin_url': 'https://www.linkedin.com/in/muhammad-sharjeel-59a255203/',
    'personal_writeup': """Short summary about the candidate here."""
}

# -----------------------
# 7) Run the crew (for backward compatibility)
# -----------------------
if __name__ == "__main__":
    print("🚀 Starting the job-application crew...")
    result = job_application_crew.kickoff(inputs=job_application_inputs)
    print("✅ Done. Look for 'tailored_resume.md' and 'interview_materials.md' in the folder.")
