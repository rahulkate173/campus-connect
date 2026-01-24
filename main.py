from flask import Flask , render_template,redirect,url_for,request
import uvicorn 

app = Flask(__name__)

@app.route("/check")
def main():
    return {""
    "response":"Hello from campus-connect",
    "status":200
    }

@app.route("/")
def home():
    """Home-page"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost",port=8000,debug=True)
    
