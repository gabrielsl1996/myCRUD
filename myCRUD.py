import mysql.connector
import re

# Para funcionar função input em Python 2.x.
try: input = raw_input
except NameError: pass

#Acessa MySQL
connection = mysql.connector.connect(host='localhost', user='root', password='', charset='utf8')
cursor = connection.cursor(dictionary=True)

#Criação do banco de dados mySQL
try:
    cursor.execute("CREATE DATABASE mycrudi ")
except: pass #Caso o database já exista

#Acessa database
connection = mysql.connector.connect(host='localhost', user='root', password='', database='mycrudi', charset='utf8')
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

except: pass #Caso a tabela já exista, ignora este passo

#Criação da tabela de empresas
try:
    cursor.execute(""" CREATE TABLE empresas
        (
        id INT(11) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
        nome VARCHAR(30) NOT NULL,
        cnpj BIGINT(14) UNSIGNED,
        PRIMARY KEY (id)
        )
        """)
    connection.commit()

except: pass #Caso a tabela já exista, ignora este passo

#Criação da tabela de relacionamento
try:
    cursor.execute(""" CREATE TABLE empresas_usuarios
        (
        id INT(11) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
        idUsuario INT UNSIGNED ZEROFILL NOT NULL,
        idEmpresa INT UNSIGNED ZEROFILL NOT NULL,
        PRIMARY KEY (id)
        )
        """)

    #Relaciona chave de users com idUsuario e empresas com idEmpresa
    cursor.execute("""ALTER TABLE empresas_usuarios
        ADD CONSTRAINT FK_usuario
        FOREIGN KEY(idUsuario)
        REFERENCES users(id)""")

    cursor.execute("""ALTER TABLE empresas_usuarios
        ADD CONSTRAINT FK_empresa
        FOREIGN KEY(idEmpresa)
        REFERENCES empresas(id)""")

    connection.commit()
except: pass #Caso a tabela já exista, ignora este passo


#################Funções para checagem de erros##########################

#Checa Menu
def checaErroMenu(opt):
    try:
        if (int(opt) > -1 and int(opt) <9):
            return False
        else:
            print("Opção inválida!")
            input("Digite qualquer tecla para voltar ao menu principal\n")
            return True
    except:
        print("Opção inválida!")
        input("Digite qualquer tecla para voltar ao menu principal\n")
        return True

#Checa Nomes de Usuários
def checaErroNomePessoa(str):
    str = str.replace(" ","") #Ignora espaços no nome (assumindo que nome e sobrenome serão inseridos em um mesmo campo)
    if (not (re.match("^[a-z]*$", str, flags=re.I) ) ):
        print("Nome inválido! Utilize somente letras e espaços.")
        return True
    else: return False

#Checa Idade
def checaErroIdade(num):
    print(num)
    try:
        if (int(num) >= 0):
            return False
        else:
            print("Idade inválida! Utilize somente números positivos.")

            return True
    except:
        print("Idade inválida! Utilize somente números positivos.")

        return True

#Checa CNPJ
def checaErroCNPJ(num):
    print(num)
    try:
        if (int(num) >= 0 and len(num)==14):
            return False
        else:
            if (int(num) >= 0):
                print("CNPJ inválido! Verifique a quantidade de dígitos")
            else:
                print("CNPJ inválido! Utilize somente números positivos")

            return True
    except:
        print("Idade inválida! Utilize somente números positivos.")

        return True

#####################Funções principais####################

#Adiciona n usuários
def CreateUser(n):
    for i in range(n):
        nome = input('Digite o nome\n')
        idade = input("Digite a idade (coloque '0' para idade desconhecida)\n")
        if (not (checaErroNomePessoa(nome) or checaErroIdade(idade) ) ): #Checa se nome e idade são válidos
            if (int(idade) == 0):
                cursor.execute("INSERT INTO users(nome) VALUES('{}')".format(nome)) #Cria com apenas nome (idade desconhecida)
            else:
                cursor.execute("INSERT INTO users(nome, idade) VALUES('{}', {})".format(nome, int(idade))) #Cria com nome e idade
            print("Cadastro de '{}' criado com sucesso\n".format(nome))
            input("Digite qualquer tecla para voltar ao menu principal\n")
        else:
            print("Cadastro de '{}' não criado!".format(nome))
            input("Digite qualquer tecla para voltar ao menu principal\n")

        #Fecha tabela
        connection.commit()


