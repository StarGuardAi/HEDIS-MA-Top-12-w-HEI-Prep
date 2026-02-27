import streamlit as st

st.set_page_config(page_title="Ultra Simple Test", layout="wide")

st.title("Ultra Simple Test")
st.write("If you can see this, Streamlit is working!")

if st.button("Click me"):
    st.write("Button clicked!")

