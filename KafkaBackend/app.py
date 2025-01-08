from flask import Flask, jsonify
from cassandra.cluster import Cluster
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect once at startup
cluster = Cluster(["localhost"], port=9042)
session = cluster.connect("stock_data")

@app.route('/stocks/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    query = f"""
    SELECT symbol, ts, open, high, low, price, volume
    FROM stock_prices
    WHERE symbol='{symbol}' 
    ORDER BY ts ASC
    """
    rows = session.execute(query)
    results = []
    for row in rows:
        results.append({
            "symbol": row.symbol,
            "ts": str(row.ts),
            "open": row.open,
            "high": row.high,
            "low": row.low,
            "price": row.price,
            "volume": row.volume
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)