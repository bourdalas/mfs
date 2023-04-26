from functools import partial
import json
import requests
from streamlit_chat import message
import streamlit as st
from backend.schemas import Message
from streamlit_autorefresh import st_autorefresh

class UserGroupChatComponent:

    def __init__(self, current_username: str, current_user_id: int) -> None:
        self.current_username = current_username
        self.current_user_id = current_user_id


    def show_history(self, group_id: int, n: int = 100):
        messages_response = requests.get(f"http://localhost:8000/user_groups/{group_id}/latest_messages/{n}")

        if not messages_response.status_code == 200:
            st.error(messages_response.status_code)
            return 

        for _message in messages_response.json():
            _message = Message(**_message)
            message(_message.text, _message.sender.username == self.current_username, seed=_message.sender.username, key=_message.id)


    def _new_message_callback(self, group_id: int ):
        st.session_state[f"{self.current_username}_message_text"] =st.session_state[f'{self.current_username}_message_text_input']
        st.session_state[f'{self.current_username}_message_text_input'] = ""

        message_response = requests.post(f"http://localhost:8000/user_groups/{group_id}/messages/", json={"text": st.session_state[f"{self.current_username}_message_text"], "sender_username": self.current_username})
        if not message_response.status_code == 200:
            st.error(message_response.status_code)
            return


    def write_message(self, group_id: int):
        st.session_state[f"{self.current_username}_message_text"] = ''
        st.text_input("Send message", key=f"{self.current_username}_message_text_input", on_change=partial(self._new_message_callback, group_id=group_id))

