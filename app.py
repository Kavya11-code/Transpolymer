import streamlit as st
import home
import prediction 
import about
import contact
import login_page as login  # Renamed login.py to login_page.py for clarity and to avoid naming conflicts

# ✅ Must be first Streamlit command
#st.set_page_config(page_title="TransPolymer", layout="wide", page_icon="🧪")

# ✅ Ensure users collection exists
login.create_users_collection()

# ✅ Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ✅ Show login or main app
if not st.session_state.logged_in:
    login.show_login_page()
else:
    # ✅ Load Home page immediately after login
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # ✅ Sidebar navigation appears only after login
    st.sidebar.title("🔗 Navigation")
    st.session_state.page = st.sidebar.radio("Select a Page", ["Home", "Predictions", "About", "Help"], index=["Home", "Predictions", "About", "Help"].index(st.session_state.page))

    # ✅ Load page dynamically
    if st.session_state.page == "Home":
        home.show()
    elif st.session_state.page == "Predictions":
        prediction.show()
    elif st.session_state.page == "About":
        about.show()
    elif st.session_state.page == "Help":
        contact.show()
    else:
        st.error("Page not found.")