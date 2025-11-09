from flask import Flask, jsonify
from flask import redirect
from flask import render_template
from flask import request 
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging

# app_log = logging.getLogger(__name__)
# logging.basicConfig(
#     filename="main_security_log.log",
#     encoding="utf-8",
#     level=logging.DEBUG,
#     format="%(asctime)s %(message)s",
# )

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"secretsesameseeds"

app_header = {"Authorisation": "isaysopensesame"}

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/add.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        hyperlink = request.form["hyperlink"]
        about = request.form["about"]
        image = request.form["image"]
        language = request.form["language"]
        data = {
            "name": name,
            "hyperlink": hyperlink,
            "about": about,
            "image": image,
            "language": language,
        }
        app.logger.critical(data)
        try:
            response = requests.post(
                "http://127.0.0.1:3000/add_extension",
                json=data,
                headers=app_header,
            )
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": "Failed to retrieve data from the API"}
        return render_template("/add.html", data=data)
    else:
        return render_template("/add.html", data={})

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
    url = "http://127.0.0.1:3000"
    if request.args.get("lang") and request.args.get("lang").isalpha():
        lang = request.args.get("lang")
        url += f"?lang={lang}"
    try:
        response = requests.get(url)
        response.raise_for_status()  #http GET request
        data = response.json()        #parse JSON response
    except requests.exceptions.RequestException as e:
        data = {"error": "Failed to retrieve data from the API"}
    return render_template("/index.html", data=data)

@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True)