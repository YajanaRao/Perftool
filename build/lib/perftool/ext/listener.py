from __future__ import print_function
import psutil
import time
import platform
import os
import csv
import threading
import logging
from colorlog import ColoredFormatter, getLogger



def getSystemInformation():
    systemdict = {}

    systemdict['Mechine'] = platform.machine()
    systemdict['Version'] = platform.version()
    systemdict['Platform'] = platform.platform()
    systemdict['Name'] = platform.uname()
    systemdict['System'] = platform.system()
    systemdict['Processor'] = platform.processor()
    systemdict['User'] = psutil.users()[0].name
    systemdict['Total Memory'] = psutil.virtual_memory().total
    systemdict['Total Disk'] = psutil.disk_usage('/').total
    systemdict['Python Version'] = platform.python_version()
    return systemdict


def getPerfData():
    dict={}

    available_memory = psutil.virtual_memory().percent
    used_disk = psutil.disk_usage('/').percent
    dict['memory'] = available_memory
    dict['disk'] = used_disk
    dict['cpu'] = psutil.cpu_percent(interval=1)
    dict['time'] = time.strftime("%H.%M.%S")
    return dict

def getProccessPerf(pid):
    dict = {}
    for proc in psutil.process_iter():
        if pid == proc.pid:
            dict['cpu'] = proc.cpu_percent()
            dict['memory'] = proc.memory_percent()
            dict['time'] = time.strftime("%H.%M.%S")
            return dict

def logger(name):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')

        logger = getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARN)



        # add formatter to ch
        ch.setFormatter(formatter)

        col_formatter = ColoredFormatter(
            "%(cyan)s%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message)s",
            datefmt='%I:%M:%S %p',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        )
        ch.setFormatter(col_formatter)

        # add ch to logger
        logger.addHandler(ch)
        return logger

class PerformanceMonitor():
    global thread
    global sys_matric 
    global proc_matric
    def __init__(self):
        self.flag = True;
        self.log = logger(self.__class__.__name__)

    def start(self,pid):
        global thread
        self.log.info("Starting the Monitor")
        thread = threading.Thread(target=self.getPerf,args=(pid,))
        thread.start()
        
    def stop(self):
        self.flag = False
        self.log.info("Waiting for the thread to terminate")
        while thread.isAlive():
            time.sleep(0.1)
        self.log.info("Monitor Stopped")
               

    def getPerf(self,pid):
        global sys_matric
        global proc_matric
        sys_matric = []
        proc_matric = []
        self.log.debug("Successfully Started")
        while self.flag:
            perf = getPerfData()
            proc = getProccessPerf(pid)
            sys_matric.append(perf)
            proc_matric.append(proc)

    def getData(self):
        global sys_matric
        global proc_matric
        dict = {}
        dict['System'] =  sys_matric
        dict['Process'] = proc_matric
        return dict
       
            
def writePerfData(output_dir,matrix):
    sys_matric = matrix['System']
    proc_matric = matrix['Process']
    data = getSystemInformation()
    if output_dir:
        report_dir = os.path.join(output_dir, 'performancedata.csv')
        with open(report_dir, 'w') as csv_file:  # just use 'w' mode in 3.x
            writer = csv.writer(csv_file,lineterminator='\n')
            writer.writerow(["time","disk","memory","cpu"])
            for perf in sys_matric:
                writer.writerow([perf['time'],perf['disk'],perf['memory'],perf['cpu']])

        report_dir = os.path.join(output_dir, 'systemdata.csv')
        with open(report_dir, 'w') as csv_file:  # just use 'w' mode in 3.x
            writer = csv.writer(csv_file,lineterminator='\n')
            writer.writerow(["System","Information"])
            for key, value in data.items():
                writer.writerow([key,value])

        report_dir = os.path.join(output_dir, 'processdata.csv')
        with open(report_dir,'w') as csvfile:
            writer = csv.writer(csvfile,lineterminator='\n')
            writer.writerow(["time","cpu","memory"])

            for perf in proc_matric:
                writer.writerow([perf['time'],perf['cpu'],perf['memory']])
    else:
        print(data,sys_matric,proc_matric)


    



#perf = PerformanceMonitor()
#perf.start(os.getpid)
#time.sleep(5)
#perf.stop()
#perf.writePerfData(None)
