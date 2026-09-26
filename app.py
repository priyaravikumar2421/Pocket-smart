from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

expenses = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    expenses.append(data)
    return jsonify({"success": True, "expenses": expenses})

@app.route('/get-insights', methods=['POST'])
def get_insights():
    data = request.json
    income = data.get('income', 0)
    total_spent = sum([float(e.get('amount',0)) for e in expenses])
    expense_text = ", ".join([f"{e['category']}: {e['amount']}" for e in expenses])
    prompt = f"You are PocketSmart AI. Income: {income}, Expenses: {expense_text}, Total: {total_spent}. Give 3 saving tips in Tamil+English mix."
    try:
        if API_KEY:
            response = model.generate_content(prompt)
            ai_reply = response.text
        else:
            saving = float(income) - total_spent
            ai_reply = f"Total Spent: {total_spent}. Remaining: {saving}. Tip: 50/30/20 rule follow pannunga!"
        return jsonify({"success": True, "insights": ai_reply, "total": total_spent})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)s