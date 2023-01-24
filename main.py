from website import create_app

# main file that runs the flask app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)