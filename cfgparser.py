import configparser, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class CfgParser():
  
    def __init__(self,env='default',cfg_path=None):
        self.env = env
        if cfg_path is None:
            self.cfg_path = os.path.join(BASE_DIR,'MongoDB','config.cfg')
        else:
            self.cfg_path = cfg_path
        
    def get(self,item):
        parser = configparser.ConfigParser()
        parser.read(self.cfg_path)
        return parser[self.env][item]
