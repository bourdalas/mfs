import os

from dotenv import find_dotenv, load_dotenv
from front_components.userauthenticator import UserAuthenticator


def create_env_user_authenticator() -> UserAuthenticator:
    load_dotenv(find_dotenv())
    return UserAuthenticator(
        api_url=os.environ["API_URL"],
        cookie_name=os.environ["USER_COOKIE_NAME"],
        cookie_key=os.environ["USER_COOKIE_KEY"],
        cookie_algorithm=os.environ["ACCESS_TOKEN_ALGORITHM"],
        cookie_expiry_minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]),
        inactivity_check_seconds=int(os.environ["USER_INACTIVITY_CHECK_SECONDS"]),
        inactivity_seconds=int(os.environ["USER_INACTIVITY_SECONDS"])
    )