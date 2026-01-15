from flask import Flask, jsonify, request, render_template, redirect, url_for
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

# temp_fake_repository_data
request_cotations = [
    {"id": 1, "title": "un nombre"},
    {"id": 2, "title": "otro nombre"},
]

selected_request_cotations = [
    {"request_cotation_id" :None}
]

cotations = []

# temp_fake_service
def store_request_cotation(title: str):
    request_cotations.append({
        "id": sorted(request_cotations, key=lambda x: x["id"], reverse=True)[0]["id"] + 1,
        "title": title 
    })
    # db will return last id
    id = request_cotations[-1]["id"]
    set_selected_request_cotation_id(id)

def store_cotation(cotation_data):
    request_cotation_id = get_selected_request_cotation_id()
    save_cotation_in_db(cotation_data)

# fake repository functions
def save_cotation_in_db(request_cotation_id, cotation_data):
    new_cotation = {
        "company_name":cotation_data["company_name"],
        "company_url":cotation_data["company_url"],
        "product_name":cotation_data["product_name"],
        "product_url":cotation_data["product_url"],
        "public_minimum_price":cotation_data["public_minimum_price"],
        "public_minimum_quantity":cotation_data["public_minimum_quantity"],
        "request_cotation_id":request_cotation_id
    }
    cotations.append(new_cotation)

# custom query for get count cotations for each request
def get_request_cotations_with_cotations_count():
    fetched_request_cotations = []
    for request_cotation in request_cotations:
        fetched_request_cotations.append({
            "request":request_cotation,
            "cotations_count": get_cotations_count_for_request_cotation(request_cotation["id"])
        })
    return fetched_request_cotations

def get_request_cotation_with_related_cotations(request_cotation_id:int):
    # call db for get request cotation
    request_cotation = get_request_cotation_by_id(request_cotation_id)
    cotations = get_cotations_count_for_request_cotation(request_cotation["id"])
    return {
        "request": request_cotation,
        "cotations": cotations
    }

def get_request_cotation_by_id(request_cotation_id):
    for request_cotation in request_cotations:
        if request_cotation.get("id") == request_cotation_id:
            return request_cotation    
    raise Exception("request cotation id not found")

# auxiliar fake simple WHERE clause  
def get_cotations_for_request_cotation(request_cotation_id:int) -> list:
    return list(filter(lambda x: x["request_cotation_id"] == request_cotation_id, cotations))

# auxiliar fake simple COUNT agreggate function  
def get_cotations_count_for_request_cotation(request_cotation_id:int):
    return len(get_cotations_for_request_cotation(request_cotation_id))

def get_selected_request_cotation_id():
    return selected_request_cotations[0]["request_cotation_id"]

def set_selected_request_cotation_id(id: int) -> None:
    selected_request_cotations[0]["request_cotation_id"] = id

# @app.post("/webhook")
# def webhook():
#     data = request.get_json()   # ← aquí lees el JSON
#     try:
#         request_cotation = store_cotation_in_db(data)
#     except RequestCotationDosentExist as e:
#         return jsonify({"message": e.message}), 400

#     print(data)
#     return jsonify({"message": "funciono!"})

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@app.get("/test-websockets")
def test_websockets():
    title = request.args.get("title")
    id = request.args.get("id")
    print(title, id)

@app.get("/")
def list_request_cotations():
    # get request cotations from servcies
    # get selected request cotation from services
    id = get_selected_request_cotation_id()
    request_cotations = get_request_cotations_with_cotations_count()
    # render html with listing of request cotation
    return render_template("request_cotation_list.html", request_cotations=request_cotations, selected_request_cotation_id=id)

@app.post("/")
def create_request_cotations():
    # validate data of request cotation
    title = request.form.get("title", None)

    # store request cotation    
    store_request_cotation(title)
    return redirect(url_for("list_request_cotations"))

@app.get("/request/<int:request_cotation_id>")
def list_cotations(request_cotation_id: int):
    # get request cotation with all cotations associated from servcies: raise error if not exists
    request_cotation_with_cotations = get_request_cotation_with_related_cotations(request_cotation_id)
    # get  with request
    return render_template("cotation_list.html", request_cotation_with_cotations)

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