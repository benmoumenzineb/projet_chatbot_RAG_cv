import streamlit as st
from pipeline import reload_vector_store, answer_cv_only

#INTERFACE STREAMLIT

def run_streamlit_app():
    # Configuration de la page
    st.set_page_config(
        page_title="DocuMind - Assistant RAG sur CV",
        page_icon="📄",
        layout="wide"
    )
    
    # CSS 
    st.markdown("""
    <style>
        /* Fond général : dégradé de bleu ciel à blanc */
        .stApp {
            background: linear-gradient(135deg, #87CEEB 0%, #E0F7FA 100%);
        }
        
        /* ===== BARRE SUPÉRIEURE (HEADER) ===== */
        header[data-testid="stHeader"] {
            background: rgba(135, 206, 235, 0.6) !important;
            backdrop-filter: blur(8px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.4);
        }
        
        /* Supprimer le fond par défaut du header */
        .stApp > header {
            background-color: transparent !important;
        }
        
        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {
            background: rgba(135, 206, 235, 0.25) !important;
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(255, 255, 255, 0.5);
        }
        
        /* Contenu principal transparent */
        .main > div {
            background: transparent;
        }
        
        /* ===== TITRE ===== */
        .custom-title {
            text-align: center;
            padding: 1rem 0 0.5rem 0;
            margin-bottom: 1rem;
        }
        .custom-title h1 {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(120deg, #1E3A8A, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
            letter-spacing: -0.5px;
        }
        .custom-title p {
            color: #1E3A8A;
            font-size: 1.1rem;
            margin-top: 0.5rem;
            font-weight: 500;
        }
        
        /* ===== MESSAGES DU CHAT ===== */
        .stChatMessage {
            background: white !important;
            border-radius: 24px !important;
            padding: 12px 20px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
            border: 1px solid rgba(135, 206, 235, 0.5) !important;
            color: #1e293b !important;
        }
        
        /* ===== CHAMP DE SAISIE ===== */
        .stChatInputContainer {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 30px;
            padding: 8px;
            backdrop-filter: blur(5px);
            margin-bottom: 1rem;
        }
        .stChatInputContainer textarea {
            background: white !important;
            border-radius: 28px !important;
            color: #1e293b !important;
            border: 1px solid #87CEEB !important;
        }
        
        /* ===== TEXTES DANS LA SIDEBAR ===== */
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stText,
        section[data-testid="stSidebar"] .stSuccess,
        section[data-testid="stSidebar"] .stInfo,
        section[data-testid="stSidebar"] .stError {
            color: #0F172A !important;
            font-weight: 500;
        }
        
        /* ===== BOUTONS ===== */
        .stButton button {
            background: #3B82F6;
            color: white;
            border: none;
            border-radius: 30px;
            transition: 0.3s;
        }
        .stButton button:hover {
            background: #2563EB;
            transform: scale(1.02);
        }
        
        /* ===== UPLOADER (zone de dépôt) ===== */
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 20px;
            border: 2px dashed #3B82F6 !important;
            padding: 1rem;
        }
        .stFileUploader label {
            color: #1E3A8A !important;
            font-weight: 600;
        }
        /* Style du texte à l'intérieur du drag & drop */
        .stFileUploader div[data-testid="stFileUploadDropzone"] {
            background: rgba(255, 255, 255, 0.8) !important;
            border: none !important;
        }
        
        /* ===== EXPANDER DANS LA SIDEBAR ===== */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.7);
            color: #1E3A8A;
            border-radius: 15px;
        }
        
        /* ===== NOTIFICATIONS (success, info, error) ===== */
        .stAlert {
            background: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(4px);
            border-left: 4px solid #3B82F6;
            border-radius: 12px;
        }
        
        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            color: #1E3A8A;
            font-size: 0.8rem;
            padding: 1rem;
            margin-top: 2rem;
            background: rgba(255,255,255,0.5);
            border-radius: 30px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Titre stylisé en bleu
    st.markdown("""
    <div class="custom-title">
        <h1>📄 DocuMind</h1>
        <p>Posez vos questions, l'assistant analyse le contenu du CV</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar pour l'upload
    with st.sidebar:
        st.markdown("### 📂 Charger un CV")
        uploaded_file = st.file_uploader("Formats supportés : PDF, DOCX", type=["pdf", "docx"])
        
        if uploaded_file:
            st.success(f" CV chargé : {uploaded_file.name}")
            
            if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
                st.session_state.vector_store = reload_vector_store(uploaded_file)
                st.session_state.current_file = uploaded_file.name
                st.session_state.messages = []
                st.rerun()
        else:
            st.info("👈 Déposez votre CV (PDF/DOCX) pour commencer")
    
    # Gestion de l'historique de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Affichage des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Zone de saisie
    if "vector_store" in st.session_state:
        if question := st.chat_input("💬 Posez votre question sur le CV..."):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                with st.spinner("🔍 Analyse en cours..."):
                    response = answer_cv_only(question, st.session_state.vector_store)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.info("📄 Commencez par charger un CV dans la barre latérale pour interagir avec l'assistant.")
    
    # Footer
    st.markdown('<div class="footer">🤖 Assistant RAG — Analyse contextuelle de CV avec Gemini</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    run_streamlit_app()