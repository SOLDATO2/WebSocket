import socket
import threading

def mandar_mensagem_para_servidor(cliente, nome_usuario):
    while True:
        messagem = f"{nome_usuario}: {input("")}"
        cliente.send(messagem.encode('ascii'))

def receber_mensagens_servidor(cliente, nome_usuario):
    while True:
        try:
            message = cliente.recv(1024).decode('ascii')
            if message == '_string_secreta_para_pedir_nick_do_usuario_':
                cliente.send(nome_usuario.encode('ascii'))
            else:
                print(message)
        except:
            print("Deu algo de errado")
            cliente.close()
            break

def main():
    nome_usuario = input("Digite o seu nome: ")
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ipv4 e tcp respectivamente
    cliente.connect(('localhost', 5000))
    
    receive_thread = threading.Thread(target=receber_mensagens_servidor, args=(cliente, nome_usuario))
    receive_thread.start()

    write_thread = threading.Thread(target=mandar_mensagem_para_servidor, args=(cliente, nome_usuario))
    write_thread.start()

if __name__ == "__main__":
    main()