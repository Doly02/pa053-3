# PA053 Distributed Systems & Middleware: Homework 3
- Author: Tomáš Dolák
- Login: 582959
- Emails: <582959@mail.muni.cz>

## Table of Contents

- [Investment Helper REST API](#investment-helper-rest-api)
  - [Description](#description)
  - [Implemented Endpoints](#implemented-endpoints)
    - [Stock Summary](#stock-summary)
    - [Stock Price with Currency Conversion](#stock-price-with-currency-conversion)
    - [Portfolio Value](#portfolio-value)
    - [Evaluation of Opportunity](#evaluation-of-opportunity)
    - [About](#about)
  - [Running Locally](#running-locally)
  - [Deployment](#deployment)
  - [Notes](#notes)
  - [Resources](#resources)


## Investment Helper REST API
This project implements a simple REST web service deployed on Vercel using Flask.  
The service aggregates data from multiple public APIs and applies custom logic to provide meaningful responses.

### Description

The application demonstrates principles of distributed systems and middleware:
- REST communication over HTTP
- Integration of multiple external services
- Data aggregation and transformation
- Stateless request processing

### Implemented Endpoints

This API integrates with external services to provide comprehensive stock data and currency conversion functionality. It utilizes the `Yahoo Finance` API to retrieve real-time stock prices, percentage changes, and company information, and the `exchangerate.host` API to obtain current USD to CZK exchange rates for accurate currency conversions.

#### Stock Summary
**Endpoint:** `GET /?queryStockSummary={symbol}`  
**Description:** Retrieves a summary of the stock including current price, percentage change, and company name.  
**Example:** `GET /?queryStockSummary=AAPL`  
**Example Response:**  
```json
{
  "symbol": "AAPL",
  "price": 150.25,
  "change": 2.5,
  "name": "Apple Inc."
}
```

#### Stock Price with Currency Conversion
**Endpoint:** `GET /?queryStockWithFX={symbol}`  
**Description:** Gets the stock price in USD and converts it to CZK using the current exchange rate.  
**Example:** `GET /?queryStockWithFX=AAPL`  
**Example Response:**  
```json
{
  "symbol": "AAPL",
  "price_usd": 150.25,
  "price_czk": 3756.25,
  "fx_rate": 25.0
}
```

#### Portfolio Value
**Endpoint:** `GET /?queryPortfolioValue={symbols}`  
**Description:** Calculates the total value of a portfolio given a comma-separated list of stock symbols.  
**Example:** `GET /?queryPortfolioValue=AAPL,GOOGL,MSFT`  
**Example Response:** 
```json
{
  "portfolio_value_usd": 450.75,
  "stocks": [
    {"symbol": "AAPL", "price": 150.25},
    {"symbol": "GOOGL", "price": 200.0},
    {"symbol": "MSFT", "price": 100.5}
  ]
}
```

#### Evaluation of Opportunity
**Endpoint:** `GET /?queryEvaluateOpportunity={symbol}`  
**Description:** Evaluates if the stock is a good investment opportunity based on its recent price change and provides a summary.  
**Example:** `GET /?queryEvaluateOpportunity=AAPL`  
**Example Response:**   
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "price_usd": 150.25,
  "price_czk": 3756.25,
  "change_percent": 2.5,
  "fx_rate_usd_czk": 25.0,
  "trend": "rising",
  "summary": "The stock is currently rising. It may indicate positive market sentiment, but buying after a strong move can be riskier."
}
```

#### About
**Endpoint:** `GET /about`  
**Description:** Provides information about the service, author, and available endpoints.  
**Response:**  
```json
{
  "service": "Investment Helper API",
  "author": "Tomas Dolak",
  "endpoints": [
    "queryStockSummary",
    "queryPortfolioValue",
    "queryStockWithFX",
    "queryEvaluateOpportunity"
  ]
}
```

### Running Locally
1. Install `requirements.txt`
```bash
pip install -r requirements.txt
vercel dev
```
2. Then open:
```
http://localhost:3000
```

### Deployment
The application is deployed using Vercel:
1. Push repository to git repository
2. Import project in Vercel
3. Deploy

### Notes
The service is designed as a stateless application, which means that each request contains all the necessary information and no session data is stored on the server. All responses are returned in JSON format to ensure easy interoperability and integration with other systems. The application relies on external public APIs, which are used without authentication, making the solution simple and easy to deploy.

### Resources
[1] "Vercel: Build and deploy on the AI Cloud" [online]. [cited 2026-04-25]. Available at [https://vercel.com/](https://vercel.com/)
[2] "Vercel: Using the REST API" [online]. [cited 2026-04-25]. Available at [https://vercel.com/docs/rest-api](https://vercel.com/docs/rest-api)
[3] "Apify: Yahoo Finance API" [online]. [cited 2026-04-25]. Available at [https://apify.com/api/yahoo-finance-api](https://apify.com/api/yahoo-finance-api)
[4] "Github: yfinance" [online]. [cited 2026-04-25]. Available at [https://github.com/ranaroussi/yfinance](https://github.com/ranaroussi/yfinance)
[5] "exchangerate.host: Real-time current and historical foreign exchange & crypto rates data solution." [online]. [cited 2026-04-25]. Available at [https://exchangerate.host/](https://exchangerate.host/)