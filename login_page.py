import streamlit as st
import bcrypt
from db import get_database
import time

def create_users_collection():
    db = get_database()
    if "users" not in db.list_collection_names():
        db.create_collection("users")

def signup(data):
    db = get_database()
    if db.users.find_one({"username": data["username"]}):
        return False, "Username already exists"
    elif db.users.find_one({"email": data["email"]}):
        return False, "Email already exists"
    else:
        hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
        data["password"] = hashed
        db.users.insert_one(data)
        return True, "Account created successfully!"

def login_user(username, password):
    db = get_database()
    user = db.users.find_one({"username": username})
    if user:
        stored_password = user["password"]
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
        if bcrypt.checkpw(password.encode(), stored_password):
            return True, user
    return False, None

def reset_password(email, new_password):
    db = get_database()
    user = db.users.find_one({"email": email})
    if user:
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        db.users.update_one({"email": email}, {"$set": {"password": hashed}})
        return True
    return False

def show_login_page():
    # Apply custom CSS for modern, animated UI
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            * {
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            /* Dark theme background */
            body {
                background-color: #121420 !important;
                color: #fff;
            }
            
            /* Override Streamlit's default spacing */
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                margin-top: 0 !important;
                max-width: 1000px;
            }
            
            /* Target all Streamlit containers */
            .css-18e3th9, .css-1d391kg, .css-1wrcr25, .css-ocqkz7, .css-j7qwjs {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            /* Override header spacing */
            header {
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
            }
            
            
            .app-header-container {
                margin: 0 !important;
                padding: 20px 0 5px 0 !important; /* Reduced bottom padding from 10px to 5px */
                line-height: 1 !important;
            }
            
            .centered-heading {
                text-align: center;
                font-weight: 700;
                background: linear-gradient(90deg, #4B8BBE, #306998);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0 !important;
                padding: 0 !important;
                line-height: 1.2 !important;
                font-size: 4.0rem !important; /* Increased from 2.5rem to 3.5rem */
            }
            
            .subheading {
                text-align: center;
                color: #ddd;
                font-weight: 400;
                margin: 5px 0 10px 0 !important; /* Reduced from 10px top and 20px bottom to 5px top and 15px bottom */
                padding: 0 !important;
                line-height: 1.2 !important;
            }
            
            # Find this CSS class in your show_login_page() function:

            .stButton > button {
                width: 60%; /* Set a fixed width for all buttons - adjust percentage as needed */
                padding: 12px 0;
                font-size: 16px;
                background: linear-gradient(90deg, #4B8BBE, #306998);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
                margin-top: 10px;
                margin-left: auto; /* Center the button */
                margin-right: auto; /* Center the button */
                display: block; /* Makes margin auto work for centering */
            }
                
            /* This ensures button containers are also centered */
            [data-testid="stButton"] {
                    text-align: center !important;
                    display: flex !important;
                    justify-content: center !important;
            }
                
            /* Force container to center contents */
            .element-container:has(.stButton) {
                    display: flex !important;
                    justify-content: center !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 7px 14px rgba(0, 0, 0, 0.3);
            }
            
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 1px solid #444;
                background-color: rgba(30, 33, 43, 0.8);
                color: #fff;
                padding: 10px 15px;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #4B8BBE;
                box-shadow: 0 0 0 2px rgba(75, 139, 190, 0.2);
            }
            
            .stSelectbox > div > div > div {
                border-radius: 8px;
                border: 1px solid #444;
                background-color: rgba(30, 33, 43, 0.8);
                color: #fff;
                padding: 2px 15px;
            }
            
            .form-fade {
                animation: fadeIn 0.5s ease forwards;
                opacity: 0;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .loader {
                display: inline-block;
                width: 80px;
                height: 80px;
                margin: 0 auto;
            }
            
            .loader:after {
                content: " ";
                display: block;
                width: 64px;
                height: 64px;
                margin: 8px;
                border-radius: 50%;
                border: 6px solid #4B8BBE;
                border-color: #4B8BBE transparent #4B8BBE transparent;
                animation: loader 1.2s linear infinite;
            }
            
            @keyframes loader {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .switch-link {
                color: #4B8BBE;
                text-align: center;
                cursor: pointer;
                margin-top: 15px;
                font-size: 14px;
                text-decoration: none;
                display: block;
            }
            
            .switch-link:hover {
                text-decoration: underline;
            }
            
            .back-btn {
                color: #4B8BBE;
                cursor: pointer;
                margin-top: 15px;
                font-size: 14px;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .back-btn:hover {
                text-decoration: underline;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-label {
                font-size: 14px;
                color: #bbb;
                margin-bottom: 5px;
                font-weight: 500;
            }
            
            /* Toast notification */
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 25px;
                background: #1e212b;
                color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.25);
                z-index: 9999;
                opacity: 0;
                transform: translateY(-20px);
                animation: toast-in 0.3s forwards, toast-out 0.3s forwards 3s;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .toast.success {
                border-left: 4px solid #4CAF50;
            }
            
            .toast.error {
                border-left: 4px solid #F44336;
            }
            
            @keyframes toast-in {
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes toast-out {
                to { opacity: 0; transform: translateY(-20px); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Hide Streamlit default elements
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            
            /* Zero out all padding and margins at the top */
            .stApp > header {
                display: none;
            }
            
            /* Ensure the app starts from the very top */
            .stApp {
                margin-top: 0 !important;
            }
            
            /* Force no spacing at the top */
            .element-container:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo and Header - Using a div container with strict spacing control
    st.markdown("""
        <div class="app-header-container">
            <h1 class="centered-heading">TransPolymer</h1>
            <h4 class="subheading">Get quick predictions using advanced polymer technology</h4>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state variables
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
    if "loading" not in st.session_state:
        st.session_state.loading = False
    if "toast" not in st.session_state:
        st.session_state.toast = None

    # Display toast notification if needed
    if st.session_state.toast:
        toast_type, message = st.session_state.toast
        st.markdown(f"""
            <div class="toast {toast_type}">
                <span>{message}</span>
            </div>
        """, unsafe_allow_html=True)
        # Clear toast after displaying
        st.session_state.toast = None

    # Create a centered card layout
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        # Loading spinner
        if st.session_state.loading:
            st.markdown('<div class="form-fade">', unsafe_allow_html=True)
            st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; margin-top: 20px;">Processing...</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(1.5)  # Simulated loading time
            st.session_state.loading = False
            st.rerun()
        
        # --- Login Form ---
        elif st.session_state.auth_mode == "login":
            st.markdown('<div class="form-fade">', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">Username</div>', unsafe_allow_html=True)
            username = st.text_input("", key="login_username", placeholder="Enter your username")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", key="login_password", placeholder="Enter your password")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Login button with animation
            if st.button("Login Now", key="login_submit"):
                st.session_state.loading = True
                success, user = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.toast = ("success", "Login successful! Redirecting...")
                else:
                    st.session_state.toast = ("error", "Invalid username or password")
                st.rerun()
                
            # Forgot Password Button
            if st.button("Forgot Password?", key="forgot_btn"):
                st.session_state.auth_mode = "forgot"
                st.rerun()
            
            # Sign Up Button
            if st.button("Sign Up", key="switch_to_signup"):
                st.session_state.auth_mode = "signup"
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Sign Up Form ---
        elif st.session_state.auth_mode == "signup":
            st.markdown('<div class="form-fade">', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">Sign up as</div>', unsafe_allow_html=True)
            role = st.selectbox("", ["Scientist", "Student", "Researcher"], key="role")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                st.markdown('<div class="form-label">Username</div>', unsafe_allow_html=True)
                username = st.text_input("", key="signup_username", placeholder="Choose a username")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                st.markdown('<div class="form-label">Email</div>', unsafe_allow_html=True)
                email = st.text_input("", key="signup_email", placeholder="Your email address")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Role-specific fields
            if role == "Student":
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="form-group">', unsafe_allow_html=True)
                    st.markdown('<div class="form-label">Student ID</div>', unsafe_allow_html=True)
                    student_id = st.text_input("", key="signup_student_id", placeholder="Your student ID")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="form-group">', unsafe_allow_html=True)
                    st.markdown('<div class="form-label">College Name</div>', unsafe_allow_html=True)
                    college_name = st.text_input("", key="signup_college", placeholder="Your college name")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            elif role in ["Scientist", "Researcher"]:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                st.markdown('<div class="form-label">Organisation</div>', unsafe_allow_html=True)
                organisation = st.text_input("", key="signup_organisation", placeholder="Your organisation name")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">State</div>', unsafe_allow_html=True)
            state = st.text_input("", key="signup_state", placeholder="Your state")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                st.markdown('<div class="form-label">Password</div>', unsafe_allow_html=True)
                password = st.text_input("", type="password", key="signup_password", placeholder="Create a password")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                st.markdown('<div class="form-label">Confirm Password</div>', unsafe_allow_html=True)
                confirm_password = st.text_input("", type="password", key="signup_confirm", placeholder="Confirm password")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Prepare signup data
            if role == "Student":
                signup_data = {
                    "role": role,
                    "username": username,
                    "student_id": student_id if 'student_id' in locals() else "",
                    "college_name": college_name if 'college_name' in locals() else "",
                    "email": email,
                    "state": state,
                    "password": password
                }
            else:
                signup_data = {
                    "role": role,
                    "username": username,
                    "email": email,
                    "organisation": organisation if 'organisation' in locals() else "",
                    "state": state,
                    "password": password
                }
            
            # Register button
            if st.button("Create Account", key="signup_submit"):
                if password != confirm_password:
                    st.session_state.toast = ("error", "Passwords don't match")
                    st.rerun()
                elif not username or not email or not password:
                    st.session_state.toast = ("error", "Please fill all required fields")
                    st.rerun()
                else:  
                    st.session_state.loading = True
                    success, message = signup(signup_data)
                    if success:
                        st.session_state.auth_mode = "login"
                        st.session_state.toast = ("success", message)
                    else:
                        st.session_state.toast = ("error", message)
                    st.rerun()
            
            # Back to login button
            if st.button("Back to Login", key="back_to_login"):
                st.session_state.auth_mode = "login"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Forgot Password Form (only accessible from login page, but keeping code in case it's needed) ---
        elif st.session_state.auth_mode == "forgot":
            st.markdown('<div class="form-fade">', unsafe_allow_html=True)
            
            st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Reset Password</h3>", unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">Email</div>', unsafe_allow_html=True)
            email = st.text_input("", key="forgot_email", placeholder="Enter your registered email")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">New Password</div>', unsafe_allow_html=True)
            new_password = st.text_input("", type="password", key="forgot_password", placeholder="Enter new password")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">Confirm New Password</div>', unsafe_allow_html=True)
            confirm_password = st.text_input("", type="password", key="forgot_confirm", placeholder="Confirm new password")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reset button
            if st.button("Reset Password", key="reset_submit"):
                if not email or not new_password:
                    st.session_state.toast = ("error", "Please fill all fields")
                    st.rerun()
                elif new_password != confirm_password:
                    st.session_state.toast = ("error", "Passwords don't match")
                    st.rerun()
                else:
                    st.session_state.loading = True
                    if reset_password(email, new_password):
                        st.session_state.auth_mode = "login"
                        st.session_state.toast = ("success", "Password reset successful")
                    else:
                        st.session_state.toast = ("error", "Email not found")
                    st.rerun()
            
            # Back to login button
            if st.button("Back to Login", key="back_btn"):
                st.session_state.auth_mode = "login"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)