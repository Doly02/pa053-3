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
    - [Compound Interest](#compound-interest)
    - [Monthly Invesment](#compound-interest)
    - [Loan Cost](#loan-cost)
    - [About](#about)
  - [Running Locally](#running-locally)
  - [Deployment](#deployment)
  - [Notes](#notes)
  - [Resources](#resources)


## Investment Helper REST API
This project implements a simple REST web service deployed on Vercel using Flask.  
The service aggregates data from multiple public APIs and applies custom logic to provide meaningful responses.

You can try the implemented service at [https://pa053-3.vercel.app/](https://pa053-3.vercel.app/)

### Description

The application demonstrates principles of distributed systems and middleware:
- REST communication over HTTP
- Integration of multiple external services
- Data aggregation and transformation
- Stateless request processing

### Implemented Endpoints

This API integrates with external services to provide stock data and currency conversion functionality.  
It uses the **Stooq API** (CSV-based) to retrieve stock prices and calculate daily changes, and the **ExchangeRate API (open.er-api.com)** to obtain current USD to CZK exchange rates.

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
**Description:** Calculates the total value of a portfolio. Supports specifying quantity of each stock using the format `SYMBOL:QUANTITY`. If quantity is not provided, it defaults to 1.
**Example:** `GET /?queryPortfolioValue=AAPL:2,MSFT:3`  
**Example Response:** 
```json
{
  "portfolio_value_usd": 1800.5,
  "stocks": [
    {
      "symbol": "AAPL",
      "quantity": 2,
      "price": 190.12,
      "value": 380.24,
      "weight_percent": 21.1
    },
    {
      "symbol": "MSFT",
      "quantity": 3,
      "price": 473.42,
      "value": 1420.26,
      "weight_percent": 78.9
    }
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

#### Compound Interest
**Endpoint:** `GET /?queryCompoundInterest={principal,rate,years}`  
**Description:** Calculates compound interest for a given initial investment.  
**Example:** `GET /?queryCompoundInterest=10000,7,10`  
**Example Response:**  
```json
{
  "principal": 10000,
  "annual_rate_percent": 7,
  "years": 10,
  "final_amount": 19671.51,
  "profit": 9671.51
}
```

#### Monthly Investment
**Endpoint:** `GET /?queryMonthlyInvestment={amount,rate,years}`  
**Description:** Calculates the future value of regular monthly investments.
**Example:** `GET /?queryMonthlyInvestment=2000,8,15`  
**Example Response:**  
```json
{
  "monthly_payment": 2000,
  "annual_rate_percent": 8,
  "years": 15,
  "invested_amount": 360000,
  "final_amount": 694047.75,
  "profit": 334047.75
}
```

#### Loan Cost
**Endpoint:** `GET /?queryLoanCost={amount,rate,years}`  
**Description:** Calculates the total cost of a loan including interest.
**Example:** `GET /?queryLoanCost=100000,6,5`  
**Example Response:**  
```json
{
  "loan_amount": 100000,
  "annual_rate_percent": 6,
  "years": 5,
  "monthly_payment": 1933.28,
  "total_paid": 115996.8,
  "total_interest": 15996.8
}
```

#### About
**Endpoint:** `GET /about`  
**Description:** Provides information about the service, author, and available endpoints.  
**Response:**  
```json
"endpoints": {
  "queryStockSummary": { "example": "/?queryStockSummary=AAPL" },
  "queryPortfolioValue": { "example": "/?queryPortfolioValue=AAPL:2,MSFT:3" },
  "queryStockWithFX": { "example": "/?queryStockWithFX=AAPL" },
  "queryEvaluateOpportunity": { "example": "/?queryEvaluateOpportunity=AAPL" },
  "queryCompoundInterest": { "example": "/?queryCompoundInterest=10000,7,10" },
  "queryMonthlyInvestment": { "example": "/?queryMonthlyInvestment=2000,8,15" },
  "queryLoanCost": { "example": "/?queryLoanCost=100000,6,5" }
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

[3] "Stooq Stock Data API" [online]. Available at [https://stooq.com/](https://stooq.com/)

[4] "ExchangeRate API (open.er-api.com)" [online]. Available at [https://open.er-api.com/](https://open.er-api.com/)
