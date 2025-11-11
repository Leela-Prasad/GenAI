from crewai import Crew, Agent, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.llm import LLM

@CrewBase
class WealthManagementCrew:
    
    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_analyst"],
            verbose=True
        )
    
    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["investment_advisor"],
            verbose=True
        )
        
    @agent
    def tax_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["tax_advisor"],
            verbose=True
        )
        
    @agent
    def wealth_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["wealth_manager"],
            verbose=True
        )
        
    @task
    def analyze_finances_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_finances_task"]
        )
        
    @task
    def investment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["investment_analysis_task"],
            context=[self.analyze_finances_task()]
        )
        
    @task
    def tax_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["tax_planning_task"],
            context=[self.analyze_finances_task()]
        )
        
    @task
    def create_wealth_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_wealth_plan_task"],            
            context=[self.analyze_finances_task(), self.investment_analysis_task(), 
                     self.tax_planning_task()]
        )
    
    @crew    
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=LLM(model="gpt-4o-mini"),
            verbose=True
        )