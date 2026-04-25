from flask import Flask, request, jsonify
import requests
import os
import csv
from io import StringIO

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
def get_usd_to_czk():
    """
    Get the current exchange rate from USD to CZK using exchangerate.host API.
    """
    url = "https://open.er-api.com/v6/latest/USD"
    r = requests.get(url, timeout=10)
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
    symbols: A list of stock symbols (e.g., ["AAPL", "GOOGL", "MSFT"]) and optionally with quantities (e.g., ["AAPL:10", "GOOGL:5", "MSFT:20"]).
    """
    try:
        total = 0
        details = []

        for item in symbols:
            if ":" in item:
                sym, qty = item.split(":")
                qty = int(qty)
            else:
                sym = item
                qty = 1

            data = get_stock_price(sym)
            price = data["regularMarketPrice"]

            value = price * qty
            total += value

            details.append({
                "symbol": sym,
                "quantity": qty,
                "price": price,
                "value": round(value, 2)
            })

        for stock in details:
            stock["weight_percent"] = round((stock["value"] / total) * 100, 2)

        return {
            "portfolio_value_usd": round(total, 2),
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

def compound_interest(query):
    try:
        principal, annual_rate, years = query.split(",")
        principal = float(principal)
        annual_rate = float(annual_rate) / 100
        years = int(years)

        final_amount = principal * ((1 + annual_rate) ** years)
        profit = final_amount - principal

        return {
            "principal": principal,
            "annual_rate_percent": annual_rate * 100,
            "years": years,
            "final_amount": round(final_amount, 2),
            "profit": round(profit, 2)
        }
    except Exception as e:
        return {"ERR": str(e)}


def monthly_investment(query):
    try:
        monthly_payment, annual_rate, years = query.split(",")
        monthly_payment = float(monthly_payment)
        monthly_rate = (float(annual_rate) / 100) / 12
        months = int(years) * 12

        final_amount = monthly_payment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        invested_amount = monthly_payment * months
        profit = final_amount - invested_amount

        return {
            "monthly_payment": monthly_payment,
            "annual_rate_percent": float(annual_rate),
            "years": int(years),
            "invested_amount": round(invested_amount, 2),
            "final_amount": round(final_amount, 2),
            "profit": round(profit, 2)
        }
    except Exception as e:
        return {"ERR": str(e)}


def loan_cost(query):
    try:
        principal, annual_rate, years = query.split(",")
        principal = float(principal)
        monthly_rate = (float(annual_rate) / 100) / 12
        months = int(years) * 12

        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
        total_paid = monthly_payment * months
        total_interest = total_paid - principal

        return {
            "loan_amount": principal,
            "annual_rate_percent": float(annual_rate),
            "years": int(years),
            "monthly_payment": round(monthly_payment, 2),
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2)
        }
    except Exception as e:
        return {"ERR": str(e)}

@app.route('/')
def home():
    q_summary = request.args.get("queryStockSummary")
    q_portfolio = request.args.get("queryPortfolioValue")
    q_fx = request.args.get("queryStockWithFX")
    q_eval_opportunity = request.args.get("queryEvaluateOpportunity")
    q_compound = request.args.get("queryCompoundInterest")
    q_monthly = request.args.get("queryMonthlyInvestment")
    q_loan = request.args.get("queryLoanCost")

    if q_summary:
        return jsonify(stock_summary(q_summary))

    if q_portfolio:
        symbols = q_portfolio.split(",")
        return jsonify(portfolio_value(symbols))

    if q_fx:
        return jsonify(stock_with_fx(q_fx))

    if q_eval_opportunity:
        return jsonify(evaluate_opportunity(q_eval_opportunity))

    if q_compound:
        return jsonify(compound_interest(q_compound))

    if q_monthly:
        return jsonify(monthly_investment(q_monthly))

    if q_loan:
        return jsonify(loan_cost(q_loan))

    return jsonify({
        "message": "Use queryStockSummary, queryPortfolioValue, queryStockWithFX, queryEvaluateOpportunity, queryCompoundInterest, queryMonthlyInvestment or queryLoanCost query parameters."
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
            "queryEvaluateOpportunity",
            "queryCompoundInterest",
            "queryMonthlyInvestment",
            "queryLoanCost"
        ]
    }