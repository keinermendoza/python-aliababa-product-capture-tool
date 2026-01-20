from os import getenv
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_socketio import SocketIO, emit
from repository import SQLAlchemyRepository 
from sheets import write_cotations_csv
from utils import copy_buyer_script_to_clipboard

# config
app = Flask(__name__)
socketio = SocketIO(app)
engine = create_engine("sqlite:///request_cotations.db", echo=False)
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

#routes
@app.post("/webhook")
def webhook():
    data = request.get_json()
    print(data)
    try:
        with engine.begin() as conn:
            repo = SQLAlchemyRepository(conn)
            repo.store_quotation(data)
            request_for_quotation = repo.get_request_for_quotation_by_id(
                repo.get_active_request_for_quotation_id()
            )
            socketio.emit("reload_page")
            
        copy_buyer_script_to_clipboard(
            buyer_name=getenv("BUYER_NAME"),
            buyer_address=getenv("BUYER_ADDRESS"),
            quantity_requested=request_for_quotation.quantity,
            product_name=data["product_name"]
        )
        
    except Exception as e:
        print("Exception was raised: ", e)
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "funciono!"})

@app.get("/")
def list_requests_for_quotations():
    with engine.begin() as conn:
        repo = SQLAlchemyRepository(conn)
        id = repo.get_active_request_for_quotation_id()
        requests_with_quotations_count = repo.get_request_for_quotations_with_quotations_count()

    return render_template(
        "request_for_quotation_list.html",
        requests_with_quotations_count=requests_with_quotations_count,
        active_request_for_quotation_id=id
    )

@app.post("/")
def create_request_cotations():
    title = request.form.get("title", None)
    quantity = request.form.get("quantity", None)

    with engine.begin() as conn:
        repo = SQLAlchemyRepository(conn)
        request_for_quotations_id = repo.store_request_for_quotation(title, quantity)
        repo.set_active_request_for_quotation_id(request_for_quotations_id)
    
    return redirect(url_for("list_requests_for_quotations"))

@app.get("/request/<int:request_for_quotation_id>")
def list_quotations(request_for_quotation_id: int):
    query = request.args.get("query", None) 
    with engine.begin() as conn:
        request_for_quotation_with_related_quotations = SQLAlchemyRepository(
            conn
        ).get_request_for_quotation_and_filter_its_related_quotations_by_id(request_for_quotation_id, query)
    
    return render_template(
        "quotation_list.html",
        request_for_quotation_with_related_quotations=request_for_quotation_with_related_quotations
    )

@app.post("/request/<int:request_for_quotation_id>/generate-cotation-csv")
def generate_quotations_csv(request_for_quotation_id: int):
    try:
        with engine.begin() as conn:
            request_for_quotation_with_related_quotations = SQLAlchemyRepository(conn).get_request_for_quotation_and_filter_its_related_quotations_by_id(request_for_quotation_id)
            path = write_cotations_csv(request_for_quotation_with_related_quotations) 
    except Exception as e:
        return jsonify({"message": f"we had an error: {e.message}"}), 400

    return jsonify({"message": f"=D cotations csv generated at {path}"})

@app.get("/quotation/<int:quotation_id>")
def edit_quotation(quotation_id: int):
    quotation = None
    try:
        with engine.begin() as conn:
            quotation = SQLAlchemyRepository(conn).get_quotation_by_id(quotation_id)
    # TODO: replace for custom Exception as QuotationNotFound
    except Exception as e:
        # TODO: replace for emit event
        # - also add event listener for show card with exception message in client
        print(str(e)) 

    return render_template(
        "quotation_edit.html",
        quotation=quotation
    )

@app.post("/quotation/<int:quotation_id>")
def update_quotation(quotation_id: int):
    try:
        with engine.begin() as conn:
            repo = SQLAlchemyRepository(conn)
            quotation = repo.get_quotation_by_id(quotation_id)
            repo.update_quotation(
                quotation=quotation,
                data=request.form   
            )

    # TODO: replace for custom Exception as QuotationNotFound
    except Exception as e:
        # TODO: replace for emit event
        # - also add event listener for show card with exception message in client
        print(str(e)) 

    return redirect(url_for("edit_quotation", quotation_id=quotation.id))


# events
@socketio.event
def update_active_request_for_quotation(data):
    with engine.begin() as conn:
        SQLAlchemyRepository(conn).change_active_request_for_quotation(data["id"])
    emit("reload_page")
 
# flask commands
@app.cli.command("start_db")
def start_db():
    from schema import metadata
    metadata.create_all(engine)

if __name__=="__main__":
    socketio.run(app)