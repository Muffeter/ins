from flask import Flask, render_template
app = Flask(import_name=__name__, template_folder='templates')

@app.route('/')
def render():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)