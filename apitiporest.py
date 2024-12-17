from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

data = pd.DataFrame({
    "year": [2020, 2021, 2022],
    "coverage_percentage": [92.5, 94.0, 93.0],
    "source": ["World Bank", "World Bank", "World Bank"]
})

data_dict = data.to_dict(orient='records')

@app.route('/api/v1/vaccination', methods=['GET'])
def get_all_data():
    return jsonify({"country": "Panama", "data": data_dict})

@app.route('/api/v1/vaccination/<int:year>', methods=['GET'])
def get_data_by_year(year):
    filtered_data = [record for record in data_dict if record['year'] == year]
    if filtered_data:
        return jsonify({"year": year, "data": filtered_data})
    return jsonify({"error": "No data found for the specified year"}), 404

@app.route('/api/v1/vaccination/statistics', methods=['GET'])
def get_statistics():
    coverage = [record['coverage_percentage'] for record in data_dict]
    return jsonify({
        "max_coverage": max(coverage),
        "min_coverage": min(coverage),
        "average_coverage": sum(coverage) / len(coverage)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)