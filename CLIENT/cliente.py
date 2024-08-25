import socket

def main():
    HOST = '127.0.0.1'
    PORT = 20000
    BUFFER_SIZE = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        nome = input("Digite seu nome para registro: ")
        s.send(nome.encode())
        
        while True:
            pergunta = input("Digite sua pergunta para o servidor: ").strip()
            s.send(pergunta.encode())
            
            if not pergunta:
                break
            
            resposta = s.recv(BUFFER_SIZE).decode('utf-8')
            print(f"Resposta do servidor: {resposta}")

            escolha = input("A resposta que você recebeu é de um humano ou IA? (Digite 'humano' ou 'ia'): ").strip().lower()
            s.send(escolha.encode())
            
            confirmacao = s.recv(BUFFER_SIZE).decode('utf-8')
            if confirmacao == 'correto':
                print("Você acertou!")
            else:
                print("Você errou.")
                
            nova_pergunta = input("Deseja fazer uma nova pergunta? (sim/nao): ").strip().lower()
            s.send(nova_pergunta.encode())
            if nova_pergunta != 'sim':
                break

        estatisticas = s.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Dados de {nome}: {estatisticas}")

if __name__ == "__main__":
    main()
