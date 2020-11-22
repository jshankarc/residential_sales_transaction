# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger

from flask import Flask, request, render_template, url_for
from datetime import date
import json
import sys
from extract import extract
from transform import transform

class Application:

    app = Flask(__name__)

    def __init__(self):
        """Initialize Configuration file 
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()


    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Load Index HTML pages 

        Returns:
            HTML File: Index HTML
        """
        return render_template('index.html', variables = date.today())
        
    @app.route('/transform/notification', methods=['POST'])
    def route_to_tranform():
        """[summary]

        Returns:
            [type]: [description]
        """

        record = request.json['Records']
        file_path_list = []
        for item in record:
            file_path_list.append(item['s3']['object']['key'])
            print(item['s3']['object']['key'])
        
        # print('This is standard output : {}'.format(record), file=sys.stdout)
        tran = transform.Transform()
        tran.transform(file_path_list)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


    @app.route('/job/', methods=['GET'])
    def route_trigger_jobs():
        """[summary]

        Returns:
            [type]: [description]
        """

        value = request.args.get('jobtype')
        # print("value is", value, file=sys.stdout)        
        print()
        ext = extract.Extract()
        ext.extract()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


if __name__ == "__main__":
    app = Application()
    app.app.run(debug=True, host = '0.0.0.0', port=8088)