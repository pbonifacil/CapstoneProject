import streamlit as st

def app():
    st.caption('📝 | Blog')
    st.write('---')

    page = st.selectbox("Some Blog Posts:", 
                        ["-", "Blog 1", "Blog 2", "Blog 3", "Blog 4", "Blog 5"])

    if page == "-":
        st.write(' ')
    
    if page == "Blog 1":
        st.subheader("The Future of Car Shopping: A Dive into AutoMentor's Chatbot Technology")
        st.write('Explore how AutoMentor is reshaping the car-buying experience with its cutting-edge Chatbot technology. Discuss the benefits of personalized recommendations and the impact on the future of automotive retail.')
    

    if page == "Blog 2":
        st.subheader("Tech Enthusiast's Guide: Navigating the Automotive Landscape with AutoMentor")
        st.write('Tailored for tech-savvy individuals, this post explores how AutoMentor caters to the preferences of those who appreciate innovation and efficiency in the car-buying process.')


    if page == "Blog 3":
        st.subheader('Green Driving: Exploring Eco-Friendly Options with AutoMentor')
        st.write("Highlight AutoMentor's commitment to sustainability by showcasing its recommendations for eco-friendly car options. Discuss the growing importance of environmentally conscious choices in the automotive industry.")


    if page == "Blog 4":
        st.subheader("Mastering the Used Car Market: AutoMentor's Transparency Advantage")
        st.write('Shed light on how AutoMentor addresses the challenges of the used car market by providing transparent information and reliable recommendations, making the process smoother for buyers.')


    if page == "Blog 5":
        st.subheader("Empowering First-Time Buyers: AutoMentor's Guide to Confident Car Purchases")
        st.write("Offer insights and tips for first-time car buyers, emphasizing how AutoMentor's user-friendly interface and personalized guidance simplify the decision-making process for those new to the world of car ownership.")



    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(r"https://media0.giphy.com/media/ooYUlJtxYZabmgzf6P/giphy.gif", width = 300)     
    with col3:
        st.write('')


    st.write("---")
    st.caption("© 2024 AutoMentor | All rights reserved")
