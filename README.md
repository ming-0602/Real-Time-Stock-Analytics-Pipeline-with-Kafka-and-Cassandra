# Real-Time Stock Analytics Pipeline
This project demonstrates a near real-time data pipeline that fetches stock data from an external API (Alpha Vantage), ingests it via Apache Kafka, stores it in Cassandra, and displays the results in a React candlestick chart.

![Untitled](https://github.com/user-attachments/assets/e94f67ec-712d-449b-bf6d-bdfd836096b0)

### Table of Contents <br />
- Overview<br />
- Features<br />
- Architecture<br />
- Technology Stack<br />
- Setup & Installation<br />
- Running the Pipeline<br />
  1. Start Kafka & Cassandra<br />
  2. Producer<br />
  3. Consumer<br />
  4. React Front-End<br />
- Usage<br />
- Customization<br />
- Next Steps<br />
- License<br />

## Overview
- Goal: Fetch real-time (or near real-time) stock quotes, push them into Kafka, store them in Cassandra, and visualize candlestick charts in a React front-end.
- Scope: Demonstrates an end-to-end pipeline: API/Producer → Kafka → Consumer + Database → Front-end Visualization.
If your aim is to see how real-time data ingestion and charting can work together, this project provides a functional starting point.

## Features
1. **Producer**: Python script (**`alphaproducer.py`**) fetches stock data from the Alpha Vantage API.
2. **Kafka**: Manages streaming data flow.
3. **Consumer**: Another Python script (**`alphaconsumer.py`**) subscribes to Kafka, processes the incoming stock data, and inserts into Cassandra.
4. **Cassandra**: Stores historical stock quotes (symbol, timestamp, open, high, low, price, volume).
5. **React Front-End**: Displays candlestick charts (using **`chartjs-chart-financial`**), pulling data from a simple API that reads from Cassandra.

## Architecture

![image](https://github.com/user-attachments/assets/dbc75e63-7d4d-4379-b576-85b6b5e1657a)

1. Producer calls Alpha Vantage every X seconds, publishes JSON to Kafka.
2. Consumer reads from Kafka, inserts into Cassandra.
3. Front-End calls a small API or directly queries Cassandra to display candlestick data.

## Technology Stack
- **Python** (3.10+ recommended)
  - **`requests`** for Alpha Vantage
  - **`confluent-kafka`** for Kafka producer/consumer
  - **`cassandra-driver`** for Cassandra
- **Apache Kafka** (Docker or local installation)
- **Apache Cassandra** (Docker or local installation)
- **React** (Create React App)
  - **`react-chartjs-2`**
  - **`chart.js`** + **`chartjs-chart-financial`** for candlesticks
  - **`chartjs-adapter-date-fns`** for time scale
- Optional: Docker Compose or Kubernetes for orchestration.

## Setup & Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/YourUsername/your-repo-name.git
    cd your-repo-name
    ```
2. Install Kafka & Cassandra:
    - **Option A**: Docker containers for both.
    - **Option B**: Local installations.
3. Configure:
    - In **`alphaproducer.py`**, set your Alpha Vantage API key (**`ALPHA_VANTAGE_API_KEY`**) and Kafka bootstrap server if needed.
    - In **`alphaconsumer.py`**, point to your Kafka server and Cassandra host.


## Running the Pipeline
1. Start Kafka & Cassandra
    - Kafka (via Docker):
      ```bash
      docker-compose up -d zookeeper kafka
      ```
      (Adjust for your environment.)
    - Cassandra:
      ```bash
      Copy code
      docker run -d --name cass_container -p 9042:9042 cassandra:latest
      ```
      or local install.
2. Producer
    - Install Python dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Run the producer:
      ```bash
      python alphaproducer.py
      ```
      It fetches stock data from Alpha Vantage every 30 seconds, publishes to Kafka.
3. Consumer
    - In another terminal:
      ```bash
      python alphaconsumer.py
      ```
      It subscribes to the stock_quotes topic and inserts rows into the stock_data.stock_prices table in Cassandra.
4. React Front-End
    - In the frontend folder:
      ```bash
      npm install
      npm start
      ```
      (Or yarn equivalents.)

    - Open http://localhost:3000 in your browser.

    - You should see a candlestick chart for a default symbol (e.g., AAPL).

## Usage
1. Edit **`alphaproducer.py`** to change the fetch interval, add more symbols (e.g. **`["AAPL","AMZN","GOOG","TSLA"]`**).
2. Watch the consumer logs: each message inserted into Cassandra is printed out.
3. Visit **`localhost:3000`** to see the chart.
    - You can customize the chart in frontend/src/CandlestickChart.js.

## Customization
  - **Add More Endpoints**: If you’d like multiple routes (e.g., **`/stocks/AAPL/daily`**), you can build an Express/Flask API or directly query Cassandra from your front-end (not recommended for production).
  - **Change the Aggregation**: Instead of raw intraday data, you can store daily OHLC.
  - **Auto-Refresh**: Set an interval in the React code to fetch new data every X seconds, or implement WebSocket push.

## Next Steps
- **Analytics**: Compute rolling averages or RSI, overlay them on the candlestick chart.
- **Real-Time Refresh**: Use a small setInterval or WebSockets to auto-update the chart.
- **Deploy**: Dockerize each component (Producer, Consumer, Cassandra, React) and orchestrate with Docker Compose or Kubernetes for a more production-like setup.
- **Authentication & Security**: Protect Kafka with SASL/SSL if needed.
- **Logging & Monitoring**: Add logs, use Prometheus + Grafana to watch consumer lag, Cassandra performance, etc.

## License
This project is licensed under the MIT License. Feel free to use or modify it for your own purposes.

## Final Note
This project demonstrates a fully functioning real-time pipeline from **API** to **Kafka** to **Cassandra** to **React** chart. If you have any questions or ideas for improvements, please open an issue or submit a pull request. Happy coding!
