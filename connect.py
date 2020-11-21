import pymongo
from cfgparser import CfgParser


class DataConnection():

    def __init__(self, env, config_path=None):
        self.env = env
        config = CfgParser(env,config_path)
        password = config.get('password')
        username = config.get('username')
        self.connect_uri = config.get('uri').replace('username:password', username+':'+password )

    def connect(self):
        conn = pymongo.MongoClient(self.connect_uri)
        return conn
    
    