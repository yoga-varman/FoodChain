import streamlit as st


st.title("🔐 Food Chain Login")

username = st.text_input("Username")

password = st.text_input("Password",type="password")

if st.button("Login", use_container_width=True):

    if username == "admin" and password == "admin123":

        st.success("✅ Login successful")

        st.session_state["foodchain_logged_in"] = True
        st.session_state["foodchain_username"] = username

        st.rerun()

    else:
        st.error("❌ Invalid username or password")