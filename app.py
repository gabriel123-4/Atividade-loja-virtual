# Importa as funções necessárias do Flask
from flask import Flask, render_template, request, redirect, url_for

# Importando a biblioteca do mysql
import mysql.connector

# Cria a aplicação Flask
app = Flask(__name__)

# Configurando a conexão do banco de dados MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",      # endereço do servidor MySQL
        port=3306,             # porta padrão do MySQL
        user="root",           # troque pelo seu usuário
        password="senai",      # troque pela sua senha
        database="bdprodutos"  # nome do seu banco de dados
    )


# ------------------------------------------------------
# ROTAS DA NOSSA APLICAÇÃO
# ------------------------------------------------------


# ------------------------------------------------------
# ROTAS DE PRODUTOS
# ------------------------------------------------------

# Rota para cadastrar um novo PRODUTO
@app.route('/')
def index():
    return render_template("/produtos/cadastro.html")

@app.route("/produtos/cadastrar", methods=["GET", "POST"])
def cadastrarProduto():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        fabricante = request.form["fabricante"]

        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = """
                INSERT INTO TBPRODUTOS (NOME, DESCRICAO, PRECO, FABRICANTE)
                VALUES (%s, %s, %s, %s)
            """
            valores = (nome, descricao, preco, fabricante)

            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

            # Exibe alert e redireciona via JavaScript
            return """
                <script>
                    alert("Produto cadastrado com sucesso!");
                    window.location.href = "/produtos/cadastrar";
                </script>
            """

        except Exception as e:
            # Exibe um alert no navegador em caso de erro
            return f"""
                <script>
                    alert("Erro ao cadastrar produto: {str(e)}");
                    window.history.back();
                </script>
            """

    else:
        # Exibe o formulário normalmente
        return render_template("/produtos/cadastro.html")

# ------------------------------------------------------
# Inicia o servidor Flask se rodar o arquivo direto
# ------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)  # debug=True atualiza automaticamente a cada alteração
