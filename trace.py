from mitmproxy import http
import re

TARGET_HOST = "d.mlcdn.com.br"
TARGET_PARAM_FIXED = "5cfbehmb"  # O valor constante na query string
UUID_PATTERN = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')  # Regex para UUID
OUTPUT_FILE = "resultado/captured_uuids.txt"

def save_to_file(data):
    with open(OUTPUT_FILE, "w") as file:  # Modo 'w' para substituir o conteúdo existente
        file.write(data + "\n")

def request(flow: http.HTTPFlow) -> None:
    # Verifica se o host é o correto e se o valor constante está na query
    if flow.request.pretty_host == TARGET_HOST and TARGET_PARAM_FIXED in flow.request.query.values():
        if UUID_PATTERN.search(flow.request.pretty_url):
            uuid_value = UUID_PATTERN.search(flow.request.pretty_url).group()
            output = f"UUID capturado: {uuid_value}\nURL completa: {flow.request.pretty_url}\n"
            save_to_file(uuid_value)  # Salva/substitui o UUID no arquivo
            print(output)  # Também exibe no console

if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-p', '8080', '-s', __file__])
