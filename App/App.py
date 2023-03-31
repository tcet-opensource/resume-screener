import streamlit as st

def main():
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities, key="level_select")
    return choice

def User():
    st.write('Welcome to user panel')
   
def Admin():
    st.write('Welcome to admin panel')

if main() == "User":
    User()
else:
    Admin()
    

