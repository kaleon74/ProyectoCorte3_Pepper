# -*- coding: utf-8 -*-
# pepper_cliente_chatbot.py

import qi
import time
import httplib
import json

SERVER_IP = "192.168.0.107"  #  IP de tu PC
SERVER_PORT = 9559

VOCABULARIO = ["audífonos", "relojería", "joyería", "casio", "apple", "pandora",
               "mercadolibre", "shopee", "amazon", "facebook", "gracias", "adiós",
               "uno", "dos", "tres", "cuatro", "cinco", "mil", "cien", "pesos", "COP",
               "ana", "carlos", "maria", "jose", "luis", "sofia", "diego", "laura",
               "miguel", "carmen", "pedro", "juan", "andrea", "david", "patricia","Diego","Kevin","Angie","Manuel"]

def reiniciar_servidor():
    try:
        conn = httplib.HTTPConnection(SERVER_IP, SERVER_PORT)
        conn.request("POST", "/reiniciar")
        conn.getresponse()
        print("🔄 Conversación reiniciada en el servidor.")
    except Exception as e:
        print("❌ Error al reiniciar:", str(e))
    finally:
        conn.close()

def obtener_pregunta():
    try:
        conn = httplib.HTTPConnection(SERVER_IP, SERVER_PORT)
        conn.request("GET", "/siguiente_pregunta")
        res = conn.getresponse()
        data = json.loads(res.read())
        return data
    except Exception as e:
        print("❌ Error al obtener pregunta:", str(e))
        return {"fin": True}
    finally:
        conn.close()

def enviar_respuesta(respuesta):
    try:
        conn = httplib.HTTPConnection(SERVER_IP, SERVER_PORT)
        headers = {'Content-Type': 'application/json'}
        cuerpo = json.dumps({"respuesta": respuesta})
        conn.request("POST", "/respuesta", cuerpo, headers)
        res = conn.getresponse()
        return res.status == 200
    except Exception as e:
        print("❌ Error al enviar respuesta:", str(e))
        return False
    finally:
        conn.close()

def obtener_resultado_final():
    try:
        conn = httplib.HTTPConnection(SERVER_IP, SERVER_PORT)
        conn.request("GET", "/resultado_final")
        res = conn.getresponse()
        data = json.loads(res.read())
        return data.get("resultado", "No se pudo obtener resultado.")
    except Exception as e:
        return "Error al obtener resultado: {}".format(str(e))
    finally:
        conn.close()

def obtener_nombre_usuario():
    try:
        conn = httplib.HTTPConnection(SERVER_IP, SERVER_PORT)
        conn.request("GET", "/obtener_nombre")
        res = conn.getresponse()
        data = json.loads(res.read())
        return data.get("nombre", "")
    except Exception as e:
        print("❌ Error al obtener nombre:", str(e))
        return ""
    finally:
        conn.close()

def escuchar_respuesta(asr, memory, max_palabras=2, tiempo_maximo=15):
    """Función para escuchar respuesta del usuario"""
    palabras = []
    ultimo = ""
    
    # Limpiar memoria antes de escuchar
    try:
        memory.removeData("WordRecognized")
    except:
        pass
    
    # Esperar un momento antes de empezar a escuchar
    time.sleep(2)
    print("🎧 Esperando respuesta del usuario...")
    
    inicio = time.time()

    while time.time() - inicio < tiempo_maximo and len(palabras) < max_palabras:
        try:
            result = memory.getData("WordRecognized")
            if isinstance(result, list) and len(result) >= 2:
                palabra = result[0]
                confianza = result[1]

                if palabra != ultimo and confianza > 0.4:
                    print("🗣️ Palabra reconocida: " + str(palabra))
                    palabras.append(palabra)
                    ultimo = palabra

            time.sleep(0.5)

        except Exception as e:
            print("⚠️ Error en memoria: " + str(e))
            time.sleep(1)

    if palabras:
        return " ".join(palabras)
    else:
        return "no entendi"

