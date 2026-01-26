from os import getenv
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_socketio import SocketIO, emit
from repository import SQLAlchemyRepository 
from sheets import write_quotations_csv
from utils import copy_buyer_script_to_clipboard
from services import quotation as quotation_services
from services import request_for_quotation as request_for_quotation_services
# config
app = Flask(__name__)
socketio = SocketIO(app)
engine = create_engine("sqlite:///request_for_quotations.db", echo=False)
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
    try:
        with engine.begin() as conn:
            repo = SQLAlchemyRepository(conn)
            default_quotation_status: int = repo.get_default_status_id()
            data["status_id"] = default_quotation_status
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
    result = request_for_quotation_services.list_request_for_quotation(engine)
    return render_template(
        "request_for_quotation_list.html",
        requests_with_quotations_count=result["requests_with_quotations_count"],
        active_request_for_quotation_id=result["id"]
    )

@app.post("/")
def create_request_cotations():
    request_for_quotation_services.store_request_for_quotation(engine, request.form)
    return redirect(url_for("list_requests_for_quotations"))

@app.get("/request_for_quotation/<int:request_for_quotation_id>")
def edit_request_for_quotation(request_for_quotation_id: int):
    request_for_quotation = request_for_quotation_services.get_request_for_quotation_by_id(engine, request_for_quotation_id)
    return render_template(
        "request_for_quotation_edit.html",
        request_for_quotation=request_for_quotation
    )

@app.post("/request_for_quotation/<int:request_for_quotation_id>")
def update_request_cotations(request_for_quotation_id: int):
    is_discarted = request.form.get('is_discarted') is not None
    data = dict(request.form)
    data["is_discarted"] = is_discarted
    request_for_quotation_services.update_request_for_quotation(engine, request_for_quotation_id, data)
    return redirect(url_for("edit_request_for_quotation", request_for_quotation_id=request_for_quotation_id))


@app.get("/request/<int:request_for_quotation_id>")
def list_quotations(request_for_quotation_id: int):
    query = request.args.get("query", None) 
    fields_to_exclude = request.args.getlist('fields_to_exclude_if_null')
    quotation_status_id = request.args.getlist('quotation_status_id')

    result = quotation_services.get_quotation_list_data(
        engine=engine,
        request_for_quotation_id=request_for_quotation_id,
        query=query,
        quotation_status=quotation_status_id,
        fields_to_exclude=fields_to_exclude
    )
    
    return render_template(
        "quotation_list.html",
        quotations=result["quotations"],
        request_for_quotation=result["request"],
        quotation_status=result["quotation_status"],
        css_status=result["css_status"]
    )

@app.post("/request/<int:request_for_quotation_id>/generate-cotation-csv")
def generate_quotations_csv(request_for_quotation_id: int):
    try:
        with engine.begin() as conn:
            request_for_quotation_with_related_quotations = SQLAlchemyRepository(conn).get_request_for_quotation_and_filter_its_related_quotations_by_id(request_for_quotation_id)
            path = write_quotations_csv(request_for_quotation_with_related_quotations) 
    except Exception as e:
        print(str(e))
        return jsonify({"message": f"we had an error: {str(e)}"}), 400

    return jsonify({"message": f"=D cotations csv generated at {path}"})

@app.get("/quotation/<int:quotation_id>")
def edit_quotation(quotation_id: int):
    result = quotation_services.get_quotation_edit_data(engine, quotation_id)
    return render_template(
        "quotation_edit.html",
        quotation=result["quotation"],
        quotation_status=result["status"]
    )

@app.post("/quotation/<int:quotation_id>")
def update_quotation(quotation_id: int):
    quotation_services.update_quotation(engine, quotation_id, request.form)
    return redirect(url_for("edit_quotation", quotation_id=quotation_id))

# events
@socketio.event
def update_active_request_for_quotation(data):
    with engine.begin() as conn:
        SQLAlchemyRepository(conn).change_active_request_for_quotation(data["id"])
    emit("reload_page")
 
@socketio.event
def delete_request_for_quotation(data):
    with engine.begin() as conn:
        SQLAlchemyRepository(conn).delete_request_for_quotation_by_id(data["id"])
    emit("reload_page")

# custom flask commands
@app.cli.command("start_db")
def start_db():
    from schema import metadata
    metadata.create_all(engine)
    from fake import quotation_status 
    
    # create quotation status
    with engine.begin() as conn:
        repo =  SQLAlchemyRepository(conn)

        for status in quotation_status:
            repo.store_quotation_status(**status)

@app.cli.command("start_and_seed_db")
def start_and_seed_db():
    """
    create and intitialize database using fake data 
    """
    from schema import metadata
    from fake import fake_request_for_quotations, quotation_status 
    metadata.create_all(engine)

    with engine.begin() as conn:
        repo =  SQLAlchemyRepository(conn)
        # create quotation status
        for status in quotation_status:
            repo.store_quotation_status(**status)

        for request in fake_request_for_quotations:
            # create fake request for quotations
            request_id = repo.store_request_for_quotation(**request["request"])
            repo.set_active_request_for_quotation_id(request_id)
            for quotation in request["quotations"]:
                
                # create fake quotations
                repo.store_quotation(quotation)


if __name__=="__main__":
    socketio.run(app)