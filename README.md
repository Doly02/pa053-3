# PA053 Distributed Systems & Middleware: Homework 3
- Author: Tomáš Dolák
- Login: 582959
- Emails: <582959@mail.muni.cz>

## Table of Contents

- [Investment Helper REST API](#investment-helper-rest-api)
  - [Description](#description)
  - [Implemented Endpoints](#implemented-endpoints)
    - [Airport Temperature](#airport-temperature)
    - [Stock Price](#stock-price)
    - [Expression Evaluation](#expression-evaluation)
  - [Running Locally](#running-locally)
  - [Example of Usage](#example-of-usage)
  - [Deployment](#deployment)
  - [Notes](#notes)
  - [Resources](#resources)


## Investment Helper REST API
This project implements a simple REST service using Flask and deployed on Vercel.  
The goal is to provide practical experience with creating a web service that integrates multiple external APIs and performs computation.


You can try the implemented service at [https://pa053-3.vercel.app/](https://pa053-3.vercel.app/), service is deployed thru GitHub repository avalaible at [https://github.com/Doly02/pa053-3](https://github.com/Doly02/pa053-3)

The system acts as a middleware layer that aggregates and enriches data from multiple external services and applies custom business logic.

### Description

The application demonstrates principles of distributed systems and middleware:
- REST communication over HTTP
- Integration of multiple external services
- Data aggregation and transformation
- Stateless request processing

## Supported Query Parameters

The service recognizes exactly three query parameters.  
Only one parameter should be present in a request.

#### Airport Temperature
**Endpoint:** `GET /?queryAirportTemp={IATA_CODE}`  
**Description:** Returns the current temperature (in °C) for a given airport.  
**Example:** `GET /?queryAirportTemp=PRG`  
**Example Response:**  
```json
8
```

#### Stock Price
**Endpoint:** `GET /?queryStockPrice={symbol}`  
**Description:** Returns the current stock price..  
**Example:** `GET /?queryStockPrice=AAPL`  
**Example Response:**  
```json
247.77
```

#### Expression Evaluation
**Endpoint:** `GET /?queryEval={expression}`  
**Description:** Evaluates an arithmetic expression. Supported operations are addition, substraction, multiplication, division and parentheses.
**Example:** `GET /?queryEval=10%2B(5*2)`  
**Example Response:** 
```json
20
```

### Example of Usage
The following example demonstrate how to interact with the deployed REST API:
```
https://pa053-3.vercel.app/?queryEval=10%2B(5*2)
```
All endpoints can be tested directly via browser by using the following base URL:
https://pa053-3.vercel.app/

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

[3] "Wttr.in" [online]. Available at [https://wttr.in/](https://wttr.in/)

[4] "Airport Data" [online]. Available at [https://airport-data.com/](https://airport-data.com/)

[5] "Stooq Stock Data API" [online]. Available at [https://stooq.com/](https://stooq.com/)
