from flask import Flask, request, redirect, url_for, jsonify, abort
from flask_restful import Resource, Api
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
import csv
import datetime

app = Flask(__name__)
api = Api(app)

def convert_date(date_in):
    tmp = date_in.split('/')
    return tmp[2] + '-' + tmp[1] + '-' + tmp[0]

class MoneyValue(Resource):
    args = {
        'start_date': fields.Date(required=True),
        'start_value': fields.Int(required=True),
        'end_date': fields.Date(required=True),
    }
    @use_kwargs(args)
    def get(self, start_date, start_value, end_date):
        if start_date > end_date:
            abort(422, "start_date is after end_date")
        start_date_str = start_date.strftime('%d/%m/%Y')
        end_date_str = end_date.strftime('%d/%m/%Y')
        start_real_value = -1
        end_value = -1
        with open('data/inflation_data.csv', 'r') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            headers = next(read)[1:]
            final_csv_row = None
            for row in read:
                if row[0] == start_date_str:
                    start_real_value = start_value / float(row[1])
                elif row[0] == end_date_str:
                    end_value = float(row[1])
                final_csv_row = row

            # Try one last time using yesterday's value
            if end_value < 0:
                end_date = end_date - datetime.timedelta(days=1)
                end_date_str = end_date.strftime('%d/%m/%Y')
                if final_csv_row[0] == end_date_str:
                    end_value = float(final_csv_row[1])

        if start_real_value < 0:
            abort(422, "No data available for that start_date")
        if end_value < 0:
            abort(422, "No data available for that end_date")

        return jsonify({'devalued': int(start_real_value * end_value), 'real': start_real_value})

class MoneyValueDateLimits(Resource):
    def get(self):
        first_date = ''
        last_date = ''
        with open('data/inflation_data.csv', 'r') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            headers = next(read)[1:]
            row = next(read)
            real_money_value = 1420
            first_date = convert_date(row[0])
            for row in read:
                last_date = convert_date(row[0])
        return jsonify({'first_date':first_date, 'last_date':last_date})

api.add_resource(MoneyValue, '/money_value')
api.add_resource(MoneyValueDateLimits, '/money_value_date_limits')

if __name__ == '__main__':
    app.run(debug=True)
