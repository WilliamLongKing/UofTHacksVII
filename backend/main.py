from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from backend.common.connect import Database

app = Flask(__name__)

@app.route('/yearly_chart_data', methods=['GET'])
def yearlyData():
    year = request.args.get('year')
    data = Database.selectSongsInDateRange( year+"01-01", year+"12-31")

    retval = []

if __name__ == '__main__':
    app.run(debug=True, port=4999)