#Deleta usuários via nome (pode ser adaptada para funcionar com qualquer informação do usuário)
def DeleteUserName():
    wantedUserName = input("Qual o nome do usuário a ser deletado?\n")
    if (checaErroNomePessoa(wantedUserName)):
        print("Nome inválido! Apenas letras são permitidas")
        input("Digite qualquer tecla para voltar ao menu principal\n")

    else:
        cursor.execute("SELECT * FROM users WHERE nome = '{}' ".format(wantedUserName))
        foundUsers = cursor.fetchall()
        if(foundUsers == []):
            print("Não há usuários com este nome!\n")
        else:
            print("{} usuário(s) encontrado(s):".format(len(foundUsers)))
            print("{}\t{:11}\t{:30}\t{:5}\n".format("Índice","ID","Nome","Idade"))
            for cont in range (len(foundUsers)):
                if (foundUsers[cont]['idade'] != None):
                    print("{}\t{:011}\t{:30}\t{:>3}\n".format(cont+1, foundUsers[cont]['id'], foundUsers[cont]['nome'], foundUsers[cont]['idade']))
                else:
                    print("{}\t{:011}\t{:30}\t{:>3}\n".format(cont+1, foundUsers[cont]['id'], foundUsers[cont]['nome'], "???"))
            print("Escolha o índice usuário a ser deletado\nSelecione '0' para cancelar")
            indice = input()
            if (indice != 0 and int(indice) <= len(foundUsers)):
                cursor.execute("DELETE FROM users WHERE id = {} ".format(foundUsers[int(indice)-1]['id']))

                print("Usuário '{}' deletado(s)\n".format(wantedUserName))
            elif (int(indice) > len(foundUsers)):
                print("Índice inválido!\nOperação cancelada!")
            else:
                print("Operação cancelada!")

            input("Digite qualquer tecla para voltar ao menu principal\n")

            connection.commit()

#Lê usuários pelo nome
def ReadUserName():
    wantedUserName = input("Qual o nome do usuário a ser pesquisado?\n")
    if (checaErroNomePessoa(wantedUserName)):
        print ("Nome inválido")
        input("Digite qualquer tecla para voltar ao menu principal\n")
    else:
        cursor.execute("SELECT * FROM users WHERE nome = '{}'".format(wantedUserName))
        foundUsers = cursor.fetchall()
        if(foundUsers == []):
            print("Não há usuários com este nome!")
            input("Digite qualquer tecla para voltar ao menu principal\n")
        else:
            print("{} usuário(s) encontrado(s):".format(len(foundUsers)))
            print("{:11}\t{:30}\t{:5}\n".format("ID","Nome","Idade"))
            for cont in range (len(foundUsers)):
                if (foundUsers[cont]['idade'] != None):
                    print("{:011}\t{:30}\t{:>3}\n".format(foundUsers[cont]['id'], foundUsers[cont]['nome'], foundUsers[cont]['idade']))
                else:
                    print("{:011}\t{:30}\t{:>3}\n".format(foundUsers[cont]['id'], foundUsers[cont]['nome'], "???"))

            connection.commit()
            input("Digite qualquer tecla para voltar ao menu principal\n")

#Atualiza usuário procurando pelo nome
def UpdateUserAgeName():
    wantedUserName = input("Qual o nome do usuário a ser alterado?\n")
    if (checaErroNomePessoa(wantedUserName)):
        print ("Voltando ao menu principal\n")
    else:
        cursor.execute("SELECT * FROM users WHERE nome = '{}'".format(wantedUserName))
        foundUsers = cursor.fetchall()
        if(foundUsers == []):
            print("Não há usuários com este nome!\n")
        else:
            print("{} usuário(s) encontrado(s):".format(len(foundUsers)))
            print("{}\t{:11}\t{:30}\t{:5}\n".format("Indice","ID","Nome","Idade"))
            for cont in range (len(foundUsers)):
                if (foundUsers[cont]['idade'] != None):
                    print("{}\t{:011}\t{:30}\t{:>3}\n".format(cont+1, foundUsers[cont]['id'], foundUsers[cont]['nome'], foundUsers[cont]['idade']))
                else:
                    print("{}\t{:011}\t{:30}\t{:>3}\n".format(cont+1, foundUsers[cont]['id'], foundUsers[cont]['nome'], "???"))
            if (len(foundUsers) == 1):
                print("Digite o novo valor da idade: (OBS: '0' para desconhecido)")
                idade = input("")
                if (not checaErroIdade(idade)):
                    if (int(idade) == 0):
                        cursor.execute("UPDATE users SET idade = NULL WHERE id={}".format(foundUsers[0]['id']))
                    else:
                        cursor.execute("UPDATE users SET idade = {} WHERE id={}".format(int(idade), foundUsers[0]['id']))

            else:
                print("Digite o índice do cadastro você deseja alterar a idade:\nSelecione '0' para cancelar")
                cont = input("")
                if (not checaErroIdade(cont) and int(cont) <= len(foundUsers)):
                    cont = int(cont)
                    if (cont == 0):
                        print("Operação cancelada!\n")
                        input("Digite qualquer tecla para voltar ao menu principal\n")

                    else:
                        #print(foundUsers[cont-1]['id'])
                        print("Digite o novo valor da idade: (OBS: '0' para desconhecido)")
                        idade = input("")
                        if (not checaErroIdade(idade)):
                            if (int(idade) == 0):
                                cursor.execute("UPDATE users SET idade = NULL WHERE id={}".format(foundUsers[cont-1]['id']))
                                print("Cadastro alterado com sucesso!")
                                input("Digite qualquer tecla para voltar ao menu principal\n")
                            else:
                                cursor.execute("UPDATE users SET idade = {} WHERE id={}".format(int(idade), foundUsers[cont-1]['id']))
                                print("Cadastro alterado com sucesso!")
                                input("Digite qualquer tecla para voltar ao menu principal\n")
                else:
                    print("Cadastro inválido!")
                    input("Digite qualquer tecla para voltar ao menu principal\n")

