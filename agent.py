import os
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = # Replace with your key

# Custom Tools
class JobPortalTool(BaseTool):
    name: str = "JobPortalTool"
    description: str = "Fetches job listings based on role and location."

    def _run(self, role: str, location: str) -> str:
        return f"Simulated job listings for {role} in {location}"

class TrainingPlatformTool(BaseTool):
    name: str = "TrainingPlatformTool"
    description: str = "Fetches training courses based on a skill."

    def _run(self, skill: str) -> str:
        return f"Simulated courses for {skill}"

# Define Agents
career_guidance_agent = Agent(
    role="Career Guidance Agent",
    goal="Guide users in India to enhance skills and find jobs by collecting input and coordinating tasks.",
    backstory="You are an AI career advisor for the Indian job market.",
    verbose=True,
    allow_delegation=True
)

skill_assessment_agent = Agent(
    role="Skill Assessment Agent",
    goal="Assess the user's current skills based on their input.",
    backstory="You are an expert in evaluating skills for Indian job seekers.",
    verbose=True,
    allow_delegation=False
)

demand_analysis_agent = Agent(
    role="Demand Analysis Agent",
    goal="Identify in-demand skills in the Indian job market.",
    tools=[JobPortalTool()],
    backstory="You analyze job trends in India.",
    verbose=True,
    allow_delegation=False
)

training_resource_agent = Agent(
    role="Training Resource Agent",
    goal="Recommend training resources for skill gaps.",
    tools=[TrainingPlatformTool()],
    backstory="You specialize in Indian training programs.",
    verbose=True,
    allow_delegation=False
)

job_matching_agent = Agent(
    role="Job Matching Agent",
    goal="Match users with job openings in India based on skills and preferences.",
    tools=[JobPortalTool()],
    backstory="You connect Indian job seekers with opportunities.",
    verbose=True,
    allow_delegation=False
)

# Define Tasks with Explicit Inputs
def get_user_input():
    role = input("Enter your desired role (e.g., Software Engineer): ")
    location = input("Enter your preferred location (e.g., Bangalore): ")
    experience = input("Enter your years of experience and skills (e.g., 5 years, Python, Java): ")
    return f"User wants to be a {role} in {location} with {experience}."

user_input_task = Task(
    description=get_user_input(),
    agent=career_guidance_agent,
    expected_output="A summary of user input: career goals, location, and experience."
)

skill_assessment_task = Task(
    description="Assess the user's skills based on their input: {user_input_task.output}.",
    agent=skill_assessment_agent,
    expected_output="A list of the user's current skills."
)

demand_analysis_task = Task(
    description="Analyze the Indian job market for in-demand skills for the user's role and location from {user_input_task.output}.",
    agent=demand_analysis_agent,
    expected_output="A list of in-demand skills."
)

training_recommendation_task = Task(
    description="Recommend training resources to bridge skill gaps between {skill_assessment_task.output} and {demand_analysis_task.output}.",
    agent=training_resource_agent,
    expected_output="A list of recommended training courses."
)

job_matching_task = Task(
    description="Match the user with job openings in India based on {skill_assessment_task.output} and {user_input_task.output}.",
    agent=job_matching_agent,
    expected_output="A list of relevant job openings."
)

# Create and Run the Crew
crew = Crew(
    agents=[
        career_guidance_agent,
        skill_assessment_agent,
        demand_analysis_agent,
        training_resource_agent,
        job_matching_agent
    ],
    tasks=[
        user_input_task,
        skill_assessment_task,
        demand_analysis_task,
        training_recommendation_task,
        job_matching_task
    ],
    verbose=True  # Boolean value as required
)

# Execute the Workflow
if __name__ == "__main__":
    print("Starting the AI-Driven Skill Enhancement and Job Connect Agent for India...")
    result = crew.kickoff()
    print("\nFinal Result:")
    print(result)