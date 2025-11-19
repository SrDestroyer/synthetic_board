import streamlit as st
from google import genai
from google.genai import types
from concurrent.futures import ThreadPoolExecutor
import time
import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import io
import tempfile
import os
from fpdf import FPDF

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="Synthetic Board 2.1: War Room",
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
    .stChatMessage {border: 1px solid #444; border-radius: 10px;}
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

# --- MOTOR DE VISUALIZACIÓN & REPORTES SOTA ---

def generate_chart_image(chart_data, title, color_hex):
    """Genera un gráfico de barras moderno en memoria (BytesIO)"""
    if not chart_data:
        return None
    
    try:
        # Configuración de estilo limpio
        plt.style.use('seaborn-v0_8-darkgrid') 
        fig, ax = plt.subplots(figsize=(6, 3.5))
        
        # Extraer datos
        categories = list(chart_data.keys())
        values = list(chart_data.values())
        
        # Crear barras con el color del agente
        bars = ax.bar(categories, values, color=color_hex, alpha=0.8)
        
        # Estética
        ax.set_title(title, fontsize=12, fontweight='bold', color='#333333')
        ax.tick_params(axis='x', rotation=15, colors='#555555')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Añadir valores
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)
        img_buffer.seek(0)
        return img_buffer
    except Exception as e:
        return None

def create_pdf(prompt, debate_data, verdict, language):
    class ModernPDF(FPDF):
        def header(self):
            self.set_fill_color(30, 30, 30)
            self.rect(0, 0, 210, 25, 'F')
            self.set_font('Arial', 'B', 16)
            self.set_text_color(255, 255, 255)
            self.set_xy(10, 8)
            self.cell(0, 10, 'SYNTHETIC BOARD // WAR ROOM REPORT', 0, 0, 'L')
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'AI Generated Strategy | Page {self.page_no()}', 0, 0, 'C')
            
        def section_title(self, label, color_rgb):
            self.set_fill_color(*color_rgb)
            self.rect(10, self.get_y(), 190, 8, 'F')
            self.set_font('Arial', 'B', 12)
            self.set_text_color(255, 255, 255)
            self.set_xy(12, self.get_y() + 1)
            self.cell(0, 6, label, 0, 1, 'L')
            self.ln(4)
            self.set_text_color(0, 0, 0)

    pdf = ModernPDF()
    pdf.add_page()
    
    def safe_text(text):
        if not text: return ""
        return text.encode('latin-1', 'replace').decode('latin-1')

    # 1. RESUMEN EJECUTIVO
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "MISSION OBJECTIVE (INPUT):", 0, 1)
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, safe_text(prompt))
    pdf.ln(8)

    # 2. ANÁLISIS DE AGENTES
    if debate_data:
        agent_configs = {
            "CEO (Visionario)": {"color": (255, 75, 75), "hex": "#FF4B4B"},
            "CFO (Crítico)": {"color": (255, 165, 0), "hex": "#FFA500"},
            "COO (Ejecutor)": {"color": (0, 212, 255), "hex": "#00D4FF"}
        }

        for role, data in debate_data.items():
            config = agent_configs.get(role, {"color": (100, 100, 100), "hex": "#666666"})
            
            pdf.section_title(safe_text(role.upper()), config["color"])
            
            pdf.set_font("Arial", size=10)
            analysis_text = safe_text(data.get("analysis", "No data"))
            pdf.multi_cell(0, 5, analysis_text)
            pdf.ln(3)
            
            # --- TRON FIX: Manejo seguro de imágenes temporales ---
            chart_data = data.get("chart_data", {})
            if chart_data:
                try:
                    img_stream = generate_chart_image(
                        chart_data, 
                        data.get("chart_title", "Metrics"), 
                        config["hex"]
                    )
                    if img_stream:
                        # Creamos un archivo temporal físico para que FPDF no falle
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                            tmpfile.write(img_stream.getvalue())
                            tmp_filename = tmpfile.name
                        
                        # Insertamos usando la ruta del archivo
                        pdf.image(tmp_filename, x=55, w=100)
                        pdf.ln(5)
                        
                        # Limpieza inmediata
                        os.unlink(tmp_filename)
                        
                except Exception as e:
                    pdf.set_font("Courier", size=8)
                    pdf.cell(0, 5, f"[Chart Error: {safe_text(str(e))}]", 0, 1)
            
            pdf.ln(5)

    # 3. VEREDICTO FINAL
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 25, 210, 5, 'F')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "FINAL BINDING VERDICT", 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, safe_text(verdict), fill=True)
    
    pdf.set_y(-40)
    pdf.line(20, 270, 80, 270)
    pdf.line(130, 270, 190, 270)
    pdf.set_font("Arial", 'I', 8)
    pdf.text(20, 275, "Digitally Signed: The Chairman")
    pdf.text(130, 275, f"Date: {safe_text(language)}")

    return pdf.output(dest='S').encode('latin-1')

# --- UI PRINCIPAL ---

def main():
    if "debate_data" not in st.session_state:
        st.session_state.debate_data = None
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""
    if "verdict" not in st.session_state:
        st.session_state.verdict = None

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
        
        if st.button("🗑️ Resetear Sala de Guerra"):
            st.session_state.debate_data = None
            st.session_state.verdict = None
            st.rerun()

    st.title("⚡ Synthetic Board 2.1: War Room")
    
    if prompt := st.chat_input("Escribe el desafío estratégico aquí..."):
        if not api_key:
            st.error("⛔ Falta API Key.")
            return
        
        st.session_state.current_prompt = prompt
        st.session_state.verdict = None 

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
        
        st.session_state.debate_data = temp_results
        st.rerun() 

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

        with tab4:
            st.header("👨‍⚖️ Veredicto Final")
            
            if st.session_state.verdict:
                st.success("Dictamen Emitido:")
                st.markdown(st.session_state.verdict)
                
                with st.spinner("📄 Generando Informe Oficial con Gráficos..."):
                    try:
                        pdf_bytes = create_pdf(
                            st.session_state.current_prompt,
                            st.session_state.debate_data,
                            st.session_state.verdict,
                            selected_lang
                        )
                        
                        st.download_button(
                            label="📄 Descargar Informe Oficial (PDF)",
                            data=pdf_bytes,
                            file_name="synthetic_board_report.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error generando PDF: {str(e)}")
                
                if st.button("🔄 Re-evaluar"):
                    st.session_state.verdict = None
                    st.rerun()
            else:
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
                            
                            st.session_state.verdict = response.text
                            st.rerun()

if __name__ == "__main__":
    main()