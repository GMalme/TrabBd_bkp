from re import S
from flask.sessions import NullSession
from flask_mysqldb import MySQL
from config import config
from flask import render_template
from flask import Flask
from flask import request,session,url_for,redirect,send_from_directory
from markupsafe import escape
from datetime import timedelta
from flask_cors import CORS 

import crud

app = Flask(__name__, static_url_path='/static')
app.secret_key = "test"
app.permanent_session_lifetime = timedelta(minutes=5)
CORS(app) 
# app.config["SESSION_PERMANENT"] = True
cmx = MySQL(app)
import crud

@app.route("/")
def helloworld():
    return "Hello, cross-origin-world"

@app.route("/logout")
def logout():
    session.pop("User", None)
    session.pop("Jogo", None)
    return redirect(url_for("login"))

@app.route("/logoutG")
def logoutG():
    session.pop("Jogo", None)
    return redirect(url_for("login"))

@app.route("/logoutA")
def logoutA():
    session.pop("User", None)
    session.pop("Admin", None)
    return redirect(url_for("login"))

@app.route("/home",methods=["GET","POST"])
def login():
    if  'User' in session:
            if 'Jogo' in session:
                cursor = cmx.connection.cursor()
                aux = session["User"]
                data = crud.seleciona_um("usuario",aux)
                print("data=",data)
                session["aviso"] = "Pesquisar"
                typeP = request.form.get("btnP")
                print("tp:",typeP)
                dataP = request.form.get("pesq")
                if dataP != "" and typeP == "Conta":
                    try:
                        print(dataP)
                        string_sql = f"SELECT * FROM usuario WHERE nome_de_usuario = '{dataP}'"
                        cursor.execute(string_sql)
                        dataP = cursor.fetchall()
                        print(dataP)
                        if dataP != ():
                            return  render_template("TelaUser.html", sess=session['User'],jog=session['Jogo'], data = dataP, flag = "False")
                        print("telaUSErR:")
                        return  render_template("TelaUser.html", sess=session['User'],jog=session['Jogo'], data = data, flag = "True")
                    except Exception as ax:

                        print("exceção=" , ax)
                if dataP != "" and typeP == "Partida":
                    print("Partidasssa:")
                return  render_template("TelaUser.html", sess=session['User'],jog=session['Jogo'], data = data, flag = "False")
            game = request.form.get("jogo")
            if 'Admin' in session:
                return redirect(url_for("loginAdm"))
            if game != None:
                session["Jogo"] = game
                return redirect(url_for("login"))
            return  render_template("TelaJogos.html")
    if request.method == "POST":
        session.permanent = True
        try:
            nomeUser = request.form.get("nomeUser")
            senhaUser = request.form.get("senhaUser")
            senha = crud.seleciona_um("usuario", nomeUser)
            print("senha",senha)
            if senha == ():
                print("usuario não encontrado!")
                return  render_template("TelaR.html", data="usuario não encontrado!")
            elif senha!= None and senha[0][3] == senhaUser and nomeUser!=None:
                session["User"] = nomeUser
                return redirect(url_for("login"))
            else:
                print("senha invalida")
                return  render_template("TelaR.html", data="Senha invalida!")

        except Exception as ax:
            print(ax)
    return  render_template("TelaLogin.html")

@app.route("/CadastroAdmin",methods=["GET","POST"])
def CadastroAdmin():
    if request.method == "POST":
        nomeComp = request.form.get("nomeComp")
        nomeUser = request.form.get("nomeUser")
        email = request.form.get("email")
        senha = request.form.get("senha")
        acessKey = request.form.get("acessKey")
        if acessKey=="" or acessKey.find(":")==-1:
            print("formato invalido")
        else:
            id = acessKey.split(":")
            print(id)
            cursor = cmx.connection.cursor()
            string_sql = f"SELECT chave FROM administrador WHERE IDadministrador = '{id[0]}'"
            cursor.execute(string_sql)
            chave = cursor.fetchall()
            if id == None or chave == ():
               print("chave sem correspondencia")
            elif chave[0][0] == id[1]:
                print("chave aceita!")
                cursor = cmx.connection.cursor()
                string_sql = f"UPDATE administrador SET nome = '{nomeComp}', user = '{nomeUser}',  senha = '{senha}', email='{email}' WHERE IDadministrador = {id[0]}"
                cursor.execute(string_sql)
                cmx.connection.commit()
                # print(string_sql)
                # print(ADICIONAR FLAGS!!!!)
                return redirect(url_for("loginAdm"))
            else:
                print("chave não aceita!")
    return  render_template("CadastroAdmin.html")

@app.route("/loginAdm",methods=["GET","POST"])
def loginAdm():
    if 'Admin' in session:
        print("homimacaco")
        return redirect(url_for("telaAdm"))
    if request.method == "POST":
        session.permanent = True
        try:
            nomeUser = request.form.get("nomeUser")
            senhaUser = request.form.get("senhaUser")
            cursor = cmx.connection.cursor()
            string_sql = f"SELECT user,senha FROM administrador WHERE user = '{nomeUser}'"
            cursor.execute(string_sql)
            senha = cursor.fetchall()
            if senha == ():
                print("usuario não encontrado!")
                alerta = "usuario não encontrado!"
                return  render_template("LoginAdm.html", flag = "True")
            elif senha!= None and senha[0][1] == senhaUser and nomeUser!=None:
                print("entro")
                session["User"] = nomeUser
                session["Admin"] = nomeUser
                return redirect(url_for("telaAdm"))
            else:
                print("senha invalida")
                alerta = "Senha invalida!"
                return  render_template("LoginAdm.html",  flag = "True")

        except Exception as ax:
            print(ax)
    return  render_template("LoginAdm.html", flag="False")

@app.route("/telaAdm")
def telaAdm():
    if 'Admin' in session:
        return  render_template("TelaAdmin.html", sess=session['Admin'])
    return redirect(url_for("login"))


@app.route("/CadastroUsuario",methods=["GET","POST"])
def CadastroUsuario():
    if request.method == "POST":
        try:
            alerta = crud.adiciona("usuario",[request.form.get("nomeUser"), request.form.get("nomeComp"), request.form.get("email"), request.form.get("senha")])
            print(alerta)
            if alerta[0] == 200:
                return  render_template("TelaLogin.html")
        except Exception as ax:
            print(ax)
    return  render_template("CadastroUsuario.html")

@app.route("/CadastroJogo",methods=["GET","POST"])
def CadastroJogo():
    return  render_template("CadastroJogo.html")

@app.route("/pb",methods=["GET","POST"])
def pbt():
    return  render_template("pb.html")

@app.route("/load/<tabela>",methods=["GET","POST"]) 
def load(tabela): 
    print("tabela:",tabela) 
    headings = ("name", "role", "salario") 
    data =( 
        ("rolf","software eng","400"), 
        ("juca","mecanico","2200"), 
        ("hugo","goleiro","600"), 
        ("rafa","motovlog","2600") 
    ) 
    return  render_template("/tabelasAdm/" + tabela +  ".html",data=data, headings=headings)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

# @app.route("/teste",methods=["GET","POST"])
# def hello2():
#     if request.method == "POST":
#         email = request.form.get("entradaEmail")
#         senha = request.form.get("entradaSenha")
#         cursor = cmx.connection.cursor()
#         string_sql = f"INSERT INTO usuario (email,senha) VALUES ('{email}','{senha}')"
#         cursor.execute(string_sql)
#         cmx.connection.commit()
#         print(email, senha)
#     return  render_template("teste.html")

if __name__ == "__main__":
    app.config.from_object(config["gabconfig"])
    app.run()
    