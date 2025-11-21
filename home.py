import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
import login_page


def show():
    # Top-right Logout button
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.page = "Home"
            st.rerun()

    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(to right, #2c3e50, #3498db); height: 300px;">
        <h1 style="text-align:center; color:white; padding-top:100px; font-family: Arial; font-weight: bold;">🧬 TransPolymer</h1>
        <h3 style="text-align:center; color:white; font-family: Arial;">A Transformer-based AI Model for Polymer Property Predictions</h3>
    </div>
    """, unsafe_allow_html=True)

    # Typing Animation
    components.html("""
    <div style="display:flex; justify-content:center; align-items:center; height:120px;">
        <span id="typed-output" style="font-size:24px; color:white; font-family:Arial;"></span>
        <span id="cursor" style="font-size:24px; color:white; margin-left:2px;">|</span>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
    <script>
        const typed = new Typed('#typed-output', {
            strings: [
                "Predict Polymer Properties Instantly",
                "Powered by Transformers and Chemistry",
                "SMILES In, Predictions Out",
                "Design Better Polymers with AI",
                "Empowering Researchers through AI"
            ],
            typeSpeed: 50, backSpeed: 30, loop: true, showCursor: false
        });
        setInterval(() => {
            const cursor = document.getElementById("cursor");
            cursor.style.visibility = (cursor.style.visibility === "hidden") ? "visible" : "hidden";
        }, 500);
    </script>
    """, height=120)

    # Flip Cards
    st.markdown("""
    <style>
        .card-container { display: flex; justify-content: center; gap: 20px; margin-top: 50px; }
        .flip-card { width: 250px; height: 300px; perspective: 1000px; }
        .flip-card-inner { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; transition: transform 0.6s; }
        .flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
        .flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; padding: 20px; border-radius: 10px; }
        .flip-card-front { background-color: #ffffff; border: 2px solid #8e44ad; display: flex; justify-content: center; align-items: center; font-size: 20px; color: #8e44ad; font-family: 'Arial', sans-serif; font-weight: bold; }
        .flip-card-back { background-color: #8e44ad; color: white; transform: rotateY(180deg); text-align: center; font-family: 'Arial', sans-serif; }
        .flip-card-back h4 { color: #ffffff; }
        .flip-card-back p { color: #f1f1f1; font-size: 14px; }
    </style>
    <div class="card-container">
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">Polymer Property Prediction</div>
                <div class="flip-card-back"><h4>Polymer Property Prediction</h4><p>Using advanced AI models to make accurate and fast polymer property predictions.</p></div>
            </div>
        </div>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">SMILES Input</div>
                <div class="flip-card-back"><h4>SMILES Input</h4><p>TransPolymer works with SMILES strings to generate accurate predictions of polymer properties.</p></div>
            </div>
        </div>
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">Transformer Technology</div>
                <div class="flip-card-back"><h4>Transformer Technology</h4><p>Built on the powerful Transformer architecture .</p></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='
        padding: 25px;
        background: #fcf3cf;
        border-left: 6px solid #f39c12;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    '>
        <h4 style='color: #d35400; text-align: center; font-family: Arial;'>What is TransPolymer?</h4>
        <p style='color: #333; font-size: 16px; text-align: center; font-family: Arial;'>
            <strong style="color: #e67e22;">TransPolymer</strong> is a powerful AI assistant that predicts physical and chemical properties of polymers using deep learning techniques.<br>
            It transforms molecular SMILES strings into property insights within seconds.
        </p>
        <div style='display: flex; flex-direction: column; align-items: center;'>
            <ul style='color: #e67e22; font-size: 15px; list-style: none; padding-left: 0; text-align: left; font-family: Arial;'>
                <li>⚡ Fast predictions driven by Transformer architecture</li>
                <li>🔍 Supports polymer innovation and discovery</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Circular Layout
    components.html("""
    <style>
        .circle-container { position:relative; width:500px; height:500px; margin:40px auto; cursor:pointer; }
        .center-circle {
            width:180px; height:180px; background:#27ae60; border-radius:50%;
            position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
            display:flex; align-items:center; justify-content:center;
            color:#fff; font-size:14px; font-weight:bold; text-align:center;
            animation:pulse 2s infinite;
        }
        .property-circle {
            width:120px; height:120px; border-radius:50%;
            position:absolute; display:flex; align-items:center; justify-content:center;
            color:#fff; font-size:13px; font-weight:bold; text-align:center;
            visibility:hidden; opacity:0; transition:all 0.5s ease; padding:10px;
        }
        .circle-container.show .property-circle { visibility:visible; opacity:1; }
        .p1 { background:#1abc9c; top:10%; left:50%; transform:translate(-50%, -50%); }
        .p2 { background:#3498db; top:30%; left:85%; transform:translate(-50%, -50%); }
        .p3 { background:#9b59b6; top:70%; left:85%; transform:translate(-50%, -50%); }
        .p4 { background:#e67e22; top:90%; left:50%; transform:translate(-50%, -50%); }
        .p5 { background:#f39c12; top:70%; left:15%; transform:translate(-50%, -50%); }
        .p6 { background:#e74c3c; top:30%; left:15%; transform:translate(-50%, -50%); }
        @keyframes pulse {
            0%,100% { transform:translate(-50%, -50%) scale(1); }
            50% { transform:translate(-50%, -50%) scale(1.05); }
        }
    </style>
    <div class="circle-container" id="circleLayout" onclick="this.classList.add('show')">
        <div class="center-circle">Who Can Use TransPolymer?</div>
        <div class="property-circle p1">Polymer Scientists</div>
        <div class="property-circle p2">Drug Delivery Researchers</div>
        <div class="property-circle p3">Materials Scientists</div>
        <div class="property-circle p4">Optical Material Engineers</div>
        <div class="property-circle p5">Environmental Researchers</div>
        <div class="property-circle p6">Students in Chemistry</div>
    </div>
    """, height=600)

    # Footer
    st.markdown("""
    <div style="text-align:center; margin-top:50px;">
        <p style="color:#555; font-family:Arial;">Transpolymer - Simple. Smart. Scientific</p>
        <p style="color:#888; font-family:Arial; font-size:14px;">&copy; 2025 TransPolymer. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)