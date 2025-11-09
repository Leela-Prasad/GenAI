from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from tools import CustomerInfoTool

@CrewBase
class FinAdvisor:
    
    @agent
    def financial_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_advisor"],
            verbose=True
        )
        
    @agent
    def retirement_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["retirement_advisor"],
            verbose=True
        )
        
    @agent
    def strategy_aggregator(self) -> Agent:
        return Agent(
            config=self.agents_config["strategy_aggregator"],
            verbose=True
        )
        
    @agent
    def tax_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["tax_advisor"],
            verbose=True
        )
        
    @task
    def financial_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["financial_analysis_task"],
            tools= [CustomerInfoTool()]
        )
        
    @task
    def investment_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["investment_planning_task"],
            tools=[SerperDevTool()],
            context=[self.financial_analysis_task()]
        )
        
    @task
    def tax_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["tax_planning_task"],
            tools=[SerperDevTool()],
            context=[self.financial_analysis_task(), self.investment_planning_task()],
            async_execution=True
        )
        
    @task
    def retirement_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["retirement_planning_task"],
            tools=[SerperDevTool()],
            context=[self.financial_analysis_task(), self.investment_planning_task()],
            async_execution=True
        )
        
    @task
    def strategy_aggregation_task(self) -> Task:
        return Task(
            config=self.tasks_config["strategy_aggregation_task"],
            context=[self.financial_analysis_task(), self.investment_planning_task(),
                     self.tax_planning_task(), self.retirement_planning_task()]
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )