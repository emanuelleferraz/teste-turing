# Teste de Turing 🤖x👩‍💻
Este projeto consiste em um servidor e um cliente para um jogo baseado no teste de Turing. O servidor utiliza dois modos de operação sendo: Automático (API do ChatGPT) ou Controloado (Humano) para fornecer respostas e permite ao cliente identificar se a resposta veio de um humano ou de uma IA.

## Estrutura do Projeto
O projeto é composto por dois arquivos principais:

- `servidor.py`: O arquivo do servidor que gerencia as conexões e respostas.
- `cliente.py`: O arquivo do cliente que interage com o servidor.

## Requisitos
- [![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
- Bibliotecas Python: `socket`, `json`, `http.client` e `threading`

## Configurações
 1. Configurações de API:
Você precisará de uma chave de API válida da OpenAI. Substitua `9cb60b74e4msh28a3c486cff37a6p16291ejsnde96528a9afb` no código do servidor por sua chave de API.
 2. Configurações no Cliente:
No arquivo `cliente.py`, o cliente se conectará ao servidor utilizando:
- Host: Substitua o localhost `127.0.0.1` pelo IP da máquina na qual o servidor estará rodando.
- Porta: `20000`

## Execução
Para executar o jogo:
1. Vá para o diretório onde contém o arquivo `servidor.py` e execute esse arquivo. Ou use o comando `python servidor.py` para executar o arquivo no terminal. O servidor iniciará e começará a ouvir conexões na porta configurada.
2. Após isso, vá para o diretório onde contém o arquivo `cliente.py` e execute esse arquivo. Ou use o comando `python client.py` para executar o arquivo no terminal. O cliente irá se conectar ao servidor e permitir que você faça perguntas e interaja.

## Funcionalidade
### Servidor
 - Modo de Operação:
   - Automático: O servidor gera respostas usando a API do ChatGPT após um atraso especificado.
   - Controlado: O servidor permite que um operador humano forneça respostas.
  
  - Gerenciamento de Dados:
Histórico: As perguntas, respostas e se o cliente acertou a origem são salvas em `historico.txt`.
Ranking: O ranking é atualizado em `ranking.txt` com base no percentual de acertos dos clientes.

### Cliente
 - Registro: O cliente envia seu nome para o servidor.
 
 - Interação:
 O cliente envia perguntas e recebe respostas do servidor.
 O cliente deve identificar se a resposta veio de um humano ou de uma IA.
 O cliente pode escolher fazer novas perguntas ou encerrar a interação.

 - Estatísticas: O cliente recebe estatísticas sobre as respostas ao final da sessão.

## Observações
Certifique-se de que o servidor esteja em execução antes de iniciar o cliente.
O servidor deve estar configurado para aceitar conexões na porta 20000, e o cliente deve conectar-se a este IP e porta.

## Contato
 - emanuelle.ferrazlm@gmail.com
