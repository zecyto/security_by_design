from flask import Flask, render_template



app = Flask("name", template_folder='server/templates')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run('localhost', 3001, True)