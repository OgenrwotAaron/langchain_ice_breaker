from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup

def ice_break_with(name:str):
    summary_template = """
    Given the LinkedIn information {information} about a person, I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    linkedin_profile_url = lookup(name=name)
    linkedin_info = scrape_linkedin_profile(
        linkedin_profile_url, False
    )

    res = chain.invoke(input={"information": linkedin_info})

    return res

if __name__ == "__main__":
    print(ice_break_with("Aaron Ogenrwot"))
