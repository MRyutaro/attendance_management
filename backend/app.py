from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"This is": "root"}


@app.get("/api")
def read_api():
    return {"This is": "api"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)

# from flask import Flask, jsonify

# app = Flask(__name__)


# @app.route('/api/profile', methods=["GET"])
# def index():
#     return jsonify({"users": [
#         {"id": 1, "name": 'MuneyukiSakataaaaaaaaaaaaaa', "email": 'aaaa.com'},
#         {"id": 2, "name": 'Ryutaro00000000000000000000', "email": 'bbbbbbb.com'},
#         {"id": 3, "name": 'Nicoooooooooooooooooooooorn', "email": 'ccccccc.com'}
#     ]})
