import streamlit as st

st.title('Monte Carlo on Stocks')

button1 = st.button("click me")
if button1:
    st.write("Fuck u!")

st.header("Start of the Radio button section!")

like = st.checkbox("Do u like me?")
button2 = st.button("Submit")
if button2:
    if like:
        st.write("Ty! I like u too")
    else:
        st.write("fuck")
        

st.header("Start of the Radio button section!")
animal = st.radio("What's ur favorite animal?", ("Lion", "Tiger", "Bears"))
button3 = st.button("Submit Animal")
if button3:
    st.write(animal)
    if animal == "Lion":
        st.write("ROAR!")

                  
st.header("Start of the Selectbox!")
animal2 = st.selectbox("What's ur favorite animal?", ("Lion", "Tiger", "Bears"))
button4 = st.button("Submit Animal 2")
if button4:
    st.write(animal2)
    if animal2 == "Lion":
        st.write("ROAR!")



st.header("Start of the Multiselection Selectbox!")
options = st.multiselect("What animals do u like?", ["Lion", "Tiger", "Bear"])
button5 = st.button("Print Animals")
if button5:
    st.write(options)


st.header("Start of the Slider Selectbox!")
epochs_num = st.slider("How many epochs?", 1, 100)
st.write(epochs_num)


st.header("Start of the Text Input!")
user_text = st.text_input("What's ur favorite movie?", "Modern Family")
if st.button("Text Button"):
    st.write(user_text)














