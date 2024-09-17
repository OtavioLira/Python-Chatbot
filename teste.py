import requests
import json

# URL do webhook local ou do servidor onde ele está rodando
WEBHOOK_URL = "https://python-chatbot-wrup.onrender.com//dialogflow"

# Função para simular uma requisição POST ao webhook com callback_data
def test_webhook(action, callback_data=None):
    # Estrutura de dados que simula uma requisição vinda do Dialogflow
    payload = {
        "queryResult": {
            "action": action,
            "parameters": {},  # Parâmetros são um dicionário vazio para manter a compatibilidade
        },
        "originalDetectIntentRequest": {
            "source": "telegram",
            "payload": {
                "data": {
                    "callback_query": {
                        "data": callback_data or ""
                    }
                }
            }
        },
        "session": "projects/webhook-teste-vqlv/agent/sessions/74be0701-205d-5dc1-0285-cb229f6abf85"
    }

    headers = {
        'Content-Type': 'application/json'
    }

    # Enviar uma requisição POST para o webhook Flask
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

    # Exibir a resposta
    print(f"Resposta para ação '{action}' com callback_data '{callback_data}':")
    print(response.json())

# Testando várias situações
if __name__ == "__main__":
    # Teste com ação 'teste.action' e 'opcao_1'
    test_webhook(action='teste.action', callback_data='opcao_1')

    # Teste com ação 'teste.action' e 'opcao_2'
    test_webhook(action='teste.action', callback_data='opcao_2')

    # Teste com ação 'defaultWelcomeIntent' (sem callback_data)
    test_webhook(action='defaultWelcomeIntent')

    # Teste com ação desconhecida
    test_webhook(action='unknown.action')
