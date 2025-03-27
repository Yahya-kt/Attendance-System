from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
import csv
import datetime
import os
import pandas as pd

app = Flask(__name__, template_folder="../frontend")
CORS(app)

csv_file = "./database/attendance.csv"
os.makedirs(os.path.dirname(csv_file), exist_ok=True)
if not os.path.isfile(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Text","Timestamp"])


@app.route('/')
def form():
    return render_template('index.html')

@app.route('/mark', methods=['POST'])
def mark():
    text_value = request.form.get('text')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([text_value, timestamp])

    return f'attendance marked :"{text_value}" at {timestamp}' 

@app.route('/dashboard',methods=['GET'])
def dashboard():
    try:
        df = pd.read_csv('./database/attendance.csv')
        df.fillna("",inplace=True)
        if df.empty:
            return jsonify([])
        data = df.to_dict(orient="records")
        print("Returning JSON:",data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error":str(e)}),500 

if __name__ == '__main__':
    app.run(debug=True, port=8888)
           
