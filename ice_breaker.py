from typing import Tuple
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup
from output_parser import Summary, summary_parser

def ice_break_with(name:str)->Tuple[Summary,str]:
    summary_template = """
    given the information about a person from linkedin {information} I want you to create:
    1. A short summary
    2. Two interesting facts about them
    \n{format_instruction}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        partial_variables={"format_instruction":summary_parser.get_format_instructions()},
        template=summary_template
    )

    linkedin_profile_url = lookup(name=name)
    linkedin_info = scrape_linkedin_profile(
        linkedin_profile_url,True
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_info})

    return res,linkedin_info.get("profile_pic_url")

if __name__ == "__main__":
    ice_break_with("Aaron Ogenrwot")
