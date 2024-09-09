import socket
import json
import time
from threading import Thread

# Realiza a requisição da resposta através da API do Copilot
def consulta_copilot(prompt):
    import http.client
    import json
    
    # Conexão
    conn = http.client.HTTPSConnection("copilot5.p.rapidapi.com")
    
    prompt_gera_resposta_curta = prompt + " Responda de forma clara e bem resumida. Não digite nada além da resposta."

    # Payload da solicitação
    payload = json.dumps({
        "message": prompt_gera_resposta_curta,
        "conversation_id": None,
        "tone": "BALANCED",
        "markdown": False,
        "photo_url": None
    })

    # Cabeçalhos da solicitação
    headers = {
        'x-rapidapi-key': "81260b7ee9msh38c8b6574e5a511p1fb191jsn00a5748320e8",
        'x-rapidapi-host': "copilot5.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    # Envio da solicitação POST para a API
    conn.request("POST", "/copilot", payload, headers)

    # Recebimento da resposta da API
    resposta = conn.getresponse()
    data = resposta.read()
    
    # Decodifica a resposta usando JSON
    resposta_json = json.loads(data.decode("utf-8"))
    
    # Extrai a mensagem específica
    mensagem = resposta_json.get("data", {}).get("message", "Erro: Não foi possível obter a resposta.")
    
    return mensagem

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

# Função para escolher se a resposta no modo controlado será da IA ou do humano
def obter_resposta_controlada(pergunta):
    escolha = input(f"Como você deseja responder? (Digite 'ia' para IA ou 'humano' para responder você mesmo): ").strip().lower()
    if escolha == 'ia':
        delay = float(input("Digite o tempo de espera para resposta de IA (em segundos): "))
        time.sleep(delay)  # Adiciona um tempo de espera se a escolha for IA
        resposta = consulta_copilot(pergunta)
        return resposta, 'ia'
    else:
        resposta = input(f"Digite a resposta humana para a pergunta '{pergunta}': ")
        return resposta, 'humano'

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
                time.sleep(delay)  # Tempo de atraso definido para resposta gerada por IA
                resposta = consulta_copilot(pergunta)
                resposta_proveniente = 'ia'
                respostas_ia += 1
            else:
                resposta, resposta_proveniente = obter_resposta_controlada(pergunta)
                if resposta_proveniente == 'humano':
                    respostas_humano += 1
                else:
                    respostas_ia += 1
    
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
