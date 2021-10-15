from flask import Flask, render_template, redirect, url_for, request, make_response, session, g, jsonify, flash
import templates
import datetime
import os
import requests



app = Flask(__name__)


@app.route("/entrance", methods=["GET", "POST"])
def entrance():
    if request.method == "POST":
        ticket = requests.post("http://localhost:9000/tickets")
    return render_template("entrance.html", ticket=ticket)


@app.route("/cars", methods=["GET"])
def cars():
    cars = request.get("http://localhost:9000/tickets")
    return render_template("cars.html", cars=cars)



if __name__ == "__main__":
    app.run(debug=True)