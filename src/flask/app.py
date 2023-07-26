from flask import Flask, render_template
from config import Config
from models import StarUser
app = Flask(import_name=__name__, template_folder='templates')

@app.route('/')
def render():
    return render_template("index.html", StarUser= )
if __name__ == '__main__':
    app.run(debug=True)