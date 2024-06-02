from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor

from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    template = """
    Given the full name {name_of_person} I want you to get me their LinkedIn Public Profile Link
    following this format https://www.linkedin.com/in/[unique identifier].
    Your answer should contain only the URL link
  """

    promp_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn Profile URL",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the LinkedIn Profile URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": promp_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup("Aaron Ogenrwot")
    print(linkedin_url)
