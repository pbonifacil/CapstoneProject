import streamlit as st

def app():
    st.caption('🙂 | Account')
    st.write('---')

    st.write('To log in click here:')
    log_in = st.button('Log In')
    if log_in:
        st.write('**Log In**')
        st.write('Email:')
        st.write('Password:')
    
    st.write('---')

    st.write('To create an account click here:')
    sign_up = st.button('Sign Up')   
    if sign_up:
        st.write('**Create your account to start using AutoMentor!**')
        st.write('Enter your name, email, and location! Do not forget to define a password!')
        st.write('Name:')
        st.write('Email:')
        st.write('Password:')
        st.write('Location:')

    st.write('---')
