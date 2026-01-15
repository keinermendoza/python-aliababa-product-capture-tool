from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_socketio import SocketIO
# from services import (
    # get_current_request_cotation,
    # save_cotation_in_db,
    # RequestCotationDosentExist
# )

app = Flask(__name__)
socketio = SocketIO(app)
engine = create_engine("sqlite:///request_cotations.db", echo=True)

CORS(
    app,
    resources={
        r"/webhook": {
            "origins": ["https://www.alibaba.com"]
        }
    },
    allow_headers=["Content-Type"],
    methods=["POST", "OPTIONS"]
)

request_cotations = [
    {"id": 1, "name": "un nombre"},
    {"id": 2, "name": "otro nombre"},
]

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@app.get("/test-websockets")
def test_websockets():
    name = request.args.get("name")
    id = request.args.get("id")
    print(name, id)

# @app.post("/webhook")
# def webhook():
#     data = request.get_json()   # ← aquí lees el JSON
#     try:
#         request_cotation = save_cotation_in_db(data)
#     except RequestCotationDosentExist as e:
#         return jsonify({"message": e.message}), 400

#     print(data)
#     return jsonify({"message": "funciono!"})


@app.get("/")
def list_request_cotations():
    # get request cotations from servcies
    
    # render html with listing of request cotation
    return render_template("list.html", request_cotations=request_cotations)

@app.post("/")
def create_request_cotations():
    # validate data of request cotation
    # store request cotation    
    pass

@app.get("/request/<int:request_cotation_id>")
def list_cotations(request_cotation: int):
    # get request cotation from servcies: : raise error if not exists
    # get all cotations associated with request
    # render html with listing of request cotations
    pass

@app.post("/request/<int:request_cotation_id>/select")
def select_request_cotations(request_cotation_id: int):
    # get request cotation from servcies: raise error if not exists
    # update value of unique selected request instance
    pass

@app.cli.command("start_db")
def start_db():
    from schema import metadata
    metadata.create_all(engine)

if __name__=="__main__":
    socketio.run(app)