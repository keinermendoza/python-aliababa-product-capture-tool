from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_socketio import SocketIO
from services import (
    get_selected_request_cotation_id,
    set_selected_request_cotation_id,
    store_request_cotation,
    store_cotation,
    get_request_cotations_with_cotations_count,
    get_request_cotation_with_related_cotations
)

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

@app.post("/webhook")
def webhook():
    data = request.get_json()   # ← aquí lees el JSON
    try:
        with engine.begin() as conn:
            store_cotation(conn, data)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "funciono!"})

# @socketio.on('message')
# def handle_message(data):
#     print('received message: ' + data)

# @app.get("/test-websockets")
# def test_websockets():
#     title = request.args.get("title")
#     id = request.args.get("id")
#     print(title, id)

@app.get("/")
def list_request_cotations():
    with engine.begin() as conn:
        id = get_selected_request_cotation_id(conn)
        request_cotations = get_request_cotations_with_cotations_count(conn)

    return render_template(
        "request_cotation_list.html",
        request_cotations=request_cotations,
        selected_request_cotation_id=id
    )

@app.post("/")
def create_request_cotations():
    title = request.form.get("title", None)

    with engine.begin() as conn:
        request_cotation_id = store_request_cotation(conn, title)
        set_selected_request_cotation_id(conn, request_cotation_id)
    
    return redirect(url_for("list_request_cotations"))

@app.get("/request/<int:request_cotation_id>")
def list_cotations(request_cotation_id: int):
    with engine.begin() as conn:
        request_cotation_with_cotations = get_request_cotation_with_related_cotations(conn, request_cotation_id)
    
    print(request_cotation_with_cotations)
    return render_template(
        "cotation_list.html",
        request_cotation_with_cotations=request_cotation_with_cotations
    )

# @app.post("/request/<int:request_cotation_id>/select")
# def select_request_cotations(request_cotation_id: int):
    # get request cotation from servcies: raise error if not exists
    # update value of unique selected request instance
    # pass

@app.cli.command("start_db")
def start_db():
    from schema import metadata
    metadata.create_all(engine)

if __name__=="__main__":
    socketio.run(app)