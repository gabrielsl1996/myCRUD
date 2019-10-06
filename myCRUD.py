import mysql.connector
import re

# Para funcionar função input em Python 2.x.
try: input = raw_input
except NameError: pass

#Acessa MySQL
connection = mysql.connector.connect(host='localhost', user='root', password='', database='mycrud', charset='utf8')
cursor = connection.cursor(dictionary=True)

#Criação da tabela de usuários
try:
    cursor.execute(""" CREATE TABLE users
        (
        id INT(11) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT ,
        nome VARCHAR(30) NOT NULL,
        idade INT UNSIGNED,
        PRIMARY KEY (id)
        )
        """)
    connection.commit()
    print("FOI")
except: pass #Caso a tabela já exista, ignora este passo


#################Funções para checagem de erros##########################

#Menu
def checaErroMenu(opt):
    try:
        if (int(opt) > -1 and int(opt) <9):
            return False
        else:
            print("Opção inválida!")
            input("Digite qualquer tecla para voltar ao menu principal")
            return True
    except:
        print("Opção inválida!")
        input("Digite qualquer tecla para voltar ao menu principal")
        return True

#Nomes de usuários
def checaErroNomePessoa(str):
    str = str.replace(" ","") #Ignora espaços no nome
    #print(str)
    if (not (re.match("^[a-z]*$", str, flags=re.I) ) ):
        print("Nome inválido! Utilize somente letras e espaços.")
        return True
    else: return False

#Idade
def checaErroIdade(num):
    try:
        if (int(num) > 0):
            return False
        else:
            print("Idade inválida! Utilize somente números positivos.")
            return True
    except:
        print("Idade inválida! Utilize somente números positivos.")
        return True


#####################Funções principais####################

#Adiciona n usuários
def CreateUser(n):
    for i in range(n):
        nome = input('Digite um nome\n')
        idade = input('Digite uma idade\n')
        if (not (checaErroNomePessoa(nome) or checaErroIdade(idade) ) ): #Checa se nome e idade são válidos
            cursor.execute("INSERT INTO users(nome, idade) VALUES('{}', {})".format(nome, idade))
        else:
            print("Cadastro de '{}' não criado!".format(nome))
        #Fecha tabela
        connection.commit()


#Deleta usuários via Nome
def DeleteUserName():
    wantedUserName = input("Qual o nome do usuário a ser deletado?")
    if (checaErroNomePessoa(wantedUserName)):
    #if (not (re.match("^[a-z]*$", wantedUserName, flags=re.I) ) ):
        print ("Error! Nome inválido! Utilize somente letras por favor")
    else:
        cursor.execute("SELECT * FROM users WHERE nome = '{}' ".format(wantedUserName))
        FoundUsers = cursor.fetchall()
        if(FoundUsers == []):
            print("Não há usuários com este nome!")
        else:
            cursor.execute("DELETE FROM users WHERE nome = '{}' ".format(wantedUserName))
            print("Usuário(s) '{}' deletado(s)".format(wantedUserName))
            connection.commit()


#Função Menu
def Menu():
    option = -1
    while (option != 0):
        print("Selecione a ação desejada:")
        print("1 - Adicionar usuário")
        print("2 - Deletar usuário por nome")
        print("3 - Busca cadastro pot nome")

        print("0 - SAIR")
        opt = input("")
        if (not checaErroMenu(opt)): #Checa se a entrada foi válida
            option = int(opt) #Transforma entrada para comparar com integer
            if (option == 1):
                CreateUser(1)
            elif (option == 2):
                DeleteUserName()




"""
#Lê usuários
cursor.execute("SELECT * FROM users ")
users = cursor.fetchall()
i=True
cont=-1
while i:
    print(cont)
    cont+=1
    #print("Entrou!")
    try: print(users[cont]['idade'])
    except: i=False

connection.commit()
"""

"""
#Atualiza usuários


"""

Menu()
#CreateUser(1)
#DeleteUserName()





connection.close()
