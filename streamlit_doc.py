#streamlit run app.py
import streamlit as st
import pandas as pd
import time
# text Utilities
st.title('Startup Dashboard')
st.header('I am learning streamlit')
st.subheader('And i am loving it')
st.write('This is a normal text')
st.markdown(""" ### My favorite Movies
- DevDas
- Bikram-Vedha
- Intesteller
""")
st.code("""
def foo(input):
    return foo**2
X = foo(2)
""")
st.latex('x^2 + y^2 + 2 = 0')

# Display Elements
df = pd.DataFrame({
    'name':['Ashis','Muna','Adhya'],
    'marks':[60,70,90],
    'package':[10,12,15]
})
st.dataframe(df)
st.metric('Revenue','$ 50000','+3')
st.json({
    'name':['Ashis','Muna','Adhya'],
    'marks':[60,70,90],
    'package':[10,12,15]
})

# Display Media
st.image('Muna.jpg')
st.video("Adhya.mp4")
#st.audio('audio file')

# Creating layout
st.sidebar.title('This is a Side-Bar')

col1, col2 = st.columns(2)
with col1:
    st.image('muna.jpg')
with col2:
    st.image('muna.jpg')

# Showing Status
st.error('Login Failed')
st.success("Login Successful")
st.info('This is Info')
st.warning("This is Warning")
bar = st.progress(0)

# for i in range(1,101):
#     time.sleep(0.1)
#     bar.progress(i)

# Taking User Input
email = st.text_input('Enter Email')
age = st.number_input('Enter Your Age')
date = st.date_input("Enter Registration Date")

# Button

import streamlit as st

email = st.text_input('Enter Email')
password = st.text_input('Enter password')
gender = st.selectbox('Select Gender',['Male','Female','Others'])

btn = st.button('Login')

if btn:
    if email == 'ashish@gmail.com' and password == '123':
        st.success('Login Success')
        st.balloons()
        st.write(gender)
    else:
        st.error('Login Failed')



file = st.file_uploader("Upload a csv file")

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())


