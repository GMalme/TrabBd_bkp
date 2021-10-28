from app import cmx

variaveis = {
    'usuario': f"INSERT INTO usuario (user, nome, senha, email, status_user) VALUES ('%s', '%s', '%s', '%s', 'false')",
    'administrador': f"INSERT INTO administrador (user, nome, senha, email, chave) VALUES ('%s', '%s', '%s', '%s', '%s')",
    'seleciona_um' :f"SELECT %s FROM %s WHERE %s = '%s'",
    'atualiza' : f"UPDATE %s SET user = '%s', nome = '%s',  senha = '%s', email='%s', chave='' WHERE IDadministrador = %s",
    'exclui'    : f"DELETE FROM %s WHERE %s='%s'"
}

# Retorna um
def seleciona_um(id, select ="*", tipo = 'administrador', atributo = 'IDadministrador'):
    try:
        cursor = cmx.connection.cursor()
        print("selecionaum=",variaveis["seleciona_um"]%(select,tipo, atributo, id))
        cursor.execute(variaveis["seleciona_um"]%(select,tipo, atributo, id))
        data = cursor.fetchall()
        return data
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
def adiciona(tipo, data):
    val = valida(tipo, data) if (tipo == "usuario" or tipo == "administrador") else 200
    print("testinha:",variaveis[tipo]%data)
    print("val:",val)
    if val[0] == 200:
        cursor = cmx.connection.cursor()
        cursor.execute(variaveis[tipo]%data)
        cmx.connection.commit()
        return val
    else:
        return val
        
# Atualiza 
def atualiza(tipo,data,id):
    val = valida(tipo, data) if (tipo == "usuario" or tipo == "administrador") else 200
    if val[0] == 200:
        print("atualiza=",variaveis['atualiza']% (tipo,data[0],data[1],data[2],data[3],id))
        cursor = cmx.connection.cursor()
        cursor.execute(variaveis['atualiza']% (tipo,data[0],data[1],data[2],data[3],id))
        cmx.connection.commit()
        return val
    else:
        return val

# Exclui
def exclui(tipo, id, atributo = "user"):
    if(seleciona_um(id,"*",tipo,atributo)[0] != 400):
        cursor = cmx.connection.cursor()
        print("exclui=",variaveis["seleciona_um"]%(tipo, atributo, id))
        cursor.execute(variaveis["exclui"]%(tipo, atributo, id))
        cmx.connection.commit()
        return 200,'usuario excluido!'
    else:
        return 400,'usuario não encontrado!'

#Valida
def valida(tipo, data):
    for dado in data:
        if dado == "":
            return (400, "Preenchimento Invalido!")
    if seleciona_um(data[0],"*",tipo,"user") != ():
        print("vadalida:",seleciona_um(data[0],"*",tipo,"user"))
        return (403, "Id Proibido!")
    return (200, "Preenchimento Valido")
