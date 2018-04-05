from flask import Flask, request, redirect, url_for, jsonify, abort
from flask_restful import Resource, Api
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
import csv

app = Flask(__name__)
api = Api(app)

class MoneyValue(Resource):
    args = {
        'start_date': fields.Date(required=True),
        'start_value': fields.Int(required=True),
        'end_date': fields.Date(required=True),
    }
    @use_kwargs(args)
    def get(self, start_date, start_value, end_date):
        start_date_str = start_date.strftime('%d/%m/%Y')
        end_date_str = end_date.strftime('%d/%m/%Y')
        start_real_value = -1
        end_value = -1
        with open('data/inflation_data.csv', 'r') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            headers = next(read)[1:]
            for row in read:
                if row[0] == start_date_str:
                    start_real_value = start_value / float(row[1])
                elif row[0] == end_date_str:
                    end_value = float(row[1])

        if start_real_value < 0:
            abort(422, "No data available for that start_date")
        if end_value < 0:
            abort(422, "No data available for that end_date")
        if start_date > end_date:
            abort(422, "start_date is after end_date")

        return jsonify(int(start_real_value * end_value))

api.add_resource(MoneyValue, '/money_value')

if __name__ == '__main__':
    app.run(debug=True)
