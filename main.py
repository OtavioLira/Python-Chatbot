import os
import logging
from typing import List
from flask import Flask, request, jsonify
import requests
from datetime import datetime

import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

def format_response(texts: List[str]) -> jsonify:
    return jsonify({"fulfillmentMessages": [{"text": {"text": texts}}]})

@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    data = request.get_json()

    # Verificar a estrutura recebida
    logger.info(f"Recebido JSON: {data}")

    action = data['queryResult'].get('action', 'Unknown Action')
    parameters = data['queryResult'].get('parameters', {})
    
    # Verificar se a estrutura do payload contém 'data' e 'callback_query'
    payload = data.get('originalDetectIntentRequest', {}).get('payload', {})
    callback_query = payload.get('data', {}).get('callback_query', {})
    callback_data = callback_query.get('data')

    if callback_data:
        logger.info(f"callback_data: {callback_data}")
    else:
        logger.info("callback_data não encontrado")

    # Usando logs ao invés de print
    logger.info(f"action: {action}")

    # Tratar diferentes ações baseadas na intent detectada
    if action == 'defaultWelcomeIntent':
        response = format_response(['Olá, como posso ajuda-lo?'])

    elif action == 'teste':
        response = format_response(['testando resposta', 'apareceu aii?'])

    elif action == 'input.nasa':
        # Tratar o callback_data com mais cuidado, para lidar com None
        if callback_data == 'opcao_1':
            dados = get_nasa_image()
            response = format_response(['opção 1 selecionada'])
        elif callback_data == 'opcao_2':
            response = format_response(['opção 2 selecionada'])
        else:
            logger.warning(f'callback_data não reconhecido: {callback_data}')
            response = format_response(['Nenhuma opção válida foi selecionada.'])

    elif action == 'inputUnknown':
        response = format_response(['Sorry, I did not understand that clearly.'])

    else:
        response = format_response([f'No handler for the action name {action}.'])

    return response

def get_nasa_image():
    # URL da API (com a sua chave de API)
    url = "https://api.nasa.gov/planetary/apod"
    
    # Parâmetros da requisição
    params = {
        'apikey': 'ktqGxRoe1TodCvszzxfVAT6v2sbQwJk3HESc5dAf',
        'date': "2024-09-24",
        'hd': 'True',
        'format': 'json'
    }
    
    # Fazendo a requisição
    response = requests.get(url, params=params)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()

        return data
    else:
        return f"Erro na requisição: {response.status_code}"

# Chamando a função e imprimindo os dados do dia atual
data = get_current_day_data()
print(data)

if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)
