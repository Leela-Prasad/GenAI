from crewai import Agent, Task, Process, Crew
from crewai.project import crew, agent, task, CrewBase, before_kickoff

@CrewBase
class WealthManagementCrew:
    
    # @before_kickoff
    # def prepare_inputs(self, inputs):
    #     return inputs
    
    @agent
    def tax_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["tax_advisor"]
        )
        
    @agent
    def wealth_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["wealth_manager"]
        )
        
    @task
    def tax_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["tax_planning_task"]
        )
        
    @task
    def create_wealth_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_wealth_plan_task"]
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )