import streamlit as st

# Define the show() function to display the About page
def show():
    # Page title and content
    st.markdown("<h2 style='text-align:center; color:#4B8BBE;'>🌐 About TransPolymer</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Why TransPolymer Section
    st.markdown("""
    <div style='background-color: #E0F7FA; padding: 15px; border-radius: 15px; text-align: center;'>
        <h3 style='color: #00796B; margin-bottom: 10px;'>Why TransPolymer</h3>
        <p style='font-size: 18px; color: #333333;'>
            In TransPolymer, we use models like <b>ChemBERTa</b> to learn from SMILES strings — a special way to represent molecules.
            This enables understanding of complex molecular structures and provides accurate predictions, even for new polymers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 🔬 Properties Predicted Section with Animated Cards
    st.markdown("### 🔬 Properties Predicted by TransPolymer", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .card {
        background: #f1f8ff;
        border: 1px solid #d9e7f5;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(75, 139, 190, 0.15);
        color: #4B8BBE;
        font-weight: bold;
        opacity: 0;
        transform: scale(0.5) rotate(0deg);
        animation: burst 6s ease-out forwards;
    }
    .card:nth-child(1) { animation-delay: 0.4s; }
    .card:nth-child(2) { animation-delay: 1.2s; }
    .card:nth-child(3) { animation-delay: 2.0s; }
    .card:nth-child(4) { animation-delay: 2.8s; }
    .card:nth-child(5) { animation-delay: 3.6s; }
    .card:nth-child(6) { animation-delay: 4.4s; }

    .card:hover {
        transform: scale(1.05);
        background-color: #e6f3ff;
        box-shadow: 0 6px 18px rgba(75, 139, 190, 0.25);
        text-shadow: 0px 0px 8px rgba(75, 139, 190, 0.5);
    }

    @keyframes burst {
        0% {
            opacity: 0;
            transform: scale(0.5) rotate(-15deg);
        }
        40% {
            opacity: 1;
            transform: scale(1.1) rotate(5deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotate(0deg);
        }
    }
    </style>

    <div class="card-container">
        <div class="card">Tensile Strength</div>
        <div class="card">Ionization Energy</div>
        <div class="card">Electron Affinity</div>
        <div class="card">LogP</div>
        <div class="card">Refractive Index</div>
        <div class="card">Molecular Weight</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 👨‍🏫 Mentor Section
    st.markdown("### 👨‍🏫 Our Mentor", unsafe_allow_html=True)
    st.markdown(""" 
    <div style='text-align: justify; font-size: 17px; color: #FFFFFF;;'>
    We are deeply grateful to our mentor, Mrs. Navatha Kolisetti, for her constant guidance and support throughout the TransPolymer project.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 📚 SMILES Info and 🔍 Use Case with Pulse Animation
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Learn More About SMILES"):
                st.markdown("""
                <div style='animation: pulse 1.5s infinite; background-color:#eef7fd; padding: 20px; border-radius: 15px; font-size: 16px; color: #333;'>
                <b>SMILES</b> stands for <i>Simplified Molecular Input Line Entry System</i>.<br><br>
                It encodes molecules as text strings like C1=CC=CC=C1 (for Benzene).  
                SMILES is simple yet powerful, making it perfect for AI training on chemical data.
                </div>
                """, unsafe_allow_html=True)
        with col2:
            if st.button("🔍 Example Use Case"):
                st.markdown("""
                <div style='animation: pulse 1.5s infinite; background-color:#eef7fd; padding: 20px; border-radius: 15px; font-size: 16px; color: #333;'>
                Imagine you're working on a biodegradable polymer for packaging.<br><br>
                You need one with low density and high flexibility.  
                Just enter the SMILES string and TransPolymer will predict its physical properties — instantly.
                </div>
                """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    @keyframes pulse {
        0% {transform: scale(1); opacity: 1;}
        50% {transform: scale(1.05); opacity: 0.8;}
        100% {transform: scale(1); opacity: 1;}
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 💡 Modern Footer
    st.markdown(""" 
    <div style="text-align: center; padding-top: 20px; font-size: 14px; color: #4B8BBE;">
        © 2025 TransPolymer • Powered by AI & Polymer Science
    </div>
    """, unsafe_allow_html=True)
