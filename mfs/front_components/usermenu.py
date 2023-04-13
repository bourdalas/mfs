import datetime
import time
from enum import Enum
from functools import partial
from math import ceil
from typing import Callable, Dict, List

import pandas as pd
import requests
import streamlit as st
import streamlit_pydantic as sp
from backend.schemas import ItemBase, User, UserExtended
from front_components.userauthenticator import UserAuthenticator


class UserMenuSidebar(Enum):
    my_profile = "My Profile"
    all_users = "Community"
    add_item = "Add Item"
    log_out = "Log Out"



def check_every_n_seconds(n):
    start_time = time.time()
    consecutive_seconds = 0
    
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time >= n:
            start_time = current_time
            consecutive_seconds = 0
        
        if consecutive_seconds >= 5:
            return True
        
        if elapsed_time % 1 < 0.01:
            consecutive_seconds += 1
            
        time.sleep(1)

class UserMenu:

    def __init__(self, authenticator: UserAuthenticator) -> None:
        self.authenticator = authenticator

    @property
    def set_active_fn(self):
        return partial(self.authenticator.set_is_active, username=self.authenticator._get_session_state_username(), is_active=True)


    def create_sidebar_menu_radio(self):
        with st.sidebar:
            st.session_state["user_menu"] = st.radio(label="Menus", options=[e.value for e in UserMenuSidebar], on_change=self.set_active_fn)

    def render_my_profile_menu(self):
        st.write("# My profile")

        profile, update = st.tabs(["Personal Information", "Update status"])

        with profile:
            user_response = requests.request("GET", f"http://localhost:8000/users/username/{st.session_state['user_info']['username']}")             
            items = User(**user_response.json()).items
            user = UserExtended(**user_response.json())
            sp.pydantic_output(user)
            with st.expander("Show items"):
                st.json(items)
        with update:
            st.write("### Update email")    
            new_email = st.text_input("New email")
            if st.button("Update"):
                user_response = requests.request("PUT", f"http://localhost:8000/users/{st.session_state['user_info']['username']}/email/?email={new_email}")             


    def _was_last_seen(self, last_active_datetime: datetime.datetime) -> str:
        timedelta = datetime.datetime.now() - last_active_datetime 
        st.write()
        if timedelta.total_seconds() >= 24*60*60:
            return f"{ceil(timedelta.total_seconds() / (24*60*60))} days"    
        elif timedelta.total_seconds() >= 2 * 60*60: 
            return f"{ceil(timedelta.total_seconds() / (60*60))} hours"    
        elif timedelta.total_seconds() >= 60*60: 
            return f"{ceil(timedelta.total_seconds() / (60*60))} hour"    
        elif timedelta.total_seconds() >= 2*60: 
            return f"{ceil(timedelta.total_seconds() / (60))} minutes"    
        elif 60 < timedelta.total_seconds() < 2*60: 
            return f"{ceil(timedelta.total_seconds() / (60))} minute"    
 
        return f"{int(timedelta.total_seconds())} seconds"    
 

    def _render_online_users(self, users: List[User]):

        df = pd.DataFrame([user for user in users if user["is_active"]])
        if df.empty:
            return

        st.write("# Online Users") 
        df["# items"] = df["items"].apply(lambda x: len(x))
        # df["last seen online"] = [self._was_last_seen(datetime.datetime.fromisoformat(x)) for x in df["last_active_datetime"].to_list()]
        df["subscribed at"] = [datetime.datetime.fromisoformat(x).date() for x in df["subscription_datetime"].to_list()]
        df = df.rename(columns={"is_active": "is online"})
        df = df.drop(columns=["items", "id", "last_active_datetime", "subscription_datetime", "is online"]).set_index("username")

        st.dataframe(df)

    def _render_offline_users(self, users: List[User]):
        df = pd.DataFrame([user for user in users if not user["is_active"]])
        if df.empty:
            return

        st.write("# Offline Users") 
        df["# items"] = df["items"].apply(lambda x: len(x))
        df["last seen online"] = [self._was_last_seen(datetime.datetime.fromisoformat(x)) for x in df["last_active_datetime"].to_list()]
        df["subscribed at"] = [datetime.datetime.fromisoformat(x).date() for x in df["subscription_datetime"].to_list()]
        df = df.rename(columns={"is_active": "is online"})
        df = df.drop(columns=["items", "id", "last_active_datetime", "subscription_datetime", "is online"]).set_index("username")

        st.dataframe(df)

    def render_all_users_menu(self):
        users = requests.request("GET", f"http://localhost:8000/users/")             
        if users.status_code != 200:
            return 

        online, offline = st.tabs(["Online", "Offline"])
        with online:
            self._render_online_users(users.json())
        with offline:
           self._render_offline_users(users.json())        
        
        if st.button("Refresh", on_click=self.set_active_fn):
            pass
 
    def log_out(self):
        self.authenticator.log_out()

    def delete_profile(self):
        if st.button("Are you sure?"):
            if requests.request("DELETE", f"http://localhost:8000/users/username/{st.session_state['user_info']['username']}"):
                st.success("Profile deleted, Have a nice day")
            else:
                st.error("Error during deleting")

    def add_item(self):
        item =  sp.pydantic_form(key="new_item_form", model=ItemBase)
        if not item:
          return 
        
        item_response = requests.request("POST", f"http://localhost:8000/users/{st.session_state['user_info']['username']}/items/", json=item.dict())             

        if not item_response.status_code == 200:
            st.error("Error during adding request")
            return
        st.success(f"Item: {item.title} added to {st.session_state['user_info']['username']}'s profile!")             

    @property
    def call_radio_fn(self) -> Dict[UserMenuSidebar, Callable]:
        return {
            UserMenuSidebar.my_profile: self.render_my_profile_menu, 
            UserMenuSidebar.add_item: self.add_item,
            UserMenuSidebar.all_users: self.render_all_users_menu, 
            UserMenuSidebar.log_out: self.log_out,
            }

    def render(self):
        self.create_sidebar_menu_radio()
        self.call_radio_fn[UserMenuSidebar(st.session_state["user_menu"])]()
        