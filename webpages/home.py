import streamlit as st

def app():
    st.caption('🏠 | Home Page')
    st.write('---')

    st.image(r"https://github.com/el-Migu-el/CapstoneProject/blob/main/webpages/images/horizontal_logo.png?raw=true", width=400)

    '''
    st.subheader('Steering toward your dream car!')'''
    st.write('*AutoMentor is more than just a technology company, it is your personal assistant in the world of cars.*')

    st.write('---')

    st.write('**Welcome to AutoMentor, where convenience meets customization in car shopping.**')
    st.write('''As a car buyer, you can effortlessly input your desired features and preferences, and our innovative Chatbot will instantly curate the most suitable options for you.
             AutoMentor is designed to make your car shopping experience easy, fast, and enjoyable.''')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(r"https://i.pinimg.com/originals/fb/a1/2c/fba12c167812b49f8fa4e033547445ff.gif", width = 300)     
    with col3:
        st.write('')


    st.write("**But that’s not all, as AutoMentor is also the future of car valuation for sellers.**")
    st.write("""Our intelligent Chatbot can predict your car’s price based on its characteristics, offering a fantastic feature for those looking to sell.
             It analyzes details such as model, age, and mileage to accurately forecast the potential selling price, empowering you with the knowledge to secure the best deal.""")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(r"https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/bfe0a770744351.5bad3c9b77f19.gif", width = 250)     
    with col3:
        st.write('')
    
          
    st.write("**Whether you’re in the market for a new car or selling your current one, AutoMentor is your go-to solution.**")
    st.write("""Embrace the simplicity and efficiency of car shopping and selling with AutoMentor – your partner in navigating the automotive world with confidence and ease.
             Visit our Chatbot page and experience the AutoMentor difference today!""")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(r"https://media2.giphy.com/media/VOBcjrSGd3Vv40imHG/giphy.gif", width = 400)     
    with col3:
        st.write('')
    

    st.write('**What are you waiting for?**')
    st.write('**Create your account and start using AutoMentor!**')
    st.image(r"https://media0.giphy.com/media/aOOdD40c3t9J85HJzZ/source.gif", width = 250)


    st.write("---")
    st.caption("© 2024 AutoMentor | All rights reserved")

    