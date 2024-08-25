import socket
import json
import time
from threading import Thread

# Realiza a requisão da resposta através da API do Chat
def consulta_chatgpt(prompt):
    import http.client
    
    # Conexão
    conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")
    
    prompt_gera_resposta_curta = prompt + " Responda da forma mais sucinta possível. Não utilize emojis nas respostas."
    
    payload = json.dumps({
        "messages": [{"role": "user", "content": prompt_gera_resposta_curta}],
        "system_prompt": "",
        "temperature": 0.7,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    })

    headers = {
        'x-rapidapi-key': "9cb60b74e4msh28a3c486cff37a6p16291ejsnde96528a9afb",
        'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/conversationgpt4-2", payload, headers)

    resposta = conn.getresponse()
    data = resposta.read()

    # Decodifica a resposta usando JSON
    resposta_json = json.loads(data.decode("utf-8"))
    return resposta_json.get("result", "Erro: Não foi possível obter a resposta.")

def salvar_historico(nome, pergunta, resposta, acertou):
    with open("historico.txt", "a", encoding="utf-8") as historico:
        historico.write(f"Nome: {nome}, Pergunta: {pergunta}, Resposta: {resposta}, Acertou: {acertou}\n")

def atualizar_ranking(nome, acertou):
    ranking = {}
    
    try:
        with open("ranking.txt", "r", encoding="utf-8") as rank_file:
            ranking = json.load(rank_file)
    except FileNotFoundError:
        pass

    if nome in ranking:
        ranking[nome]['total'] += 1
        if acertou:
            ranking[nome]['acertos'] += 1
    else:
        ranking[nome] = {'total': 1, 'acertos': 1 if acertou else 0}

    # Calcular percentual de acertos
    ranking[nome]['percentual'] = (ranking[nome]['acertos'] / ranking[nome]['total']) * 100

    # Ordenar ranking por percentual de acertos (decrescente)
    ranking_ordenado = dict(sorted(ranking.items(), key=lambda item: item[1]['percentual'], reverse=True))

    with open("ranking.txt", "w", encoding="utf-8") as rank_file:
        json.dump(ranking_ordenado, rank_file, indent=4, ensure_ascii=False)      

def on_new_client(clientsocket, addr):
    print(f'Cliente {addr} conectado.')
    
    nome = clientsocket.recv(1024).decode('utf-8')
    print(f'Nome do cliente: {nome}')
    
    respostas_ia = 0
    respostas_humano = 0
    acertos = 0

    while True:
        try:
            # Seleciona o modo de operação do servidor
            mode = input("Escolha o modo de operação (automatico/controlado): ").strip().lower()
            delay = 0
            if mode == 'automatico':
                delay = float(input("Digite o tempo de espera para resposta automática (em segundos): "))

            # Recebe a pergunta do client
            pergunta = clientsocket.recv(1024).decode('utf-8')
            if not pergunta:
                break

            print(f'Pergunta recebida do cliente {addr}: {pergunta}')
            
            if mode == 'automatico':
                time.sleep(delay) # Tempo de atraso definido da resposta gerada por IA
                resposta = consulta_chatgpt(pergunta)
                resposta_proveniente = 'ia'
                respostas_ia += 1
            else:
                resposta = input(f'Cliente {addr} perguntou: "{pergunta}". Digite a resposta: ') # Modo controlado
                resposta_proveniente = 'humano'
                respostas_humano += 1
    
            # Envia a resposta ao client
            clientsocket.send(resposta.encode('utf-8'))

            escolha = clientsocket.recv(1024).decode('utf-8').strip().lower()
            acertou = escolha == resposta_proveniente
            if acertou:
                acertos += 1
                clientsocket.send("correto".encode('utf-8'))
            else:
                clientsocket.send("incorreto".encode('utf-8'))

            salvar_historico(nome, pergunta, resposta, acertou)
            atualizar_ranking(nome, acertou)
            
            nova_pergunta = clientsocket.recv(1024).decode('utf-8').strip().lower()
            if nova_pergunta != 'sim':
                break

        except Exception as error:
            print(f"Erro com o cliente {addr}: {error}")
            break

    estatisticas = f"Respostas de IA: {respostas_ia}, Respostas de Humanos: {respostas_humano}, Acertos: {acertos}"
    clientsocket.send(estatisticas.encode('utf-8'))

    clientsocket.close()

def main():
    HOST = '127.0.0.1'
    PORT = 20000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen()
        print(f'Servidor escutando em {HOST}:{PORT}...')

        while True:
            clientsocket, addr = server_socket.accept()
            client_thread = Thread(target=on_new_client, args=(clientsocket, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
