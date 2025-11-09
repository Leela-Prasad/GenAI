from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from tools import CustomerInfoTool

@CrewBase
class FinAdvisor:
    
    @agent
    def fin_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["fin_advisor"],
            # tools at agent level, so it can be used in both financial_analysis and investment_recommendation task
            tools=[CustomerInfoTool()], 
            verbose=True
        )
        
    @task
    def financial_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["financial_analysis"],
            output_file="analysis_task2.md"
        )
        
    @task
    def investment_recommendation(self) -> Task:
        return Task(
            config=self.tasks_config["investment_recommendation"],
            tools=[SerperDevTool()],
            output_file="investment_task2.md"
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )