
import streamlit as st
from front_components.factories.userauthenticatorfactory import (
    create_env_user_authenticator,
)
from front_components.factories.usermenufactory import create_user_menu
from front_components.utils import hide_streamlit_style

st.set_page_config(
    page_title="MFS",
    page_icon="📼",
)

def main():
    hide_streamlit_style()

    authenticator = create_env_user_authenticator()
    authenticator.authorize()

    user_menu = create_user_menu(authenticator=authenticator)
    user_menu.render()


if __name__ == '__main__':

    main()
