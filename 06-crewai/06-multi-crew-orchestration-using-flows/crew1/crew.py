from crewai import Crew, Agent, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff

@CrewBase
class InvestmentAnalysisCrew:
    
    # @before_kickoff
    # def prepare_inputs(self, inputs):
    #     return inputs
    
    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_analyst"]        
        )
        
    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["investment_advisor"]
        )
        
    @task
    def analyze_finances_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_finances_task"]
        )
        
    @task
    def investment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["investment_analysis_task"]
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )