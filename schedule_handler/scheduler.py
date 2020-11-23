# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger
import time as t
import schedule
from extract import extract
from schedule_handler.safe_schedule import SafeScheduler
from datetime import date



class Scheduler:
    """Create job to run ETL process
    """
    def __init__(self):
        """Initalize Class level variable
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')
        self.s3_directory = self.config.getConfigValue('S3_FILE_PATH_TRANSFORM')


    def job(self):
        self.log.info('Job Initialed')
        # if date.today().day == self.day:
        ext = extract.Extract()
        ext.extract_zip()
            

    #https://stackoverflow.com/a/57221649
    def schedule(self, day, time):

        self.day = day
        self.time = time
        
        scheduler = SafeScheduler()
        scheduler.every().day.at(time).do(self.job)
        # schedule.every(1).minutes.do(self.job)
        self.log.info('SCHEDULER SET to {} on every {} month'.format(self.time, self.day))
        while True: 
            # Checks whether a scheduled task  
            # is pending to run or not 
            self.log.info('Timer Loop'.format(self.time, self.day))
            schedule.run_pending() 
            t.sleep(10) 

if __name__== '__main__':
    trans = Scheduler()
    trans.schedule(23, '20:05')