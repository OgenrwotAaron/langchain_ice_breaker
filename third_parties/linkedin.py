import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape LinkedIn
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/aaronogenrwot/a294ec95b6e7e6e90319119f394cba02/raw/9ff2374374556f0d7da78932476ff593fb98c694/aaron-ogenrwot.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        headers = {"Authorization": "Bearer " + os.environ.get("PROXYCURL_API_KEY")}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        response = requests.get(
            api_endpoint,
            params={
                "linkedin_profile_url": linkedin_profile_url,
                "extra": "include",
                "github_profile_id": "include",
                "facebook_profile_id": "include",
                "twitter_profile_id": "include",
                "personal_contact_number": "include",
                "personal_email": "include",
                "inferred_salary": "include",
                "skills": "include",
                "use_cache": "if-present",
                "fallback_to_cache": "on-error",
            },
            headers=headers,
        )

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
        and k not in ["people_also_viewed", "certifications", "extra","activities"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://www.linkedin.com/in/aaron-ogenrwot-240ba716b/", True
        )
    )
