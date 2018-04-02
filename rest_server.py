from flask import Flask, request, redirect, url_for
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
        start_date = start_date.strftime('%d/%m/%Y')
        end_date = end_date.strftime('%d/%m/%Y')
        start_real_value = -1
        end_value = -1
        with open('data/inflation_data.csv', 'r') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            headers = next(read)[1:]
            for row in read:
                if row[0] == start_date:
                    start_real_value = start_value / float(row[1])
                elif row[0] == end_date:
                    end_value = float(row[1])
        return int(start_real_value * end_value)

api.add_resource(MoneyValue, '/money_value')

if __name__ == '__main__':
    app.run(debug=True)
