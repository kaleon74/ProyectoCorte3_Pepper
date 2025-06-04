# -*- coding: utf-8 -*-
# ak_prices_server.py

from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Preguntas a realizar en orden (ahora incluye el nombre como primera "pregunta")
PREGUNTAS = [
    ("nombre", u"¿Cuál es tu nombre?"),  # Esta se maneja de forma especial
    ("producto", u"¿qué producto deseas consultar? Por ejemplo: relojería, joyería, audífonos."),
    ("plataformas", u"¿en qué plataformas deseas consultar? Por ejemplo: MercadoLibre, Shopee, Amazon, Facebook Marketplace."),
    ("precio", u"¿cuál es tu rango de precio? Por ejemplo: mayor a 150 mil COP, menor a 400 mil COP."),
    ("marca", u"¿qué marca prefieres? Por ejemplo: Casio, Apple, Pandora."),
    ("cantidad", u"¿cuántos resultados quieres comparar? Por ejemplo: 1, 2, etc.")
]

# Diccionario de respuestas del usuario
conversacion = {
    "estado": 0,  # índice actual de pregunta
    "respuestas": {}  # clave: valor
}

# Deepseek API
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e'
API_URL = 'https://api.deepseek.com/v1/chat/completions'

def safe_encode(texto):
    """Convierte texto a UTF-8 de forma segura"""
    if isinstance(texto, unicode):
        return texto.encode('utf-8')
    elif isinstance(texto, str):
        try:
            return texto.decode('utf-8').encode('utf-8')
        except:
            return texto
    return str(texto)

def construir_prompt():
    """Construye el prompt con las respuestas"""
    r = conversacion["respuestas"]
    
    # Incluir el nombre en el prompt para personalizar la respuesta
    nombre = r.get("nombre", "Cliente")
    if nombre == "no entendi":
        nombre = "Cliente"
    
    prompt = u"""Necesito que realices una comparativa de precios siguiendo estos parametros:
- Cliente: {nombre}
- Producto: {producto}
- Plataformas: {plataformas}
- Precio: {precio}
- Marca: {marca}
- Cantidad: {cantidad}

INSTRUCCIONES:
- Dirigete al cliente por su nombre ({nombre}) de manera natural y amigable
- Estructura: caracteristicas basicas del producto, precio del producto, tabla comparativa
- Longitud: 700 palabras aproximadamente
- Estilo: analisis del producto sencillo y claro, personalizado para {nombre}
- Incluye un consejo personalizado para que {nombre} como emprendedor pueda tasar el precio de su producto o elegir donde es mejor comprar
- Menciona que esta informacion es cortesia de AK Watch, tu tienda especializada en relojeria, joyeria y audifonos

Haz que la respuesta sea calida y personal, como si fueras un asesor experto de AK Watch hablando directamente con {nombre}.
""".format(
        nombre=nombre,
        producto=r.get("producto", ""),
        plataformas=r.get("plataformas", ""),
        precio=r.get("precio", ""),
        marca=r.get("marca", ""),
        cantidad=r.get("cantidad", "")
    )
    
    return prompt

def consultar_deepseek(prompt, temperatura=0.85):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json; charset=utf-8'
    }

    data = {
        'model': 'deepseek-chat',
        'temperature': temperatura,
        'messages': [{
            'role': 'user',
            'content': prompt
        }]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content']
        return result
    except Exception as e:
        return u"Error al consultar Deepseek: {}".format(str(e))

@app.route('/siguiente_pregunta', methods=['GET'])
def siguiente_pregunta():
    idx = conversacion["estado"]
    if idx >= len(PREGUNTAS):
        return jsonify({"fin": True})

    clave, texto = PREGUNTAS[idx]
    
    # Saltar la pregunta del nombre ya que se maneja en el cliente
    if clave == "nombre":
        conversacion["estado"] += 1
        if conversacion["estado"] >= len(PREGUNTAS):
            return jsonify({"fin": True})
        clave, texto = PREGUNTAS[conversacion["estado"]]
    
    return jsonify({
        "fin": False,
        "pregunta": texto
    })

@app.route('/respuesta', methods=['POST'])
def recibir_respuesta():
    data = request.json
    texto_usuario = data.get("respuesta", "").strip()

    idx = conversacion["estado"]
    if idx >= len(PREGUNTAS):
        return jsonify({"status": "finalizado"})

    clave, _ = PREGUNTAS[idx]
    conversacion["respuestas"][clave] = texto_usuario
    conversacion["estado"] += 1
    
    print(u"📝 Respuesta recibida - {}: {}".format(clave, texto_usuario).encode('utf-8'))

    return jsonify({"status": "ok"})

@app.route('/obtener_nombre', methods=['GET'])
def obtener_nombre():
    """Endpoint para obtener el nombre del usuario (simplificado)"""
    nombre = conversacion["respuestas"].get("nombre", "Cliente")
    return jsonify({"nombre": nombre})

@app.route('/resultado_final', methods=['GET'])
def resultado_final():
    if conversacion["estado"] < len(PREGUNTAS):
        return jsonify({"error": "Faltan respuestas"})

    prompt = construir_prompt()
    resultado = consultar_deepseek(prompt)
    
    # Log para debugging (simplificado)
    print("🧠 Generando resultado final...")
    print("📋 Respuesta generada correctamente")
    
    return jsonify({"resultado": resultado})

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    conversacion["estado"] = 0
    conversacion["respuestas"] = {}
    print("🔄 Conversación reiniciada")
    return jsonify({"status": "reiniciado"})

@app.route('/estado', methods=['GET'])
def obtener_estado():
    """Endpoint para debugging - ver el estado actual"""
    return jsonify({
        "estado": conversacion["estado"],
        "respuestas": conversacion["respuestas"],
        "total_preguntas": len(PREGUNTAS)
    })

if __name__ == '__main__':
    print("🚀 Servidor AK Watch iniciado...")
    print("🎯 Endpoints disponibles:")
    print("   - GET  /siguiente_pregunta")
    print("   - POST /respuesta")
    print("   - GET  /obtener_nombre")
    print("   - GET  /resultado_final")
    print("   - POST /reiniciar")
    print("   - GET  /estado (debug)")
    app.run(host='0.0.0.0', port=9559)
