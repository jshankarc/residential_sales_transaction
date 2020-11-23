# custom modules to handle configuration and logs
import schedule
from scheduler import Scheduler
from exception import InvalidRequest
from extract.extract import Extract
import configuration as configs
import logconfig as logger

from flask import Flask, request, render_template, url_for, jsonify
from datetime import date
import json
import sys
from extract import extract
from transform import transform
from load import load as ld
from schedule_handler import scheduler

class Application:

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Load Index HTML pages 

        Returns:
            HTML File: Index HTML
        """
        return render_template('index.html')


    @app.route('/extract', methods=['POST'])
    def extract():
        """Download file from the server 

        Returns:
            HTML File: Index HTML
        """
        #TODO: Form Validation, 
        #TODO: Task status infomation
        county = request.form.get('county')
        monthYear = request.form.get('monthYear')

        ext = Extract()
        status = 'FAILED'
        if ext.extract(county, monthYear):
            print("Extraction SUCESSFUL", sys.stderr)
            status = 'SUCCESS'
        return render_template('index.html', status = status)

    @app.route('/scheduler', methods = ['POST'])
    def scheduler():
        status = 'FAILED'

        schedule_info = request.form.get('scheduler_time')
        print('Schedule INfo {}'.format(schedule_info))

        time = schedule_info.split('T')[1]
        day = schedule_info.split('T')[0].split('-')[1]
        print('schedule time:{} and day:{}'.format(time, day))

        sch = scheduler.Scheduler()
        sch.schedule(day, time)
        
        return render_template('index.html')

    @app.route('/transform/notification', methods=['POST'])
    def route_to_tranform():
        """Invoke Tranform process
        """
        
        status = 'FAILED'
        json_data = ""

        if request.form.get('transformJsonReq') == None:
            json_data = request.json['Records']
        else:
            json_data = json.loads(request.form.get('transformJsonReq'))['Records']
        
        file_path_list = []
        for item in json_data:
            file_path_list.append(item['s3']['object']['key'])
            print(item['s3']['object']['key'])
        
        tran = transform.Transform()
        tran.transform(file_path_list)
        return render_template('index.html', status = status)

    @app.route('/load/notification', methods=['POST'])
    def route_to_load():
        """Invoke process
        """
        status = 'FAILED'
        json_data = ""

        if request.form.get('loadJsonReq') == None:
            json_data = request.json['Records']
        else:
            json_data = json.loads(request.form.get('loadJsonReq'))['Records']
        
        file_path_list = []
        for item in json_data:
            file_path_list.append(item['s3']['object']['key'])
            print(item['s3']['object']['key'])
        
        loadobj = ld.Load(file_path_list)
        loadobj.load()
        return render_template('index.html', status = status)
    
    @app.errorhandler(InvalidRequest)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


if __name__ == "__main__":
    app = Application()
    app.app.run(debug=True, host = 'localhost', port=8088)