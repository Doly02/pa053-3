from flask import Flask, request, jsonify
import requests
import csv
from io import StringIO
import ast
import operator as op

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
}
app = Flask(__name__)

PERCENTAGE_THRESHOLD = -5  # Threshold for evaluating investment opportunity

def get_stock_price(symbol):
    """
    Get the current stock price for a given symbol using Yahoo Finance API.
    symbol: The stock symbol to look up (e.g., "AAPL").
    """
    url = f"https://stooq.com/q/l/?s={symbol.lower()}.us&f=sd2t2ohlcv&h&e=csv"
    r = requests.get(url, timeout=10)
    r.raise_for_status()

    reader = csv.DictReader(StringIO(r.text))
    row = next(reader)

    if row["Close"] == "N/D":
        raise ValueError(f"Stock symbol {symbol} was not found")

    price = float(row["Close"])
    open_price = float(row["Open"])

    change_percent = ((price - open_price) / open_price) * 100 if open_price else 0

    return {
        "symbol": symbol.upper(),
        "shortName": symbol.upper(),
        "regularMarketPrice": price,
        "regularMarketChangePercent": change_percent
    }

def evaluate_expression(expression):
    """
    Evaluate a mathematical expression safely using the ast module.
    expression: A string containing the mathematical expression to evaluate (e.g., "2 + 3 * (4 - 1)").
    """

    def eval_node(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(node.op)](eval_node(node.operand))
        if isinstance(node, ast.Expression):
            return eval_node(node.body)

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return eval_node(tree)



def airport_temp(code):
    """
    Get the current temperature in Celsius for a given airport code using wttr.in API.
    code: The IATA airport code (e.g., "PRG" for Prague).
    """
    try:

        airport_url = f"https://airport-data.com/api/ap_info.json?iata={code.upper()}"
        r = requests.get(airport_url, timeout=10)
        airport_data = r.json()

        if "city" not in airport_data:
            raise ValueError("Invalid airport code")

        city = airport_data["city"]

        weather_url = f"https://wttr.in/{city}?format=j1"
        r = requests.get(weather_url, timeout=10)
        weather_data = r.json()

        temp = weather_data["current_condition"][0]["temp_C"]
        return float(temp)

    except Exception:
        return 0

@app.route('/')
def home():
    q_airport = request.args.get("queryAirportTemp")
    q_stock = request.args.get("queryStockPrice")
    q_eval = request.args.get("queryEval")

    if q_airport:
        temp = airport_temp(q_airport)
        if temp is None:
            return jsonify(0)
        
        return jsonify(float(temp))
    if q_stock:
        return jsonify(float(get_stock_price(q_stock)["regularMarketPrice"]))

    if q_eval:
        return jsonify(float(evaluate_expression(q_eval)))

    temp = None
    return jsonify(temp)