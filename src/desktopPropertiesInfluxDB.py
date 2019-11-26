from influxdb import InfluxDBClient
from datetime import datetime
import time
import argparse

import psutil
import platform
import cpuinfo
import shutil

USER = 'Melchior'
PASSWORD = 'azertyuiop'
DBNAME = 'WaveSinTSDB'

#os Name
os= platform.system()
timePause=5

def main(host='localhost', port=8086):
        
    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
    print("Create database: " + DBNAME)
    client.create_database(DBNAME)
    client.switch_database(DBNAME)
    
    i=0
    while(True):
        properties=[]
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        print("data : "+str(i))
        ## Battery 
        battery = psutil.sensors_battery()
        battery = str(battery.percent)
        #process running
        processPID = psutil.pids()
        Nprocess = len(processPID)
        #CPU
        cpu=cpuinfo.get_cpu_info()['brand']
        #disk
        total, used, free = shutil.disk_usage("/")
        total= total // (2**30)
        used= used // (2**30)
        free = free //(2**30)
        prop = {
            "measurement": 'laptop',
            "tags":{
                    "OS":os,
                    "CPU":cpu,
                    },
            
            "time": current_time,
            "fields": {
                "batery": battery,
                "process running":Nprocess,
                "Total Disk":total,
                "Free DISK":free,
                "Used DISK":used  
            }
        }
        properties.append(prop)
        i+=1
            # Write points
        print("Writting")
        client.write_points(properties)

    ##


    #query = 'SELECT * FROM laptop'
    #print("Querying data: " + query)
    #result = client.query(query, database=DBNAME)
    #print("Result: {0}".format(result))

    #print("Delete database: " + DBNAME)
    #client.drop_database(DBNAME)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
        
    