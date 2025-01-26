from app import app

@app.route('/')
def hola():
    return 'Hola'

@app.route('/saludo/<nombre>')
def saludo(nombre):
    contenido = """
        <html>
            <head>
                <title>Saludo</title>
            </head>
            <body>
                <h1>Saludo a {}</h1>
            </body>
        </html>
    """
    return contenido.format(nombre)