import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import joblib
from transformers import AutoTokenizer, AutoModel
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, Draw
from datetime import datetime
from db import get_database
import random
import pandas as pd
import time
import base64
from io import BytesIO

# Set seeds
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Page styling and configuration
st.set_page_config(
    page_title="Polymer Property Prediction",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2E7D32;
        margin-bottom: 0.5rem;
    }
    .property-card {
        background-color: #f1f8e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
    }
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .loader {
        border: 16px solid #f3f3f3;
        border-radius: 50%;
        border-top: 16px solid #3498db;
        width: 50px;
        height: 50px;
        animation: spin 2s linear infinite;
        margin: 20px auto;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load ChemBERTa
@st.cache_resource
def load_chemberta():
    with st.spinner("Loading ChemBERTa model..."):
        tokenizer = AutoTokenizer.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")
        model = AutoModel.from_pretrained("seyonec/ChemBERTa-zinc-base-v1").to(device).eval()
    return tokenizer, model

# Load scalers
@st.cache_resource
def load_scalers():
    return {
        "Tensile Strength (MPa)": joblib.load("scaler_Tensile_strength_Mpa_.joblib"),
        "Ionization Energy (eV)": joblib.load("scaler_Ionization_Energy_eV_.joblib"),
        "Electron Affinity (eV)": joblib.load("scaler_Electron_Affinity_eV_.joblib"),
        "logP": joblib.load("scaler_LogP.joblib"),
        "Refractive Index": joblib.load("scaler_Refractive_Index.joblib"),
        "Molecular Weight (g/mol)": joblib.load("scaler_Molecular_Weight_g_mol_.joblib")
    }

# Transformer model
class TransformerRegressor(nn.Module):
    def __init__(self, feat_dim=2058, embedding_dim=768, ff_dim=1024, num_layers=2, output_dim=6):
        super().__init__()
        self.feat_proj = nn.Linear(feat_dim, embedding_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim, nhead=8, dim_feedforward=ff_dim,
            dropout=0.1, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.regression_head = nn.Sequential(
            nn.Linear(embedding_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )

    def forward(self, x, feat):
        feat_emb = self.feat_proj(feat)
        stacked = torch.stack([x, feat_emb], dim=1)
        encoded = self.transformer_encoder(stacked)
        aggregated = encoded.mean(dim=1)
        return self.regression_head(aggregated)

# Load model
@st.cache_resource
def load_model():
    with st.spinner("Loading prediction model..."):
        model = TransformerRegressor()
        try:
            state_dict = torch.load("transformer_model.bin", map_location=device)
            model.load_state_dict(state_dict)
            model.eval().to(device)
        except Exception as e:
            raise ValueError(f"Failed to load model: {e}")
    return model

# RDKit descriptors
def compute_descriptors(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string.")
    desc = [
        Descriptors.MolWt(mol),
        Descriptors.MolLogP(mol),
        Descriptors.TPSA(mol),
        Descriptors.NumRotatableBonds(mol),
        Descriptors.NumHDonors(mol),
        Descriptors.NumHAcceptors(mol),
        Descriptors.FractionCSP3(mol),
        Descriptors.HeavyAtomCount(mol),
        Descriptors.RingCount(mol),
        Descriptors.MolMR(mol)
    ]
    return np.array(desc, dtype=np.float32)

# Morgan fingerprint
def get_morgan_fingerprint(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string.")
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    return np.array(fp, dtype=np.float32).reshape(1, -1)

# ChemBERTa embedding
def get_chemberta_embedding(smiles: str, tokenizer, chemberta):
    inputs = tokenizer(smiles, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = chemberta(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

# Save to DB
def save_to_db(smiles, predictions, mol_image=None):
    predictions_clean = {k: float(v) for k, v in predictions.items()}
    doc = {
        "smiles": smiles,
        "predictions": predictions_clean,
        "timestamp": datetime.now()
    }
    if mol_image:
        doc["molecule_image"] = mol_image
    
    db = get_database()
    db["polymer_predictions"].insert_one(doc)
    return doc["_id"]

# Get molecule image as base64
def get_molecule_image(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        img = Draw.MolToImage(mol, size=(300, 300))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

# Removed example SMILES

# Get history from database
def get_prediction_history(limit=5):
    db = get_database()
    history = list(db["polymer_predictions"].find().sort("timestamp", -1).limit(limit))
    return history

# Sidebar
def show_sidebar():
    st.sidebar.markdown("<div class='sub-header'>About This Tool</div>", unsafe_allow_html=True)
    st.sidebar.info("""
    This tool predicts key properties of polymers based on their SMILES representation.
    
    It uses a transformer neural network combined with ChemBERTa embeddings and molecular descriptors.
    """)
    
    st.sidebar.markdown("<div class='sub-header'>Property Explanations</div>", unsafe_allow_html=True)
    
    with st.sidebar.expander("Tensile Strength"):
        st.write("""
        **Tensile Strength (MPa)** measures the maximum stress a material can withstand before breaking.
        Higher values indicate stronger materials.
        """)
    
    with st.sidebar.expander("Ionization Energy"):
        st.write("""
        **Ionization Energy (eV)** is the energy required to remove an electron from an atom or molecule.
        It affects chemical reactivity and stability.
        """)
        
    with st.sidebar.expander("Electron Affinity"):
        st.write("""
        **Electron Affinity (eV)** measures how much energy is released when an electron is added to a neutral atom.
        It influences a polymer's electrical properties.
        """)
        
    with st.sidebar.expander("logP"):
        st.write("""
        **logP** is the partition coefficient that measures how a substance distributes between water and lipid phases.
        It affects solubility and permeability of polymers.
        """)
        
    with st.sidebar.expander("Refractive Index"):
        st.write("""
        **Refractive Index** measures how light propagates through the material.
        It's important for optical applications of polymers.
        """)
        
    with st.sidebar.expander("Molecular Weight"):
        st.write("""
        **Molecular Weight (g/mol)** is the mass of a molecule.
        It affects mechanical properties, processability, and many other characteristics.
        """)
    
    st.sidebar.markdown("<div class='sub-header'>Recent Predictions</div>", unsafe_allow_html=True)
    history = get_prediction_history(5)
    if history:
        for i, item in enumerate(history):
            smiles = item["smiles"]
            timestamp = item["timestamp"].strftime("%Y-%m-%d %H:%M")
            with st.sidebar.expander(f"#{i+1}: {smiles[:15]}... ({timestamp})"):
                st.code(smiles, language="text")
                for prop, val in item["predictions"].items():
                    st.write(f"**{prop}**: {val:.4f}")
    else:
        st.sidebar.write("No prediction history available.")

# Example SMILES section removed

# Property visualization
def visualize_properties(results):
    st.markdown("<div class='sub-header'>Property Visualization</div>", unsafe_allow_html=True)
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame([results])
    
    # Normalize values for radar chart
    property_ranges = {
        "Tensile Strength (MPa)": (0, 200),
        "Ionization Energy (eV)": (5, 15),
        "Electron Affinity (eV)": (0, 5),
        "logP": (-5, 10),
        "Refractive Index": (1, 2),
        "Molecular Weight (g/mol)": (0, 5000)
    }
    
    normalized_values = {}
    for prop, value in results.items():
        min_val, max_val = property_ranges.get(prop, (0, 1))
        normalized = (value - min_val) / (max_val - min_val)
        normalized_values[prop] = max(0, min(normalized, 1))  # Clamp between 0 and 1
    
    # Display as gauge charts
    cols = st.columns(3)
    for i, (prop, norm_val) in enumerate(normalized_values.items()):
        with cols[i % 3]:
            st.markdown(f"<div class='property-card'>", unsafe_allow_html=True)
            st.markdown(f"<h4>{prop}</h4>", unsafe_allow_html=True)
            # Ensure the value is a float between 0 and 1
            st.progress(float(norm_val))
            st.markdown(f"<h3 style='text-align: center;'>{results[prop]:.4f}</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a bar chart comparing the properties
    normalized_df = pd.DataFrame({
        'Property': list(normalized_values.keys()),
        'Normalized Value': list(normalized_values.values()),
        'Actual Value': [results[prop] for prop in normalized_values.keys()]
    })
    
    st.bar_chart(normalized_df.set_index('Property')['Normalized Value'])

# Main function
def show():
    # Initialize session state for SMILES input
    if 'smiles_input' not in st.session_state:
        st.session_state.smiles_input = ""
    
    # Main header
    st.markdown("<div class='main-header'>🧪 Polymer Property Prediction</div>", unsafe_allow_html=True)
    
    # Sidebar
    show_sidebar()
    
    # Input section
    st.markdown("<div class='sub-header'>Input Your Polymer</div>", unsafe_allow_html=True)
    
    # SMILES input with example dropdown
    col1, col2 = st.columns([3, 1])
    with col1:
        smiles_input = st.text_input("Enter SMILES Representation", 
                                      value=st.session_state.smiles_input,
                                      help="SMILES (Simplified Molecular Input Line Entry System) is a notation representing molecular structure.")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear", key="clear_button"):
            st.session_state.smiles_input = ""
    

    # Input validation
    is_valid = False
    if smiles_input:
        mol = Chem.MolFromSmiles(smiles_input)
        is_valid = mol is not None
        
        if is_valid:
            st.session_state.smiles_input = smiles_input
            col1, col2 = st.columns([1, 2])
            with col1:
                mol_img = get_molecule_image(smiles_input)
                if mol_img:
                    st.markdown(f"<img src='data:image/png;base64,{mol_img}' style='max-width:100%;'>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.markdown("### Molecule Properties")
                st.write(f"**Formula:** {Chem.rdMolDescriptors.CalcMolFormula(mol)}")
                st.write(f"**Rings:** {Descriptors.RingCount(mol)}")
                st.write(f"**H-Bond Donors:** {Descriptors.NumHDonors(mol)}")
                st.write(f"**H-Bond Acceptors:** {Descriptors.NumHAcceptors(mol)}")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Invalid SMILES string. Please check your input.")
    
    # Prediction button
    run_prediction = st.button("🔍 Predict Properties", disabled=not is_valid, key="predict_button")
    
    if run_prediction:
        try:
            # Load resources with progress indication
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Load models
            status_text.text("Loading models...")
            model = load_model()
            tokenizer, chemberta = load_chemberta()
            scalers = load_scalers()
            progress_bar.progress(0.25)  # Ensure float value between 0 and 1
            time.sleep(0.5)  # Simulate processing time for better UX
            
            # Step 2: Compute molecular features
            status_text.text("Computing molecular features...")
            descriptors = compute_descriptors(smiles_input)
            descriptors_tensor = torch.tensor(descriptors, dtype=torch.float32).unsqueeze(0)
            fingerprint = get_morgan_fingerprint(smiles_input)
            fingerprint_tensor = torch.tensor(fingerprint, dtype=torch.float32)
            features = torch.cat([descriptors_tensor, fingerprint_tensor], dim=1).to(device)
            progress_bar.progress(0.50)  # Ensure float value between 0 and 1
            time.sleep(0.5)  # Simulate processing time
            
            # Step 3: Generate embeddings
            status_text.text("Generating ChemBERTa embeddings...")
            embedding = get_chemberta_embedding(smiles_input, tokenizer, chemberta)
            progress_bar.progress(0.75)  # Ensure float value between 0 and 1
            time.sleep(0.5)  # Simulate processing time
            
            # Step 4: Make predictions
            status_text.text("Making predictions...")
            with torch.no_grad():
                preds = model(embedding, features)
            
            preds_np = preds.cpu().numpy()
            keys = list(scalers.keys())
            preds_rescaled = np.concatenate([
                scalers[keys[i]].inverse_transform(preds_np[:, [i]])
                for i in range(6)
            ], axis=1)
            
            results = {key: val for key, val in zip(keys, preds_rescaled.flatten())}
            progress_bar.progress(1.0)  # Ensure float value between 0 and 1
            status_text.empty()
            
            # Save to database
            mol_img = get_molecule_image(smiles_input)
            save_to_db(smiles_input, results, mol_img)
            
            # Display results
            st.success("✅ Prediction completed successfully!")
            
            # Visualize results
            visualize_properties(results)
            
            # Detailed results in expandable section
            with st.expander("View Detailed Results"):
                result_df = pd.DataFrame({
                    'Property': list(results.keys()),
                    'Predicted Value': [f"{val:.4f}" for val in results.values()]
                })
                st.table(result_df)
                
                # Export options
                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name=f"polymer_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
            st.code(str(e))
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #ccc; color: #666;">
        <p>Polymer Property Prediction Tool - © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()