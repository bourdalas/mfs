from front_components.userauthenticator import UserAuthenticator
from front_components.usermenu import UserMenu


def create_user_menu(authenticator: UserAuthenticator) -> UserMenu:
    return UserMenu(authenticator)