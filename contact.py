import streamlit as st

def show():
    # Custom styles for dark theme and remove top padding
    st.markdown("""
        <style>
        body {
            background-color: #121212;
            color: #f1f1f1;
        }
        section[data-testid="stSidebar"] + div div[data-testid="stVerticalBlock"] {
            padding-top: 0rem;
        }
        .section-title {
            font-size: 26px;
            font-weight: bold;
            color: #4B8BBE;
            margin-top: 2rem;
        }
        .subsection {
            font-size: 18px;
            margin-top: 1rem;
        }
        .faq, .glossary, .troubleshoot {
            background-color: #333333;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            color: #f1f1f1;
        }
        .email-box {
            background-color: #2C3E50;
            padding: 1rem;
            border-radius: 10px;
            color: #f1f1f1;
        }
        .st-expanderHeader {
            color: #4B8BBE;
        }
        .st-expanderContent {
            color: #f1f1f1;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page title
    st.title("📘 Help & Support - TransPolymer")

    st.markdown("<div class='section-title'>❓ Help Center - TransPolymer</div>", unsafe_allow_html=True)
    st.markdown("Welcome to the **TransPolymer Help Page**. This guide will walk you through how to use the app effectively.")

    # 1. Getting Started
    st.markdown("<div class='section-title'>🚀 Getting Started</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Step 1:** Go to the **Prediction** page.
    - **Step 2:** Enter a valid **SMILES string**.
    - **Step 3:** Click **Predict** to see the results.
    - The app will return **six polymer properties** based on your input.
    """)

    # 2. FAQ
    st.markdown("<div class='section-title'>📌 Frequently Asked Questions</div>", unsafe_allow_html=True)
    with st.expander("🧬 What is a SMILES format?"):
        st.markdown("SMILES (Simplified Molecular Input Line Entry System) is a line notation for describing molecular structures using short ASCII strings.")
    with st.expander("❌ What if I enter an invalid SMILES string?"):
        st.markdown("The system will show an error if the SMILES string is incorrectly formatted or contains special characters.")

    
    # 3. Troubleshooting Tips
    st.markdown("<div class='section-title'>🛠️ Troubleshooting</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""
        - ❌ **Common Mistakes**:
            - Extra spaces in SMILES strings
            - Using unsupported or uncommon formats
        - 🔄 **To Refresh**: Press `Ctrl+R` or click the "Rerun" button if something goes wrong.
        """)

    # 4. Support
    st.markdown("<div class='section-title'>📬 Support</div>", unsafe_allow_html=True)
    st.markdown("""
    For further help, reach us at 📧 **transpolymer2@gmail.com**  
    GitHub - https://github.com/Transpolymer
    """)

# Run this file directly for testing
if __name__ == "__main__":
    show()