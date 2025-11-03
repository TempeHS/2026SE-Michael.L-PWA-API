from flask import Flask, jsonify
from flask import redirect
from flask import render_template
from flask import request 
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"secretsesameseeds"

app_header = {"Authorisation": "isaysopensesame"}

# @app.route("/get-user/<user_id>")
# def get_user(user_id):
#     user_data = {
#         "user_id": user_id,
#         "name": "John Doe",
#         "email": "john.doe@example.com",
#     }

#     extra = request.args.get("extra")
#     if extra:
#         user_data["extra"] = extra

#     return jsonify(user_data), 200


# @app.route("/create-user", methods=["POST"])
# def create_user():
#     data = request.get_json()

#     return jsonify(data), 201

@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["GET"])
@csp_header(
    {
    "base-uri": "self",
    "default-src": "'self'",
    "style-src": "'self'",
    "script-src": "'self'",
    "img-src": "*",
    "media-src": "'self'",
    "font-src": "self",
    "object-src": "'self'",
    "child-src": "'self'",
    "connect-src": "'self'",
    "worker-src": "'self'",
    "report-uri": "/csp_report",
    "frame-ancestors": "'none'",
    "form-action": "'self'",
    "frame-src": "'none'",
    }
)
def index():
    return render_template("/index.html")

@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True)     