def main():
    session = qi.Session()
    session.connect("tcp://127.0.0.1:9559")

    animated_speech = session.service("ALAnimatedSpeech")
    asr = session.service("ALSpeechRecognition")
    memory = session.service("ALMemory")
    # tablet = session.service("ALTabletService")  # tablet info
    
    # Reiniciar la conversación en el servidor
    reiniciar_servidor()

    # Configurar ASR
    try:
        asr.unsubscribe("Chat_ASR")
    except:
        pass

    asr.pause(True)
    time.sleep(0.5)
    
    asr.setLanguage("Spanish")
    asr.setVocabulary(VOCABULARIO, True)
    
    asr.pause(False)
    asr.subscribe("Chat_ASR")

    print("🤖 Pepper iniciando presentación personalizada...")

    # PRESENTACIÓN DE AK WATCH
    presentacion = "Hola! Bienvenido a AK Watch, tu tienda especializada donde encontraras la mejor seleccion en relojeria, joyeria, audifonos y mucho mas. Soy tu asistente virtual y estoy aqui para ayudarte a encontrar exactamente lo que necesitas."
    
    print("🎤 Presentacion: " + presentacion)
    # tablet.showText("¡Bienvenido a AK Watch!")
    
    asr.pause(True)
    animated_speech.say(presentacion)
    time.sleep(2)
    asr.pause(False)

    # PREGUNTA POR EL NOMBRE
    pregunta_nombre = "Para brindarte una mejor atencion, me gustaria conocerte. Cual es tu nombre?"
    print("📢 Preguntando nombre: " + pregunta_nombre)
    # tablet.showText("¿Cuál es tu nombre?")
    
    asr.pause(True)
    animated_speech.say(pregunta_nombre)
    time.sleep(1)
    asr.pause(False)

    # Escuchar el nombre (permitir 1 palabra, más tiempo)
    nombre_usuario = escuchar_respuesta(asr, memory, max_palabras=1, tiempo_maximo=12)
    
    print("👤 Nombre del usuario: " + nombre_usuario)
    enviar_respuesta(nombre_usuario)  # Enviar nombre al servidor
    
    # Saludo personalizado
    if nombre_usuario != "no entendi":
        saludo_personal = "Mucho gusto, " + nombre_usuario + "! Ahora vamos a encontrar el producto perfecto para ti. Te hare algunas preguntas para poder ayudarte mejor."
    else:
        saludo_personal = "Perfecto! Ahora vamos a encontrar el producto ideal para ti. Te hare algunas preguntas para poder ayudarte mejor."
    
    print("👋 Saludo personalizado: " + saludo_personal)
    # tablet.showText("¡Hola {}!".format(nombre_usuario))
    
    asr.pause(True)
    animated_speech.say(saludo_personal)
    time.sleep(2)
    asr.pause(False)

    print("🤖 Iniciando proceso de consulta personalizada...")

    # PROCESO NORMAL DE PREGUNTAS
    while True:
        pregunta_info = obtener_pregunta()
        if pregunta_info.get("fin"):
            print("✅ Todas las preguntas respondidas.")
            break

        texto_pregunta = pregunta_info.get("pregunta", "")
        nombre_actual = obtener_nombre_usuario()
        
        # Personalizar la pregunta con el nombre
        if nombre_actual and nombre_actual != "no entendi":
            texto_pregunta_personalizada = nombre_actual + ", " + texto_pregunta
        else:
            texto_pregunta_personalizada = texto_pregunta
            
        print(" Pregunta personalizada: " + texto_pregunta_personalizada)
        # tablet.showText(texto_pregunta_personalizada)
        
        asr.pause(True)
        animated_speech.say(texto_pregunta_personalizada)
        time.sleep(1)
        asr.pause(False)

        # Escuchar respuesta
        respuesta_usuario = escuchar_respuesta(asr, memory, max_palabras=2, tiempo_maximo=12)

        # tablet.showText("Usuario dijo: " + respuesta_usuario)
        print("📝 Enviando respuesta: " + respuesta_usuario)
        enviar_respuesta(respuesta_usuario)

        print("⏳ Esperando antes de la siguiente pregunta...\n")
        time.sleep(2)

    # RESULTADO FINAL PERSONALIZADO
    resultado = obtener_resultado_final()
    nombre_final = obtener_nombre_usuario()
    
    if nombre_final and nombre_final != "no entendi":
        mensaje_final = "Perfecto, " + nombre_final + "! He terminado el analisis del producto que buscas."
    else:
        mensaje_final = "Perfecto! He terminado el analisis del producto que buscas."
    
    print("🧠 Resultado personalizado obtenido:\n" + resultado)
    
    asr.pause(True)
    animated_speech.say(mensaje_final)
    time.sleep(1)
    animated_speech.say(resultado[:500])
    
    # Despedida personalizada
    if nombre_final and nombre_final != "no entendi":
        despedida = "Gracias por visitar AK Watch, " + nombre_final + ". Esperamos verte pronto!"
    else:
        despedida = "Gracias por visitar AK Watch. Esperamos verte pronto!"
    
    animated_speech.say(despedida)
    asr.pause(False)

    # Limpiar al final
    try:
        asr.pause(True)
        asr.unsubscribe("Chat_ASR")
    except:
        pass

    print("✅ Finalizado.")

if __name__ == "__main__":
    main()
