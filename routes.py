# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger

from flask import Flask, request, render_template, url_for
from datetime import date
import json
import sys
from extract import extract

class Application:

    app = Flask(__name__)

    def __init__(self):
        """
        Initialize Configuration file 
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()


    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html', variables = date.today())
        
    @app.route('/transform/notification', methods=['POST'])
    def route_to_tranform():
        value = request.json['Records']
        print(value, file=sys.stderr)
        print('This is standard output', file=sys.stdout)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


    @app.route('/job/', methods=['GET'])
    def route_trigger_jobs():
        value = request.args.get('jobtype')
        print("value is", value, file=sys.stdout)        
        ext = extract.Extract()
        ext.extract()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


#x.Records[0].s3.object.key

if __name__ == "__main__":
    app = Application()
    app.app.run(debug=True, host = '0.0.0.0', port=8088)