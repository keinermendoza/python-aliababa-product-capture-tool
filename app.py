from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_socketio import SocketIO, emit
from repository import (
    get_selected_request_cotation_id,
    set_selected_request_cotation_id,
    change_selected_request_cotation,
    store_request_cotation,
    store_cotation,
    get_request_cotations_with_cotations_count,
    get_request_cotation_with_related_cotations
)
from sheets import write_cotations_csv

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
    data = request.get_json()
    try:
        with engine.begin() as conn:
            store_cotation(conn, data)
            socketio.emit("reload_page")
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "funciono!"})

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
    quantity = request.form.get("quantity", None)

    with engine.begin() as conn:
        request_cotation_id = store_request_cotation(conn, title, quantity)
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

@app.post("/request/<int:request_cotation_id>/generate-cotation-csv")
def generate_cotation_csv(request_cotation_id: int):
    try:
        with engine.begin() as conn:
            request_cotation_with_cotations = get_request_cotation_with_related_cotations(conn, request_cotation_id)
            path = write_cotations_csv(request_cotation_with_cotations) 
    except Exception as e:
        return jsonify({"message": f"we had an error: {e.message}"}), 400

    return jsonify({"message": f"=D cotations csv generated at {path}"})

@socketio.event
def update_selected_request_cotation(data):
    with engine.begin() as conn:
        change_selected_request_cotation(conn, data["id"])
    emit("reload_page")
 
@app.cli.command("start_db")
def start_db():
    from schema import metadata
    metadata.create_all(engine)

if __name__=="__main__":
    socketio.run(app)