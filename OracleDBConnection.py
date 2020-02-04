#Importing libraries
import os
#import platform
import cx_Oracle

class OracleDBConnection:
    
    def __init__(self, ip, port, SID, user_name, password):
        self.ip = ip
        self.port = port
        self.SID = SID
        self.user_name = user_name
        self.password = password
    
    #Creating a database connection
    def createConnection(self):
        LOCATION = r"C:\Oracle\instantclient_19_3"
        #print("ARCH:", platform.architecture())
        #print("FILES AT LOCATION:")
        for name in os.listdir(LOCATION):
            print(name)
        os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
        
        dsn_tns = cx_Oracle.makedsn(self.ip, self.port, self.SID)
        conn = cx_Oracle.connect(self.user_name, self.password, dsn_tns)
        
        return conn

