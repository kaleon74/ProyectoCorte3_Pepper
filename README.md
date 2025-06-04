# 🤖 Pepper Chatbot - AK Watch
Sistema de chatbot inteligente implementado en el robot Pepper para consultas personalizadas de productos y comparativas de precios, potenciado por IA generativa.

> ## 🌟 Características Principales
* **Interacción Natural:** Conversación en español con reconocimiento de voz personalizado
* **Personalización Avanzada:** Experiencia adaptada usando el nombre del usuario
* **IA Generativa:** Análisis inteligente de productos usando Deepseek API
* **Arquitectura Distribuida:** Cliente Pepper + Servidor Flask + API Externa
* **Dominio Especializado:** Optimizado para relojería, joyería y audífonos

> ## 🏗️ Arquitectura del Sistema
![imagen](https://github.com/user-attachments/assets/e7b5e2c1-ace4-469f-b36c-7deeba25f83f)
    
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

> ## Instalación ⬇️

1. **Clonar el repositorio**
git clone https://github.com/tu-usuario/pepper-chatbot-akwatch.git
cd pepper-chatbot-akwatch
2. **Configurar el servidor**
pip install flask requests
3. **Configurar API Key**
**En serverdef4.py**
**API_KEY** = 'sk-53751d5c6f344a5dbc0571de9f51313e'
4. **Configurar IP del servidor**
**En pricesmap5.py**
**SERVER_IP** = "192.168.0.107"  # IP de tu PC

> ## Flujo de Conversación 💬
![imagen](https://github.com/user-attachments/assets/e1e3c94d-3378-47f0-9b94-7c5f8cca3fcb)

> ## Características Técnicas ⚙️
### Reconocimiento de Voz

* Vocabulario personalizado con 40+ términos específicos
* Umbral de confianza: >0.4
* Timeouts configurables por pregunta
* Manejo de errores y reintentos automáticos

### Servidor Flask

* API RESTful con 6 endpoints
* Gestión de estado de conversación
* Encoding UTF-8 para caracteres especiales
* Manejo robusto de errores HTTP

### Integración IA

* Prompt engineering personalizado
* Temperatura 0.85 para balance creatividad/precisión
*Respuestas de ~700 palabras
* Contexto de marca integrado
