import socket
import threading

#Uma conversa em websocket irá precisar de 1 servidor e os clientes
#O servidor irá receber a coneção dos usuarios e as mensagens.
#O servidor irá redistribuir uma mensagem para todos os usuario conectados



clientes = []
nomes_dos_usuarios = []
def receber_usuarios(servidor):
    while True:
        cliente, endereco = servidor.accept()
        
        
        cliente.send('_string_secreta_para_pedir_nick_do_usuario_'.encode('ascii'))
        nome_usuario = cliente.recv(1024).decode('ascii')
        nomes_dos_usuarios.append(nome_usuario)
        print(f"Usuario ~{nome_usuario}~ do endreço {endereco[0]}:{endereco[1]} conectado")
        clientes.append(cliente)
        
        thread = threading.Thread(target=receber_mensagens_de_usuarios, args=(cliente,))
        thread.start()
        

def receber_mensagens_de_usuarios(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            enviar_mensagens_para_todos_usuarios_conectados(mensagem)
        except:
            index_cliente_que_saiu = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nome = nomes_dos_usuarios[index_cliente_que_saiu]
            mensagem_saida = f"Usuario {nome} saiu do chat".encode("ASCII")
            print(f"Usuario ~{nome}~ desconectou do servidor")
            enviar_mensagens_para_todos_usuarios_conectados(mensagem_saida)
            nomes_dos_usuarios.remove(nome)
            break
            
def enviar_mensagens_para_todos_usuarios_conectados(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)
        


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    servidor.bind(("localhost", 5000)) #atribui ip e porta para o servidor
    servidor.listen(2) #ativa o servidor com um limite maximo de usuarios que podem entrar, no caso 2
    
    receber_usuarios(servidor)
    
    


if __name__ == "__main__":
    main()