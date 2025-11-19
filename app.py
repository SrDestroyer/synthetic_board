import streamlit as st
from google import genai
from google.genai import types
from concurrent.futures import ThreadPoolExecutor
import time
import pandas as pd
import json
import re

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="Synthetic Board 2.0: War Room",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E; border-radius: 5px; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50; color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE AGENTES ---

def get_agent_response(role: str, focus: str, problem: str, context_file: str, api_key: str, language: str) -> dict:
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        ACT AS: {role} of a major corporation.
        PRIME DIRECTIVE: Focus exclusively on {focus}.
        
        CONTEXT FROM FILES: {context_file}
        INPUT PROBLEM: "{problem}"
        
        CRITICAL INSTRUCTION:
        You MUST respond in strict JSON format with the following structure keys:
        1. "analysis": (String) Your strategic analysis in {language}. Max 200 words. Use Markdown for formatting.
        2. "chart_title": (String) A title for a chart supporting your view in {language}.
        3. "chart_data": (Dictionary) Key-Value pairs for a bar chart (e.g., {{"Risk": 80, "Profit": 20}}). Values must be numeric.
        
        Output ONLY the JSON object. Do not wrap it in a list.
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7, 
                response_mime_type="application/json"
            )
        )
        
        try:
            data = json.loads(response.text)
            if isinstance(data, list):
                data = data[0] if len(data) > 0 else {"analysis": "⚠️ JSON vacío.", "chart_data": {}}
            if not isinstance(data, dict):
                return {"analysis": f"⚠️ Error formato: {type(data)}", "chart_data": {}}
            return data
            
        except json.JSONDecodeError:
            return {"analysis": "⚠️ Error decodificando JSON.", "chart_title": "Error", "chart_data": {}}
            
    except Exception as e:
        return {"analysis": f"⚠️ Error Crítico: {str(e)}", "chart_data": {}}

# --- UI PRINCIPAL ---

def main():
    # Inicializar Estado de Sesión para persistencia
    if "debate_data" not in st.session_state:
        st.session_state.debate_data = None
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""
    if "verdict" not in st.session_state:
        st.session_state.verdict = None

    # 1. SIDEBAR
    with st.sidebar:
        st.title("🎛️ Command Center")
        api_key = st.text_input("Google Gen AI API Key", type="password")
        st.markdown("---")
        uploaded_file = st.file_uploader("Subir datos (TXT, CSV, MD)", type=["txt", "csv", "md"])
        
        file_content = ""
        if uploaded_file is not None:
            try:
                file_content = uploaded_file.read().decode("utf-8")
                st.success(f"✅ {uploaded_file.name} indexado.")
            except:
                st.error("Error leyendo archivo.")

        selected_lang = st.selectbox("Idioma / Language", ["Español", "English", "Français"])
        
        # Botón de reinicio manual
        if st.button("🗑️ Resetear Sala de Guerra"):
            st.session_state.debate_data = None
            st.session_state.verdict = None
            st.rerun()

    # 2. HEADER
    st.title("⚡ Synthetic Board 2.0: War Room")
    
    # 3. INPUT (Lógica de Disparo)
    # Si el usuario escribe algo nuevo, disparamos el proceso y guardamos en session_state
    if prompt := st.chat_input("Escribe el desafío estratégico aquí..."):
        if not api_key:
            st.error("⛔ Falta API Key.")
            return
        
        st.session_state.current_prompt = prompt
        st.session_state.verdict = None # Limpiamos veredicto anterior

        # Ejecución de Agentes
        st.write(f"🧠 **Analizando:** '{prompt}'")
        
        agents = [
            {"role": "CEO (Visionario)", "focus": "Growth, Brand, Innovation", "icon": "🦁"},
            {"role": "CFO (Crítico)", "focus": "Cost, Risk, ROI, Audit", "icon": "💰"},
            {"role": "COO (Ejecutor)", "focus": "Logistics, Efficiency, Ops", "icon": "⚙️"}
        ]
        
        temp_results = {}
        with st.spinner("🔄 Los agentes están generando simulaciones gráficas..."):
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(get_agent_response, a["role"], a["focus"], prompt, file_content, api_key, selected_lang): a 
                    for a in agents
                }
                for future in futures:
                    agent_meta = futures[future]
                    temp_results[agent_meta["role"]] = future.result()
        
        # GUARDAMOS EN ESTADO PERSISTENTE
        st.session_state.debate_data = temp_results
        st.rerun() # Recargamos para mostrar los resultados limpios

    # 4. RENDERIZADO (Solo si hay datos en memoria)
    if st.session_state.debate_data:
        
        st.info(f"📋 Desafío Actual: **{st.session_state.current_prompt}**")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🦁 CEO", "💰 CFO", "⚙️ COO", "⚖️ Presidente"])

        def render_agent_tab(tab, agent_role, data):
            with tab:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader(f"Análisis del {agent_role}")
                    st.markdown(data.get("analysis", "Sin datos"))
                with col2:
                    st.subheader("📊 Proyección")
                    st.caption(data.get("chart_title", "Métricas"))
                    chart_data = data.get("chart_data", {})
                    if chart_data:
                        df = pd.DataFrame(list(chart_data.items()), columns=["Concepto", "Valor"])
                        st.bar_chart(df.set_index("Concepto"))
                    else:
                        st.warning("No hay datos gráficos.")

        results = st.session_state.debate_data
        render_agent_tab(tab1, "CEO (Visionario)", results["CEO (Visionario)"])
        render_agent_tab(tab2, "CFO (Crítico)", results["CFO (Crítico)"])
        render_agent_tab(tab3, "COO (Ejecutor)", results["COO (Ejecutor)"])

        # 5. LOGICA DEL PRESIDENTE (Ahora fuera del bloque chat_input)
        with tab4:
            st.header("👨‍⚖️ Veredicto Final")
            
            # Si ya hay veredicto guardado, lo mostramos
            if st.session_state.verdict:
                st.success("Dictamen Emitido:")
                st.markdown(st.session_state.verdict)
                if st.button("🔄 Re-evaluar"):
                    st.session_state.verdict = None
                    st.rerun()
            else:
                # Si no, mostramos el botón para generarlo
                if st.button("🔨 Emitir Sentencia Vinculante"):
                    if not api_key:
                        st.error("Falta API Key")
                    else:
                        with st.spinner("El Presidente está deliberando..."):
                            client = genai.Client(api_key=api_key)
                            debate_context = json.dumps(st.session_state.debate_data)
                            
                            final_prompt = f"""
                            ACT AS: Chairman of the Board.
                            INPUT: Review JSON analysis from CEO, CFO, COO: {debate_context}
                            PROBLEM: {st.session_state.current_prompt}
                            LANGUAGE: {selected_lang}
                            OUTPUT: A Markdown summary of the decision. Be authoritative.
                            """
                            
                            response = client.models.generate_content(
                                model="gemini-2.0-flash",
                                contents=final_prompt
                            )
                            
                            # Guardamos el veredicto en estado y recargamos
                            st.session_state.verdict = response.text
                            st.rerun()

if __name__ == "__main__":
    main()