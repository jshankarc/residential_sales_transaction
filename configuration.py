from configparser import ConfigParser
import sys
class Configuration: 

    CONFIG_FILE_PATH = 'configs/config.ini'
  
    # default constructor 
    def __init__(self):
        # Read Configuration file  
        self.config_object = ConfigParser()
        try:
            with open(Configuration.CONFIG_FILE_PATH) as file:
                self.config_object.read_file(file)
                self.config = self.config_object["WEBSITE_INFO"]
        except FileNotFoundError:
            # self.log.error("Configuration File Does not exist in the root path {}".format(LoadConfiguration.CONFIG_FILE_PATH))
            print("Configuration File Does not exist in the root path {}".format(Configuration.CONFIG_FILE_PATH), file=sys.stderr)
  
    # a method for printing data members 
    def getConfigValue(self, key):
        """[summary]

        Args:
            key ([type]): [description]

        Returns:
            [type]: [description]
        """
        # print("getConfigValue: Key: {}, Value: {}".format(key,self.config[key]), file=sys.stdout)
        return self.config[key]

 
if __name__== '__main__':
    trans = Configuration()
    trans.getConfigValue('url')
