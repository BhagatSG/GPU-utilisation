import pyodbc
import pandas as pd
import json
import configparser
import sys
import os
from datetime import date,datetime 
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
logfile = datetime.now().strftime('gpuutilisation.log')
handler = logging.FileHandler(logfile)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

if (logger.hasHandlers()):
    logger.handlers.clear()
# add the file handler to the logger
logger.addHandler(handler)

def parseGetConnection(config_path):   
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_path)
    config.sections()
    dbserver = config.get('db','DB_SERVER')
    dbase = config.get('db','DB_DATABASE')
    username = config.get('db','DB_USER')
    password = config.get('db','DB_PWD')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbserver+';DATABASE='+dbase+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor,cnxn;

def main():
    logger.info('********************************************************************************')
    if len(sys.argv)<1:
        logger.error('Exception occured in main() method Arguments')
        logger.info('********************************************************************************')
        sys.exit(1) 
    config_path='/root/config.ini'
    logger.info('config_path location: '+config_path)
    fileLocation= sys.argv[1]
    logger.info('fileLocation Arguement: '+fileLocation)
    if os.path.exists(config_path):
        try:
            cursor,cnxn=parseGetConnection(config_path)
            logger.info('Db Object Created')

            with open(fileLocation) as f:
                data = json.load(f)
            logger.info('Json Data Loaded: '+str(data))
            
            gpuutilisationDF=pd.DataFrame(columns=['uuid'])
            for gpu in data['gpus']:
                gpuutilisationDF=gpuutilisationDF.append({'uuid':gpu['uuid'],'gpuname':gpu['name'],'gpuUtilisation':gpu['utilization.gpu'],'powerDrawn':gpu['power.draw'],'memoryUsed':gpu['memory.used'],'memoryTotal':gpu['memory.total'],'gpuTemperature':gpu['temperature.gpu'],'processes':str(gpu['processes'])},ignore_index=True)
            
            fileName=fileLocation.split("/")[-1].split('##')
            logger.info('fileName value: '+str(fileName))
            gpuutilisationDF['hostName']=fileName[0]
            gpuutilisationDF['vmId']=fileName[1]
            gpuutilisationDF['vmSize']=fileName[2]
            gpuutilisationDF['resourceGroupName']=fileName[3]
            gpuutilisationDF['subscriptionId']=fileName[4].split('.')[0]    
            
            logger.info('Dataframe Created & Insertion into DB Started')
            for ind in gpuutilisationDF.index:
                cursor.execute("INSERT INTO gpuutilisation(host_name,subscription_id,resource_group_name,vm_id,vm_size,uuid,gpu_name,gpu_utilisation,power_drawn,used_memory,total_memory,gpu_temperature,processes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) ", 
                                (gpuutilisationDF['hostName'][ind],gpuutilisationDF['subscriptionId'][ind],gpuutilisationDF['resourceGroupName'][ind],gpuutilisationDF['vmId'][ind],
                                gpuutilisationDF['vmSize'][ind],gpuutilisationDF['uuid'][ind],gpuutilisationDF['gpuname'][ind],int(gpuutilisationDF['gpuUtilisation'][ind]),int(gpuutilisationDF['powerDrawn'][ind]),
                                int(gpuutilisationDF['memoryUsed'][ind]),int(gpuutilisationDF['memoryTotal'][ind]),int(gpuutilisationDF['gpuTemperature'][ind]),gpuutilisationDF['processes'][ind]))
            cnxn.commit()
            
            logger.info('Insertion into DB Completed')
            logger.info('********************************************************************************')
        except Exception as ex:
            logger.error('Exception occured in main() method:: '+str(ex))
            logger.info('********************************************************************************')
    else:
        logger.error("Configuration File Doesn't Exist")
        logger.info('********************************************************************************')

if __name__ == '__main__':
    main()
