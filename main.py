# from flask import Flask , render_template,redirect,url_for,request
# import uvicorn 
# from parents import create_app
# app = Flask(__name__)
# @app.route("/check")
# def main():
#     return {""
#     "response":"Hello from campus-connect",
#     "status":200
#     }

# @app.route("/")
# def home():
#     """Home-page"""
#     return render_template("index.html")

# @app.route("/parents")
# def parents():
#     parents = create_app()
#     parents.run(host="localhost",port=8000,debug=True)



# if __name__ == "__main__":
#     app.run(host="localhost",port=8000,debug=True)
    
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
