import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import bcrypt
import extra_streamlit_components as stx  # type: ignore
import jwt
import requests  # type: ignore
import streamlit as st
import streamlit_pydantic as sp  # type: ignore
from backend.schemas import (
    User,
    UserCreateFull,
    UserCreatePassword,
    UserExtended,
    UserLogin,
    UserLoginResponse,
)
from pydantic import ValidationError
from streamlit_autorefresh import st_autorefresh

# from streamlit_authenticator.authenticate import Authenticate


class UserAuthenticator:

    def __init__(
            self, 
            api_url: str, 
            cookie_name: str, 
            cookie_key: str, 
            cookie_algorithm: str, 
            cookie_expiry_minutes: int, 
            inactivity_seconds: int, 
            inactivity_check_seconds: int
        ) -> None:

        self.api_url = api_url

        self.cookie_name = cookie_name
        self.cookie_key = cookie_key

        self.cookie_algorithm = cookie_algorithm
        self.cookie_expiry_minutes = cookie_expiry_minutes
        self.cookie_manager = stx.CookieManager()

        self._init_session_state()

        self.inactivity_seconds = inactivity_seconds
        self.inactivity_check_seconds = inactivity_check_seconds

        st_autorefresh(interval=1000 * self.inactivity_check_seconds, limit=100, key="authenticator_counter")


    def _init_session_state(self):
        st.session_state["user_info"] = {'authentication_status': False, "username": None, "id": None, "last_inactivity_check_datetime": datetime.now()}

    def _set_session_state_fields(self, authentication_status: Optional[bool] = None, username: Optional[str] = None, id: Optional[str] = None, last_inactivity_check_datetime: Optional[datetime] = None):
        if authentication_status:
            st.session_state["user_info"]['authentication_status'] = authentication_status
        if username:
            st.session_state["user_info"]['username'] = username
        if id:
            st.session_state["user_info"]["id"] = id
        if last_inactivity_check_datetime:
            st.session_state["user_info"]["last_inactivity_check_datetime"] = last_inactivity_check_datetime

    def _get_session_state_id(self) -> Optional[str]:
        return st.session_state["user_info"]['id']

    def _get_session_state_username(self) -> Optional[str]:
        return st.session_state["user_info"]['username']

    def _get_session_state_authentication_status(self) -> bool:
        return st.session_state["user_info"]['authentication_status']

    def _get_session_state_last_inactivity_check(self) -> datetime:
        return st.session_state["user_info"]["last_inactivity_check_datetime"]

    def _token_encode(self, username: str) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({
            'username':username,
            'exp_date':(datetime.utcnow() + timedelta(minutes=self.cookie_expiry_minutes)).timestamp()}, 
            self.cookie_key, algorithm=self.cookie_algorithm)

    def _token_decode(self, token) -> Dict[str, Any]:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        return jwt.decode(token, self.cookie_key, algorithms=['HS256'])

    def _set_cookie(self, username: str):
        self.cookie_manager.set(self.cookie_name, self._token_encode(username),
            expires_at=datetime.now() + timedelta(days=self.cookie_expiry_minutes))
        self._set_session_state_fields(username=username, authentication_status=True)

    def check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        encoded_token = self.cookie_manager.get(self.cookie_name)
        if not encoded_token:
            return 
        token = self._token_decode(encoded_token)

        if not token or 'username' not in token:
            return

        if not token['exp_date'] > datetime.utcnow().timestamp():
            return 


        response = requests.request("GET", f"{self.api_url}/users/username_password/{token['username']}/")
 
        if response.status_code != 200:
            return 

        self._set_session_state_fields(authentication_status=True, username=token['username'])

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  

    def _sign_up_form(self) -> UserCreatePassword:
        user_extended = sp.pydantic_input(key="signup_form", model=UserExtended)
        password = st.text_input('Password', type='password', help="The password of the user. It should be at least 8 characters long and contain at least one uppercase letter, one number, and one special character.")
        confirm_password = st.text_input('Confirm password', type='password', help="Repeat the password")
  
        if not st.button("Sign up"):
            return 

        if not(user_extended and password and confirm_password):
            st.error("Fill in the missing fields")
            return   
        try:

            return UserCreatePassword(username=user_extended["username"], email=user_extended["email"], name=user_extended["name"], password=password, confirm_password=confirm_password)
        except ValidationError as e:
            st.error(e)

    def sign_up(self):
        new_user = self._sign_up_form()
        if not new_user:
            return

        user_create = UserCreateFull(username=new_user.username, email=new_user.email, name=new_user.name, password=self._hash_password(new_user.password), subscription_datetime=datetime.now().isoformat(), last_active_datetime=datetime.now().isoformat())
        response = requests.post(f"{self.api_url}/users/", json=json.loads(json.dumps(user_create.dict(), default=str)))

        if response.status_code != 200:
            st.error(response.text) 
            return          


        st.success("Successful Sign up!\nPlease log in to proceed.")
        requests.post(f"{self.api_url}/users/send_signup_email/{user_create.username}/")


    def _log_in_form(self) -> UserLogin:
        login_form = st.form('Log in')
        username = login_form.text_input('Username')
        password = login_form.text_input('Password', type='password')
        if login_form.form_submit_button("Log in"):
            try:
                return UserLogin(username=username, password=password)
            except ValidationError as e:
                st.error(e)

    def log_in(self):
        data = self._log_in_form()
        if not data:
            return
 
        response = requests.request("GET", f"{self.api_url}/users/username_password/{data.username}/")
 
        if response.status_code != 200:
            st.error(f"Did not find user with username: {data.username}")
            return
        
        if not bcrypt.checkpw(password=data.password.encode(), hashed_password=response.json()["password"].encode()):
            st.error("Wrong password")
            return

        # set is_active to True
        response = requests.put(f"{self.api_url}/users/{data.username}/is_active/?is_active=true")
        if response.status_code != 200:
            st.error(response.text)
            return
        
        self._set_cookie(data.username)

    
    def set_is_active(self, username: str, is_active: bool):
        response = requests.put(f"{self.api_url}/users/{username}/is_active/?is_active={'false' if not is_active else 'true'}")
        if response.status_code != 200:
            st.error(response.text)

    def log_out(self):
        # set is_active to False
        username = self._get_session_state_username()
        if username:
            self.set_is_active(username=username, is_active=False)

        self.cookie_manager.delete(self.cookie_name)
        self._init_session_state()

    def render_authentication_menu(self):
        log_in, sign_up  =  st.tabs(["Log in", "Sign up"])
        with log_in:
            self.log_in()
        with sign_up:
            self.sign_up()

    def is_authorized(self) -> bool:
        self.check_cookie()
        return self._get_session_state_authentication_status()

 
    def authorize(self):

        if self.is_authorized():
            return

        st.write("# Welcome to MFS! 👋")
        self.render_authentication_menu()
        st.stop()


    def check_inactivity(self): 

        response = requests.request("GET", f"{self.api_url}/users/username/{self._get_session_state_username()}/")
        if response.status_code != 200:
            return
        user = User(**response.json())
        if (datetime.now() - user.last_active_datetime).seconds > self.inactivity_seconds and user.is_active:
            self.set_is_active(self._get_session_state_username(), is_active=False)

        self._set_session_state_fields(last_inactivity_check_datetime=datetime.now())
