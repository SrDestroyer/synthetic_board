import streamlit as st
from google import genai
from google.genai import types
from concurrent.futures import ThreadPoolExecutor
import time

# --- TRON ARCHITECTURE: CONFIG & SETUP ---
st.set_page_config(
    page_title="Synthetic Board: AI Decision Architect",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS inyectados para una estética Cyberpunk/Tech limpia
st.markdown("""
    <style>
    .stChatMessage {border: 1px solid #444; border-radius: 10px;}
    .agent-card {padding: 15px; border-radius: 8px; background-color: #1E1E1E; border-left: 4px solid;}
    </style>
""", unsafe_allow_html=True)

# --- LOGIC CORE: AGENT ORCHESTRATION ---

def get_agent_response(role: str, focus: str, problem: str, api_key: str, language: str) -> str:
    try:
        client = genai.Client(api_key=api_key)
        
        # INYECCIÓN DE IDIOMA: Mantenemos la lógica en inglés para precisión,
        # pero forzamos la salida al idioma seleccionado.
        prompt = f"""
        ACT AS: {role} of a major corporation.
        PRIME DIRECTIVE: Focus exclusively on {focus}.
        INPUT: The user presents the following business problem: "{problem}"
        
        CRITICAL OUTPUT INSTRUCTION: 
        You MUST respond strictly in the following language: {language}.
        Do not mix languages. Translate your professional persona to {language}.
        
        OUTPUT: Provide a concise, high-impact strategic analysis (max 150 words).
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8, 
                max_output_tokens=500 # Aumentado un poco para idiomas verbosos
            )
        )
        
        if response.text:
            return response.text
        else:
            return f"⚠️ Respuesta vacía ({role}). Intente de nuevo."
            
    except Exception as e:
        return f"⚠️ **Error de Conexión:** {str(e)}"

# --- UI LAYER: REACTIVE INTERFACE ---

def main():
    # 1. Sidebar: Security & Config
    with st.sidebar:
        st.title("🔐 Secure Gateway")
        api_key = st.text_input("Google Gen AI API Key", type="password", help="Tu llave no se guarda.")
        
        st.markdown("---")
        st.subheader("🌐 Configuración Global")
        
        # SELECTOR DE IDIOMA (Top 5 + Bonus)
        selected_lang = st.selectbox(
            "Idioma de Respuesta / Language",
            ["Español", "English", "中文 (Chinese Mandarin)", "हिन्दी (Hindi)", "العربية (Arabic)", "Français"]
        )
        
        st.markdown("---")
        st.caption(f"Mode: {selected_lang}")
        st.caption("Engine: Gemini 2.0 Flash")

    # 2. Main Header
    st.title("⚡ Synthetic Board: AI Decision Architect")
    st.markdown(f"Presenta tu desafío. El Consejo debatirá en **{selected_lang}**.")

    # 3. Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. Input Logic
    if prompt := st.chat_input("Describe tu situación estratégica..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:
            st.error("⛔ Alerta: Inserte su API Key en el menú lateral.")
            return

        with st.chat_message("assistant"):
            st.write(f"🔄 Convocando al Consejo en {selected_lang}...")
            
            agents = [
                {"role": "CEO (Visionario)", "focus": "Growth, Brand, Long-term Vision, Disruption", "color": "#FF4B4B"},
                {"role": "CFO (Crítico)", "focus": "Risk Management, Cash Flow, Audit, Profitability", "color": "#FFA500"},
                {"role": "COO (Ejecutor)", "focus": "Logistics, Processes, Efficiency, Execution", "color": "#00D4FF"}
            ]

            results = []
            start_time = time.time()
            
            # PASAMOS EL IDIOMA A LOS HILOS
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(get_agent_response, agent["role"], agent["focus"], prompt, api_key, selected_lang): agent 
                    for agent in agents
                }
                
                for future in futures:
                    agent_info = futures[future]
                    try:
                        text = future.result()
                        results.append({"role": agent_info["role"], "text": text, "color": agent_info["color"]})
                    except Exception as exc:
                        results.append({"role": agent_info["role"], "text": f"Error: {exc}", "color": "#FF0000"})

            latency = time.time() - start_time
            st.caption(f"⚡ Consejo reunido en {latency:.2f}s")

            cols = st.columns(3)
            full_response_log = ""
            
            for idx, col in enumerate(cols):
                res = results[idx] 
                with col:
                    st.markdown(f"<div style='border-bottom: 3px solid {res['color']}; margin-bottom: 10px;'><b>{res['role']}</b></div>", unsafe_allow_html=True)
                    st.markdown(res["text"])
                    full_response_log += f"**{res['role']} ({selected_lang}):**\n{res['text']}\n\n"

            st.session_state.messages.append({"role": "assistant", "content": full_response_log})

            # --- FASE 2: PRESIDENTE MULTILINGÜE ---
            st.markdown("---")
            st.subheader("⚖️ Resolución Vinculante")
            
            with st.status("🧠 Sintetizando posturas...", expanded=True) as status:
                st.write("📥 Analizando conflicto...")
                
                board_debate_log = f"""
                PROBLEM: {prompt}
                LANGUAGE CONTEXT: {selected_lang}
                OPINION CEO: {results[0]['text']}
                OPINION CFO: {results[1]['text']}
                OPINION COO: {results[2]['text']}
                """
                
                verdict = get_agent_response(
                    role="Presidente del Consejo (The Chairman)",
                    focus="Synthesize arguments, make a FINAL binding decision. Be authoritative.",
                    problem=board_debate_log,
                    api_key=api_key,
                    language=selected_lang # <-- El Presidente también habla el idioma
                )
                
                status.update(label="✅ Dictamen Finalizado", state="complete", expanded=False)

            st.info(f"**DICTAMEN FINAL:**\n\n{verdict}", icon="👨‍⚖️")
            st.session_state.messages.append({"role": "assistant", "content": f"**VEREDICTO:**\n{verdict}"})

if __name__ == "__main__":
    main()