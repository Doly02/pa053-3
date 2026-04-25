from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PERCENTAGE_THRESHOLD = -5  # Threshold for evaluating investment opportunity

def get_stock_price(symbol):
    """
    Get the current stock price for a given symbol using Yahoo Finance API.
    symbol: The stock symbol to look up (e.g., "AAPL").
    """
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    r = requests.get(url)
    data = r.json()
    return data["quoteResponse"]["result"][0]

def get_usd_to_czk():
    """
    Get the current exchange rate from USD to CZK using exchangerate.host API.
    """
    url = "https://api.exchangerate.host/latest?base=USD&symbols=CZK"
    r = requests.get(url)
    data = r.json()
    return data["rates"]["CZK"]

def stock_summary(symbol):
    """
    Get a summary of the stock price and change for a given symbol.
    symbol: The stock symbol to look up (e.g., "AAPL").
    """
    try:
        data = get_stock_price(symbol)
        return {
            "symbol": symbol,
            "price": data["regularMarketPrice"],
            "change": data["regularMarketChangePercent"],
            "name": data.get("shortName", "N/A")
        }
    except Exception as e:
        return {"ERR": str(e)}

def portfolio_value(symbols):
    """
    Calculate the total value of a stock portfolio given a list of stock symbols.
    symbols: A list of stock symbols (e.g., ["AAPL", "GOOGL", "MSFT"]).
    """
    try:
        total = 0
        details = []

        for sym in symbols:
            data = get_stock_price(sym)
            price = data["regularMarketPrice"]
            total += price
            details.append({
                "symbol": sym,
                "price": price
            })

        return {
            "portfolio_value_usd": total,
            "stocks": details
        }
    except Exception as e:
        return {"ERR": str(e)}

def stock_with_fx(symbol):
    """
    Get the stock price in USD and convert it to CZK using the current exchange rate.
    symbol: The stock symbol to look up (e.g., "AAPL").
    """
    try:
        stock = get_stock_price(symbol)
        price_usd = stock["regularMarketPrice"]

        rate = get_usd_to_czk()
        price_czk = price_usd * rate

        return {
            "symbol": symbol,
            "price_usd": price_usd,
            "price_czk": round(price_czk, 2),
            "fx_rate": rate
        }
    except Exception as e:
        return {"ERR": str(e)}
    
def evaluate_opportunity(symbol):
    """
    Evaluate whether the stock is a good investment opportunity based on its price change percentage.
    symbol: The stock symbol to evaluate (e.g., "AAPL").
    """
    try:
        stock = get_stock_price(symbol)
        fx_rate = get_usd_to_czk()

        price_usd = stock["regularMarketPrice"]
        change_percentage = stock.get("regularMarketChangePercent", 0)
        price_czk = price_usd * fx_rate

        if change_percentage < PERCENTAGE_THRESHOLD:
            trend = "falling"
            summary = "The stock is currently falling. This may indicate a short-term dip, but it can also signal increased risk."
        elif change_percentage > -PERCENTAGE_THRESHOLD:
            trend = "rising"
            summary = "The stock is currently rising. It may indicate positive market sentiment, but buying after a strong move can be riskier."
        else:
            trend = "stable"
            summary = "The stock is relatively stable today. There is no strong short-term movement visible from the current price change."

            return {
                "symbol": symbol.upper(),
                "name": stock.get("shortName", "N/A"),
                "price_usd": price_usd,
                "price_czk": round(price_czk, 2),
                "change_percent": round(change_percentage, 2),
                "fx_rate_usd_czk": round(fx_rate, 4),
                "trend": trend,
                "summary": summary
            }

    except Exception as e:
        return {"ERR": str(e)}


@app.route('/')
def home():
    q_summary = request.args.get("queryStockSummary")
    q_portfolio = request.args.get("queryPortfolioValue")
    q_fx = request.args.get("queryStockWithFX")
    q_eval_opportunity = request.args.get("queryEvaluateOpportunity")

    if q_summary:
        return jsonify(stock_summary(q_summary))

    if q_portfolio:
        symbols = q_portfolio.split(",")
        return jsonify(portfolio_value(symbols))

    if q_fx:
        return jsonify(stock_with_fx(q_fx))

    if q_eval_opportunity:
        return jsonify(evaluate_opportunity(q_eval_opportunity))

    return jsonify({
        "message": "Use queryStockSummary, queryPortfolioValue, queryStockWithFX or queryEvaluateOpportunity query parameters to get stock information."
    })

@app.route('/about')
def about():
    return {
        "service": "Investment Helper API",
        "author": "Tomas Dolak",
        "endpoints": [
            "queryStockSummary",
            "queryPortfolioValue",
            "queryStockWithFX",
            "queryEvaluateOpportunity"
        ]
    }