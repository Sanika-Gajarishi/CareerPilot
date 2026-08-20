import streamlit as st
import requests

from components.auth_form import login_form
from services.auth import login_user


def show_login():

    left, center, right = st.columns([1, 2, 1])

    with center:

        submitted, email, password = login_form()

        if submitted:

            if not email:

                st.warning("Enter email.")
                return

            if not password:

                st.warning("Enter password.")
                return

            with st.spinner("Signing in..."):

                try:

                    login_user(
                        email=email,
                        password=password,
                    )

                    st.success("Login Successful")

                    st.rerun()

                except requests.HTTPError as e:

                    if e.response.status_code == 401:

                        st.error("Invalid Email or Password")

                    else:

                        st.error(e.response.text)

                except Exception as e:

                    st.error(str(e))