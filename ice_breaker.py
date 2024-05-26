from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
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

    linkedin_info = scrape_linkedin_profile(
        'https://www.linkedin.com/in/aaron-ogenrwot-240ba716b/',
        True
    )

    res = chain.invoke(input={"information": linkedin_info})

    print(res)
