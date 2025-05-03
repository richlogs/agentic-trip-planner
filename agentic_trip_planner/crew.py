from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

llm = LLM(model='ollama/quen3:4b', base_url='http://localhost:11434')


@CrewBase
class ResearchCrew:
    """A crew for conducting research,
    summarizing findings, and fact-checking
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.search_tool = SerperDevTool()
        self.llm = LLM(model='ollama/quen3:4b', base_url='http://localhost:11434')

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trip_advisor'], tools=[self.search_tool]
        )  # type: ignore

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'], tools=[self.search_tool]
        )  # type: ignore

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'], tools=[self.search_tool])  # type: ignore

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )
