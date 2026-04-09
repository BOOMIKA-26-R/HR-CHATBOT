from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
try:
    df = pd.read_csv("employee_data.csv")
except Exception as e:
    print("Error loading CSV:", e)
    df = None

# Functions
def total_employees():
    return len(df) if df is not None else 0

def avg_salary():
    return df['Salary'].mean() if df is not None else 0

def employees_by_department():
    return df['Department'].value_counts().to_dict() if df is not None else {}

# Webhook for Dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    query = req["queryResult"]["queryText"].lower()

    if "total employees" in query:
        return jsonify({"fulfillmentText": f"Total employees: {total_employees()}"})
    elif "average salary" in query:
        return jsonify({"fulfillmentText": f"Average salary: {avg_salary():.2f}"})
    elif "department count" in query:
        counts = employees_by_department()
        return jsonify({"fulfillmentText": f"Employees per department: {counts}"})
    else:
        return jsonify({"fulfillmentText": "I can answer total employees, average salary, or department count."})

import matplotlib.pyplot as plt
import os

def generate_department_chart():
    counts = df['Department'].value_counts()
    plt.bar(counts.index, counts.values)
    os.makedirs("static", exist_ok=True)
    chart_path = "static/dept_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)