# ⚡ Synthetic Board: AI Decision Architect

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-8E75B2?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Arquitectura Multi-Agente (SOTA)** que simula un Consejo Directivo Corporativo para la toma de decisiones estratégicas complejas.

---

## 🧠 Sobre el Proyecto

**Synthetic Board** no es un chatbot estándar. Es un sistema de orquestación de agentes que utiliza el patrón **Map-Reduce (Fan-Out/Fan-In)** para descomponer problemas de negocio.

El sistema convoca a tres perfiles de IA especializados (CEO, CFO, COO) que analizan el problema en paralelo. Posteriormente, un cuarto agente ("El Presidente") agrega el contexto completo, evalúa los conflictos y emite un veredicto vinculante.

### ✨ Características Clave
* **🚀 Motor SOTA:** Impulsado por **Gemini 2.0 Flash**, aprovechando baja latencia y razonamiento avanzado.
* **⚡ Ejecución Paralela:** Implementación de `ThreadPoolExecutor` para reducir la latencia de respuesta en un 60% (vs. ejecución secuencial).
* **🎭 Personas Estrictas:** Prompt Engineering avanzado para asegurar que el CFO priorice finanzas y el CEO la visión, generando conflicto constructivo real.
* **⚖️ Síntesis Agéntica:** Un meta-agente lee las posturas anteriores y genera una conclusión unificada (Hegelian Dialectic Synthesis).
* **🔐 Seguridad:** Manejo de API Keys en memoria (Session State), sin almacenamiento en disco.

---

## 🏗️ Arquitectura del Sistema

El flujo de datos sigue un patrón de **Decision Pipeline**:

```mermaid
graph TD
    User[👤 User Input] -->|Business Problem| Dispatcher{⚡ Task Dispatcher}
    
    subgraph "Parallel Agent Processing (Map Phase)"
        Dispatcher -->|Thread 1| CEO[🦁 CEO Agent<br>Vision & Growth]
        Dispatcher -->|Thread 2| CFO[💰 CFO Agent<br>Risk & Budget]
        Dispatcher -->|Thread 3| COO[⚙️ COO Agent<br>Ops & Logistics]
    end
    
    CEO --> Aggregator[📥 Context Aggregation]
    CFO --> Aggregator
    COO --> Aggregator
    
    subgraph "Synthesis (Reduce Phase)"
        Aggregator -->|Full Debate Log| Chairman[👨‍⚖️ The Chairman<br>Final Verdict & KPIs]
    end
    
    Chairman --> UI[🖥️ Streamlit Interface]
🛠️ Instalación y Uso Local
Prerrequisitos
Python 3.10 o superior.

Una API Key de Google AI Studio.

1. Clonar el Repositorio
Bash

git clone [https://github.com/tu-usuario/synthetic-board.git](https://github.com/tu-usuario/synthetic-board.git)
cd synthetic-board
2. Configurar Entorno Virtual
Se recomienda aislar las dependencias:

Windows:

PowerShell

python -m venv venv
.\venv\Scripts\activate
Mac/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
3. Instalar Dependencias
Bash

pip install -r requirements.txt
4. Ejecutar Aplicación
Bash

streamlit run app.py
📂 Estructura del Proyecto
Plaintext

synthetic-board/
├── app.py               # Lógica Core (UI + Orquestación Agentes)
├── requirements.txt     # Dependencias (streamlit, google-genai)
└── README.md            # Documentación
🧪 Ejemplo de Uso
Input del Usuario:

"Queremos implementar una semana laboral de 4 días manteniendo el 100% del salario."

Respuesta del Sistema:

CEO: Aprueba por impacto en marca y atracción de talento.

CFO: Rechaza rotundamente por impacto en márgenes y coste unitario.

COO: Solicita análisis de turnos y advierte sobre caída de soporte al cliente.

PRESIDENTE: Dictamina realizar un Programa Piloto A/B en un departamento no crítico durante 3 meses antes de decidir.

🛡️ Disclaimer
Este proyecto utiliza Modelos de Lenguaje Grande (LLMs). Las decisiones estratégicas reales deben ser validadas por profesionales humanos.

Built with 💻 by [Fco.JavierPradoGuerrero]