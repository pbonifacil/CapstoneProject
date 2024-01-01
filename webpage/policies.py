import streamlit as st

def app():
    st.caption('Policies')

    page = st.selectbox("For a more detailed view of our policies:", 
                        ["Terms & Policies", "Privacy Policy", "Brand Guidelines"])

    if page == "Terms & Policies":
        st.subheader('Terms and Policies')
        st.write('**By using AutoMentor, you agree to the following terms and policies:**')
    
        st.markdown('**User Data**')
        st.caption('AutoMentor collects user data such as name, email address, and location to provide personalized recommendations. We do not share this data with third parties without the user’s consent.')
    
        st.markdown('**Recommendations**')
        st.caption('AutoMentor provides car recommendations based on the user’s preferences. These recommendations are generated using machine learning algorithms and are not guaranteed to be accurate. AutoMentor is not responsible for any damages or losses incurred as a result of using our recommendations.')
    
        st.markdown('**User Conduct**')
        st.caption('Users are expected to use AutoMentor in a responsible and respectful manner. Users are prohibited from using AutoMentor to engage in any illegal or unethical activities.')
    
        st.markdown('**Intellectual Property**')
        st.caption('All content provided by AutoMentor is protected by intellectual property laws. Users are prohibited from copying, modifying, or distributing AutoMentor’s content without our consent.')

        st.markdown('**Termination**')
        st.caption('AutoMentor reserves the right to terminate user access to the chatbot at any time and for any reason.')    

        st.markdown('**Changes to Terms and Policies**')
        st.caption('AutoMentor reserves the right to modify these terms and policies at any time. Users will be notified of any changes via email.') 

    if page == "Privacy Policy":
        st.subheader('Privacy Policy')
        st.write('**AutoMentor is committed to protecting your privacy. This privacy policy explains how we collect, use, and disclose your personal information when you use our chatbot.**')
    
        st.markdown('**User Data**')
        st.caption('We collect the following information from you when you use AutoMentor:')
        st.caption(' - Name')
        st.caption(' - Email address')
        st.caption(' - Location')
        st.caption('We use this information to provide personalized recommendations for cars.')
    
        st.markdown('**How is your information used**')
        st.caption('We use your information to provide personalized recommendations for cars. We do not share your information with third parties without your consent.')
    
        st.markdown('**Security**')
        st.caption('We take reasonable measures to protect your information from unauthorized access, use, or disclosure.')
    
        st.markdown('**Retention**')
        st.caption('We retain your information for as long as necessary to provide you with our services and as required by law.')

        st.markdown('**Changes to This Policy**')
        st.caption('We may update this privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page.')    


    if page == "Brand Guidelines":
        st.subheader('Brand Guidelines')
        st.write('**Automentor brand guidelines:**')
    
        st.markdown('**Logo**')
        st.caption('The AutoMentor logo should be used whenever possible to maintain brand recognition and consistency. Please refer to clear space, sizing, and usage on backgrounds guidelines for best practices.')
    
        st.markdown('**Colors**')
        st.caption('The AutoMentor primary color palette is composed of four colors: #b6bbc4, #161a30, #31304d, and #f0ece5. These colors should be used regularly in marketing materials to reinforce the AutoMentor brand.')
    
        st.markdown('**Typography**')
        st.caption('Our primary typeface, Monospace, is used for headlines, subheadlines, CTA’s, and body text. It works equally well in print and digital applications. Please use Monospace in all communication materials whenever possible.')
    


