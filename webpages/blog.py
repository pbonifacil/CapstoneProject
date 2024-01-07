import streamlit as st

def app():
    st.caption('📝 | Blog')
    st.write('---')

    page = st.selectbox("Some Blog Posts:", 
                        ["-", "Blog 1", "Blog 2", "Blog 3", "Blog 4", "Blog 5"])

    if page == "-":
        st.write(' ')
    
    if page == "Blog 1":
        st.subheader('Blog Title')
        st.write('Blog Text')
    

    if page == "Blog 2":
        st.subheader('Blog Title')
        st.write('Blog Text')


    if page == "Blog 3":
        st.subheader('Blog Title')
        st.write('Blog Text')


    if page == "Blog 4":
        st.subheader('Blog Title')
        st.write('Blog Text')


    if page == "Blog 5":
        st.subheader('Blog Title')
        st.write('Blog Text')



    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(r"https://media0.giphy.com/media/ooYUlJtxYZabmgzf6P/giphy.gif", width = 300)     
    with col3:
        st.write('')


    st.write("---")
    st.caption("© 2024 AutoMentor | All rights reserved")