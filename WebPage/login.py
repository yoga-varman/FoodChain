import sys
import secrets
import string
import hashlib
import streamlit as st

sys.path.append("/home/yogavarman/Projects/FoodChain")

from Config.db import get_conn
from Functions.AllFunctions import generate_userid
from Functions.LogInFun import login_user,create_user,send_user_credentials


st.set_page_config(
    page_title="FoodChain Login",
    page_icon="🔐",
    layout="centered"
)



# UI

st.title("🔐 FoodChain")
st.caption("Food Chain Management Portal")
login_tab, create_tab = st.tabs(["🔑 Login", "👤 Create User"])


# LOGIN TAB

with login_tab:
    st.subheader("Login")
    username = st.text_input("Username",key="login_username")
    password = st.text_input("Password",type="password",key="login_password")
    if st.button(
        "Login",
        use_container_width=True,
        type="primary"
    ):
        if not username or not password:
            st.warning("Please enter username and password.")
        else:
            try:
                if login_user(username, password):
                    st.success("✅ Login successful")
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.switch_page("FoodChain/dashboard.py")
                else:
                    st.error("❌ Invalid username or password")
            except Exception as e:
                st.error(f"Login failed: {e}")


# CREATE USER TAB

with create_tab:
    st.subheader("Create User")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name",key="first_name")
    with col2:
        last_name = st.text_input("Last Name",key="last_name")
    

    gender = st.selectbox("Gender",
        [
            "Male",
            "Female",
            "Other"
        ],
        key="gender"
    )

    email = st.text_input("Email ID",key="email")
    date_of_birth = st.date_input("Date of Birth",key="date_of_birth")
    if st.button("Create User",use_container_width=True,type="primary"):
        # Validation
        if not first_name.strip():
            st.warning("Please enter first name.")
        elif not last_name.strip():
            st.warning("Please enter last name.")
        elif not email.strip():
            st.warning("Please enter email ID.")
        else:
            try:
                # Create database user
                user_id, username, temporary_password = create_user(
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    gender=gender,
                    email=email.strip(),
                    dob=date_of_birth
                )

                # Send email
                send_user_credentials(
                    email=email.strip(),
                    first_name=first_name.strip(),
                    username=username,
                    password=temporary_password
                )
                st.success("✅ User created successfully!")
                st.info(f"Username `{username}` has been sent to `{email}`.")
            except Exception as e:
                st.error(f"❌ User creation failed: {e}")