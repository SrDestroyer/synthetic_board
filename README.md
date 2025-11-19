# ⚡ Synthetic Board 3.0: Enterprise War Room

![Version](https://img.shields.io/badge/Version-3.0%20Enterprise-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-8E75B2?style=for-the-badge&logo=google)
![Audio](https://img.shields.io/badge/Audio-Neural%20TTS-green?style=for-the-badge)

> **Sistema de Soporte a la Decisión (DSS) Multi-Agente** que simula un Consejo Directivo Corporativo. Transforma problemas de negocio en estrategias accionables con análisis financiero, operativo y visión de mercado.

---

## 🧠 Capacidades SOTA (State-of-the-Art)

### 🚀 V3.0: Personalización y Multimodalidad
* **🎭 Agentes Editables:** Configura en tiempo real quiénes forman tu consejo (ej. *"Elon Musk"* como CEO, *"Warren Buffet"* como CFO).
* **🗣️ Interfaz de Voz (Jarvis):** El Presidente dicta la sentencia final mediante síntesis de voz neural (**gTTS**).
* **📄 Reportes Ejecutivos:** Generación automática de **PDFs Profesionales** con gráficos financieros incrustados (`Matplotlib` + `FPDF`).
* **📊 War Room Visual:** Los agentes no solo hablan; proyectan **gráficos de barras** basados en datos generados dinámicamente.

### 🏗️ Arquitectura Core
* **Map-Reduce Pattern:** Ejecución paralela de 3 roles (CEO, CFO, COO) + 1 Sintetizador (Presidente).
* **RAG-Lite:** Ingesta de archivos de contexto (`.txt`, `.csv`) para análisis basado en datos reales.
* **Persistencia de Estado:** Sesiones fluidas que no pierden datos al interactuar con la UI.
* **Blindaje Lingüístico:** Prompt Engineering avanzado para forzar respuestas estrictas en **Español, Inglés o Francés**.

---

## 🛠️ Instalación Local

### Prerrequisitos
* Python 3.10 o superior.
* Una API Key de [Google AI Studio](https://aistudio.google.com/).

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/TU_USUARIO/synthetic-board.git](https://github.com/TU_USUARIO/synthetic-board.git)
cd synthetic-board
2. Entorno Virtual
Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Instalar Dependencias
Bash

pip install -r requirements.txt
(Incluye: streamlit, google-genai, pandas, matplotlib, fpdf, gTTS)

4. Lanzar la War Room
Bash

streamlit run app.py
📂 Estructura del Proyecto
Plaintext

synthetic-board/
├── app.py               # Código Maestro (Monolito V3.0)
├── requirements.txt     # Dependencias de producción
├── README.md            # Documentación Oficial
└── .gitignore           # Configuración de seguridad git
🧪 Ejemplo de Uso (Flow)
Configuración (Sidebar):

Define al CEO como "Steve Jobs" (Enfoque: Diseño).

Selecciona idioma "Español".

Input: "Queremos eliminar el trabajo remoto para fomentar la creatividad."

Procesamiento:

CEO (Steve Jobs): Apoya la medida para interacción cara a cara.

CFO: Alerta sobre costos de oficina y riesgo de fuga de talento.

COO: Proyecta gráfico de caída de productividad transitoria.

Resolución (Presidente):

Emite un veredicto híbrido (3 días oficina / 2 remoto).

Audio: Escuchas la decisión.

PDF: Descargas el informe con el gráfico de costes del CFO.

🛡️ Seguridad & Privacidad
API Keys: Se procesan en memoria RAM y nunca se guardan en disco.

Archivos: Los documentos subidos y gráficos temporales se eliminan inmediatamente tras su uso (tempfile + os.unlink).

Desarrollado con 💻 por [Tu Nombre]


### 🚀 Último Push

Para que esto se refleje en tu GitHub:

1.  Copia el código de arriba en tu archivo `README.md`.
2.  Guarda.
3.  Ejecuta en la terminal:
    ```powershell
    git add README.md
    git commit -m "Docs: Update README to V3.0 Enterprise specs"
    git push
    ```