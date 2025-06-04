# 🤖 Pepper Chatbot - AK Watch
Sistema de chatbot inteligente implementado en el robot Pepper para consultas personalizadas de productos y comparativas de precios, potenciado por IA generativa.

> ## 🌟 Características Principales
* **Interacción Natural:** Conversación en español con reconocimiento de voz personalizado
* **Personalización Avanzada:** Experiencia adaptada usando el nombre del usuario
* **IA Generativa:** Análisis inteligente de productos usando Deepseek API
* **Arquitectura Distribuida:** Cliente Pepper + Servidor Flask + API Externa
* **Dominio Especializado:** Optimizado para relojería, joyería y audífonos

> ## 🏗️ Arquitectura del Sistema
┌─────────────────────────────────────────────────────────────────┐
│                    PEPPER CHATBOT SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────────────────────────────────────┐
         │                                                         │
         ▼                                                         │
┌─────────────────┐     HTTP/JSON      ┌─────────────────┐         │
│   🤖 PEPPER     │◄──────────────────►│  🖥️ FLASK       │         │
│                 │                    │                 │         │
│ • Speech Recog  │   GET /pregunta    │ • Conversation  │         │
│ • Text to Speech│   POST /respuesta  │ • State Mgmt    │         │
│ • Memory Mgmt   │   GET /resultado   │ • API Routes    │         │
│                 │                    │                 │         │
└─────────────────┘                    └─────────────────┘         │
         ▲                                       │                 │
         │                                       │ HTTPS           │
         │              ┌─────────────────┐      │                 │
         │              │   🧠 DEEPSEEK   │◄─────┘                 │
         │              │                 │                       │
         └──────────────│ • LLM Analysis  │                       │
           Resultado    │ • Prompt Eng    │                       │
           Personalizado│ • 700+ words    │                       │
                        │                 │                       │
                        └─────────────────┘                       │
                                   ▲                              │
                                   └──────────────────────────────┘
    
> ## Componentes

* **pricesmap5.py:** Cliente Pepper con reconocimiento de voz y síntesis de habla
* **serverdef4.py:** Servidor Flask para gestión de conversaciones y API
* **Deepseek API:** Motor de IA para generación de análisis personalizados

> ## 🚀 Instalación y Configuración
**Prerrequisitos**

* Robot Pepper con NAOqi 2.x
* Python 2.7 (compatible con NAOqi)
* Acceso a red local WiFi
* API Key de Deepseek
