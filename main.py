from flask import Flask, render_template, redirect, request, jsonify
import serial
import json
import requests

app = Flask(__name__)
s = serial.Serial("COM9", 9600)


@app.route("/")
def index():
    temp_in, humd_in, temp_out, humd_out = get_data()
    return render_template('index.html', temp_in=temp_in, humd_in=humd_in, temp_out=temp_out, humd_out=humd_out)


@app.route("/turn_on")
def led_on():
    s.write("B".encode("ascii"))
    s.readline()
    return redirect("/")


@app.route("/turn_off")
def led_off():
    s.write("C".encode("ascii"))
    s.readline()
    return redirect("/")


@app.route("/message", methods=['POST'])
def message():
    msg = request.form['msg']
    print('The user said "' + msg + '".')
    lcd = 'W'+msg+'\n'
    s.write(lcd.encode("ascii"))
    return redirect("/")


@app.route("/data.json", methods=['GET'])
def json_data():
    dat = get_data()
    return jsonify(temp_in=dat[0], humd_in=dat[1], temp_out=dat[2], humd_out=dat[3])


def get_data():
    s.write("R".encode("ascii"))
    msg = s.readline().decode("ascii").strip().split(",")
    temp_in = str(msg[0])
    humd_in = str(msg[1])
    r = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=Annapolis&appid=59398f41b4b9294d47cfd27e177d3062')
    vals = r.json()
    temp = vals['main']['temp']
    temp = temp - 273.15
    temp_out ="%.2f"%temp
    humd = vals['main']['humidity']
    humd_out = str(humd)
    return temp_in, humd_in, temp_out, humd_out

app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)