#Criação de empresa
def CreateCompany(n):
    for i in range(n):
        nome = input('Digite o nome\n')
        cnpj = input("Digite o CNPJ\n")
        if (nome!="" and (not (checaErroCNPJ(cnpj) ) ) ): #Checa se nome e CNPJ são válidos
            cursor.execute("INSERT INTO empresas(nome, cnpj) VALUES('{}', {})".format(nome, int(cnpj))) #Cria com nome e CNPJ
            print("Cadastro de '{}' criado com sucesso\n".format(nome))
            input("Digite qualquer tecla para voltar ao menu principal\n")
        else:
            print("Cadastro de '{}' não criado!".format(nome))
            input("Digite qualquer tecla para voltar ao menu principal\n")
        #Fecha tabela
        connection.commit()

def CreateRelashionship():
    wantedUserName = input("Digite o nome do usuario\n")
    wantedCompanyName = input("Digite o nome da empresa\n")

    #Checa usuário
    if (checaErroNomePessoa(wantedUserName)):
        print ("Nome inválido")
        userOK=False
        input("Digite qualquer tecla para voltar ao menu principal\n")

    else:
        cursor.execute("SELECT * FROM users WHERE nome = '{}'".format(wantedUserName))
        foundUsers = cursor.fetchall()
        if(foundUsers == []):
            print("Não há usuários com este nome!")
            userOK = False
            input("Digite qualquer tecla para voltar ao menu principal\n")
        else:
            print("{} usuário(s) encontrado(s):".format(len(foundUsers)))
            for cont in range (len(foundUsers)):
                print("Nome = {}".format(foundUsers[cont]['nome']) )
                print("Id = {}".format(foundUsers[cont]['id']) )
                print("Idade = {}\n".format(foundUsers[cont]['idade']) )

            if (int(len(foundUsers)) > 1):
                user = input("Escolha o usuário correto")
            else:
                user=1
            userOK = True

    #Checa empresa
    if(userOK):
        cursor.execute("SELECT * FROM empresas WHERE nome = '{}'".format(wantedCompanyName))
        foundCompanies = cursor.fetchall()
        if(foundCompanies == []):
            print("Não há empresas com este nome!")
            companyOK = False
            input("Digite qualquer tecla para voltar ao menu principal\n")
        else:
            print("{} empresa(s) encontrada(s):".format(len(foundCompanies)))
            for cont in range (len(foundCompanies)):
                print("Nome = {}".format(foundCompanies[cont]['nome']) )
                print("Id = {}".format(foundCompanies[cont]['id']) )
                print("CNPJ = {}\n".format(foundCompanies[cont]['cnpj']) )
            if (int(len(foundCompanies) > 1)):
                company = input("Selecione a empresa correta")
            else:
                company = 1
            companyOK = True
    if (companyOK):
        SQLInsertCmd = """INSERT INTO empresas_usuarios (idUsuario, idEmpresa)
            VALUES ({},{})""".format(foundUsers[user-1]['id'], foundCompanies[company-1]['id'])
        cursor.execute(SQLInsertCmd)
        connection.commit()
        input("Digite qualquer tecla para voltar ao menu principal\n")


############################## Menu ##################################
def Menu():
    option = -1
    while (option != 0):
        print("Menu principal")
        print("Selecione a ação desejada:")
        print("1 - Adicionar usuário")
        print("2 - Deletar usuário por nome")
        print("3 - Buscar usuário por nome")
        print("4 - Alterar idade de um usuário")
        print("5 - Adicionar empresa")
        print("6 - Criar relacionamento (usuário - empresa)")
        print("0 - SAIR")
        opt = input("")
        if (not checaErroMenu(opt)): #Checa se a entrada foi válida
            option = int(opt) #Transforma entrada para comparar com integer
            if (option == 1):
                CreateUser(1)
            elif (option == 2):
                DeleteUserName()
            elif (option == 3):
                ReadUserName()
            elif (option == 4):
                UpdateUserAgeName()
            elif (option == 5):
                CreateCompany(1)
            elif (option == 6):
                CreateRelashionship()



Menu()
#CreateUser(1)
#DeleteUserName()





connection.close()
