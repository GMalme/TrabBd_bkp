# from re import S
# from flask.sessions import NullSession
# from flask_mysqldb import MySQL
# from config import config
# from flask import render_template
# from flask import Flask
# from flask import request,session,url_for,redirect,send_from_directory
# from markupsafe import escape
# from datetime import timedelta
# from flask_cors import CORS 

from app import cmx

variaveis = {
    'usuario': f"INSERT INTO usuario (user, nome, senha, email, status_user) VALUES (%s, %s, %s, %s,'false')",
    'administrador': f"INSERT INTO administrador (user, nome, senha, email, chave) VALUES (%s, %s, %s, %s,%s)",
}

# Retorna um
def seleciona_um(tipo, id, atributo = 'user'):
    try:
        cursor = cmx.connection.cursor()
        string_sql = f"SELECT * FROM {tipo} WHERE {atributo} = '{id}'"
        cursor.execute(string_sql)
        data = cursor.fetchall()
        return (data)
    except Exception as ax:
        return (400,ax)

# Retorna todos
def seleciona_todos(tipo):
    cursor = cmx.connection.cursor()
    string_sql = f"SELECT * FROM '{tipo}''"
    cursor.execute(string_sql)
    data = cursor.fetchall()
    return data
    
# Adiciona
def adiciona(tipo, data, acessKey = ""):
    print("data:",data[0])
    val = valida(tipo, data, acessKey) if (tipo == "usuario" or tipo == "administrador") else 200
    if val[0] == 200:
        cursor = cmx.connection.cursor()
        cursor.execute(variaveis[tipo], data)
        cmx.connection.commit()
        return val
    else:
        return val
        
# Atualiza 
def atualiza(tipo,data):
    print("hi")

# Exclui

#Valida
def valida(tipo, data, acessKey):
    if seleciona_um(tipo, data[0]) != ():
        return (403, "Id Proibido!")
    for dado in data:
        if dado == "":
            return (400, "Preenchimento Invalido!")
    if acessKey == ":" or acessKey.find(":")==-1 and tipo == "administrador":
        return (400, "Chave Invalida!")
    return (200, "Preenchimento Valido")
