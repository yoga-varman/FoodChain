import sys
from datetime import datetime
import streamlit as st

sys.path.append("/home/yogavarman/Projects/FoodChain")

from Config.db import JDBC_URL, DB_PROPERTIES, DATABASE_URL,get_conn

from Functions.AllFunctions import generate_userid

from Functions.LogInFun import JDBC_URL, DB_PROPERTIES, DATABASE_URL,get_conn

import secrets
import string
import hashlib



def generate_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%"
    return "".join(secrets.choice(characters) for _ in range(length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def login_user(username, password):
    conn = get_conn()
    try:
        cur = conn.cursor()
        password_hash = hash_password(password)
        cur.execute(
            """
            SELECT user_id, first_name, last_name
            FROM foodchain.users
            WHERE username = %s
              AND password_hash = %s
              AND is_active = TRUE
            """,
            (username, password_hash)
        )
        user = cur.fetchone()
        if user:
            st.session_state["foodchain_logged_in"] = True
            st.session_state["foodchain_user_id"] = user[0]
            st.session_state["foodchain_username"] = username
            st.session_state["foodchain_name"] = f"{user[1]} {user[2]}"
            return True
        return False
    finally:
        cur.close()
        conn.close()



def create_user(first_name, last_name, gender, email, dob):
    conn = get_conn()
    try:
        cur = conn.cursor()
        # Generate username using your existing function
        username = generate_userid(cur)
        # Generate temporary password
        temporary_password = generate_password()
        # Hash password before storing
        password_hash = hash_password(temporary_password)
        cur.execute(
            """
            INSERT INTO foodchain.users
            (
                user_id,
                username,
                password_hash,
                first_name,
                last_name,
                gender,
                email,
                date_of_birth,
                is_active,
                created_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                TRUE,
                CURRENT_TIMESTAMP
            )
            RETURNING user_id
            """,
            (
                username,
                username,
                password_hash,
                first_name,
                last_name,
                gender,
                email,
                dob
            )
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id, username, temporary_password
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
        
        
def send_user_credentials(email, first_name, username, password):

    import smtplib
    from email.message import EmailMessage

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587

    SMTP_USERNAME = "yourgmail@gmail.com"
    SMTP_PASSWORD = "your-16-character-app-password"

    message = EmailMessage()

    message["Subject"] = "FoodChain Account Created"
    message["From"] = SMTP_USERNAME
    message["To"] = email

    message.set_content(
        f"""
Hello {first_name},

Your FoodChain account has been created successfully.

Username: {username}
Temporary Password: {password}

Please login to FoodChain using these credentials.

Regards,
FoodChain Team
"""
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )

        server.send_message(message)