import streamlit as st

def app():
    st.caption('📝 | Blog')
    st.write('---')

    page = st.selectbox("Our Blog Posts:", 
                        ["-", "The Future of Car Shopping", "Tech Enthusiast's Guide", "Green Driving", "Mastering the Used Car Market", "Empowering First-Time Buyers"])

    if page == "-":
        st.write(' ')
    
    if page == "The Future of Car Shopping":
        st.subheader("The Future of Car Shopping")
        st.write("**A Dive into AutoMentor's Chatbot Technology**")
        st.write('Explore how AutoMentor is reshaping the car-buying experience with its cutting-edge Chatbot technology. Discuss the benefits of personalized recommendations and the impact on the future of automotive retail.')
    

    if page == "Tech Enthusiast's Guide":
        st.subheader("Tech Enthusiast's Guide")
        st.write("**Navigating the Automotive Landscape with AutoMentor**")
        st.write('Tailored for tech-savvy individuals, this post explores how AutoMentor caters to the preferences of those who appreciate innovation and efficiency in the car-buying process.')


    if page == "Green Driving":
        st.subheader('Green Driving')
        st.write("**Exploring Eco-Friendly Options with AutoMentor**")
        st.write("Highlight AutoMentor's commitment to sustainability by showcasing its recommendations for eco-friendly car options. Discuss the growing importance of environmentally conscious choices in the automotive industry.")


    if page == "Mastering the Used Car Market":
        st.subheader("Mastering the Used Car Market")
        st.write("**AutoMentor's Transparency Advantage**")
        st.write('Shed light on how AutoMentor addresses the challenges of the used car market by providing transparent information and reliable recommendations, making the process smoother for buyers.')


    if page == "Empowering First-Time Buyers":
        st.subheader("Empowering First-Time Buyers")
        st.write("**AutoMentor's Guide to Confident Car Purchases**")
        st.write("Offer insights and tips for first-time car buyers, emphasizing how AutoMentor's user-friendly interface and personalized guidance simplify the decision-making process for those new to the world of car ownership.")



    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(r"https://upgrades.057tech.com/ModelXGif3.gif", width = 300)     
    with col3:
        st.write('')


    st.write("---")
    st.caption("© 2024 AutoMentor | All rights reserved")
