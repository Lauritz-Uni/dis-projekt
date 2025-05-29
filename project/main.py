from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # when debug is true, the server will reload on code changes live. So turn off in production. 
