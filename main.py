import os
import pugno

def listar_arquivos(diretorio):
    # Lista todos os arquivos .txt no diretório especificado
    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.txt')]
    arquivos.sort()  # Ordena os arquivos em ordem alfabética
    return arquivos

def ler_arquivo(arquivo):
    # Lê todas as linhas do arquivo especificado
    with open(arquivo, 'r') as file:
        linhas = file.readlines()
    return linhas

def main():
    diretorio = './DB'
    arquivos = listar_arquivos(diretorio)

    if not arquivos:
        print("Nenhum arquivo .txt encontrado no diretório.")
        return

    print("Arquivos encontrados:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}: {arquivo}")

    # Solicita ao usuário escolher um arquivo pelo número correspondente
    escolha = int(input("Digite o número do arquivo que você deseja abrir: ")) - 1

    if escolha < 0 or escolha >= len(arquivos):
        print("Escolha inválida.")
        return

    arquivo_escolhido = os.path.join(diretorio, arquivos[escolha])
    linhas = ler_arquivo(arquivo_escolhido)

    print(f"\nConteúdo do arquivo {arquivos[escolha]}:")
    for linha in linhas:
        linha = linha.strip()
        if ':' in linha:  # Verifica se o formato email:senha existe
            email, senha = linha.split(':', 1)
            pugno.chk(email, senha)  # Assume que esta função retorna algum resultado
        else:
            print("Formato inválido encontrado:", linha)

if __name__ == "__main__":
    main()
