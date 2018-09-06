from __future__ import print_function
import psutil
import time
import platform
import os
import sys
import csv
import threading
import logging
from colorlog import ColoredFormatter, getLogger

sys.path.append('./reporter')

from reporter.influxdbhandler import influx_writer
from reporter.flaskapi import start_server,PerfData,stop_server



def getSystemInformation():
    systemdict = {}

    systemdict['Mechine'] = platform.machine()
    systemdict['Version'] = platform.version()
    systemdict['Platform'] = platform.platform()
    #systemdict['Name'] = platform.uname()
    systemdict['System'] = platform.system()
    systemdict['Processor'] = platform.processor()
    systemdict['User'] = psutil.users()[0].name
    systemdict['Total Memory'] = psutil.virtual_memory().total
    systemdict['Total Disk'] = psutil.disk_usage('/').total
    systemdict['Python Version'] = platform.python_version()
    return systemdict


def getPerfData():
    dictn={}

    available_memory = psutil.virtual_memory().percent
    used_disk = psutil.disk_usage('/').percent
    dictn['memory'] = available_memory
    dictn['disk'] = used_disk
    dictn['cpu'] = psutil.cpu_percent(interval=1)
    dictn['time'] = time.strftime("%H.%M.%S")
    return dictn

def getProccessPerf(pid):
    dictn = {}
    for proc in psutil.process_iter():
        if pid == proc.pid:
            dictn['cpu'] = proc.cpu_percent()
            dictn['memory'] = proc.memory_percent()
            dictn['time'] = time.strftime("%H.%M.%S")
            return dictn
def get_interface():
    counter = psutil.net_io_counters(pernic=True)
    if "Ethernet" in counter:
        return "Ethernet"
    else:
        return 'Wireless Network Connection'



convertion = lambda total,time: (total / time) / 1000000

def get_network_io(interface):
    data = {}
    counter=psutil.net_io_counters(pernic=True)[interface]
    data['sent'] = counter.bytes_sent
    data['recv'] = counter.bytes_recv
    return data

def average (list,key):
    total = 0
    for item in list:
        total = item[key]
    return total/len(list)

def network_collector():
    dictn = {}
    interface = get_interface()
    t0 = time.time()
    t1 = time.time()
    data = []
    while int(t1-t0) < 1:
        counter = get_network_io(interface)
        data.append(counter)
        t1 = time.time()
    t = t1-t0
    # print(t)

    avg_sent = average(data,'sent')
    avg_recv = average(data,'recv')
    dictn['recv'] = convertion(avg_sent,t)
    dictn['sent'] = convertion(avg_recv,t)
    dictn['time'] = time.strftime("%H.%M.%S")
    return dictn

def logger(name):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')

        logger = getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)



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
    global net_matric
    def __init__(self,live,database):
        self.flag = True
        self.live = live
        self.database = database
        self.log = logger(self.__class__.__name__)

    def start(self,pid):
        global thread
        self.log.info("Starting the Monitor")
        thread = threading.Thread(target=self.getPerf,args=(pid,))
        thread.start()

    def stop(self):
        time.sleep(10)
        self.flag = False
        self.log.info("Waiting for the thread to terminate")
        while thread.isAlive():
            time.sleep(0.1)
        self.log.info("Monitor Stopped")


    def getPerf(self,pid):
        global sys_matric
        global proc_matric
        global net_matric
        sys_matric = []
        proc_matric = []
        net_matric = []
        self.log.debug("Successfully Started")
        if str(self.live) == "True":
            perfdata = PerfData()
            server = threading.Thread(target=start_server,args=(perfdata,))
            server.start()
            self.log.debug("live reporting is enabled")
            # httpserver = HttpServer()
            # httpserver.startServer()
            self.log.debug("Server is running")
            self.log.debug(self.flag)
            while self.flag:
                perf = getPerfData()
                proc = getProccessPerf(pid)
                nets = network_collector()
                perfdata.set_system_data(perf)
                perfdata.set_process_data(proc)
                perfdata.set_network_data(nets)
            #     proc = getProccessPerf(pid)
            #     updateProcessData(proc)
            #     updateSystemData(perf)
                sys_matric.append(perf)
                proc_matric.append(proc)
                net_matric.append(nets)
            #
            # httpserver.stopServer()

            stop_server()

        elif str(self.database) == "True":
            self.log.debug("data will be pushed to database")
            inflx = influx_writer()
            inflx.create_datasource()
            self.log.debug("Datasource created")
            self.log.debug(self.flag)
            while self.flag:
                perf = getPerfData()
                proc = getProccessPerf(pid)
                nets = network_collector()
                inflx.write_process_data(proc)
                inflx.write_system_data(perf)
                sys_matric.append(perf)
                proc_matric.append(proc)
                net_matric.append(nets)
                self.log.debug("no issues")


        else:
            self.log.debug("Live reporting is disabled")
            while self.flag:
                perf = getPerfData()
                proc = getProccessPerf(pid)
                nets = network_collector()
                sys_matric.append(perf)
                proc_matric.append(proc)
                net_matric.append(nets)


    def getData(self):
        global sys_matric
        global proc_matric
        global net_matric
        dictn = {}
        dictn['System'] =  sys_matric
        dictn['Process'] = proc_matric
        dictn['Network'] = net_matric
        return dictn

def writeSystemInfo(output_dir):
    data = getSystemInformation()
    report_dir = os.path.join(output_dir, 'systemdata.csv')
    with open(report_dir, 'w') as csv_file:  # just use 'w' mode in 3.x
        writer = csv.writer(csv_file,lineterminator='\n')
        writer.writerow(["System","Information"])
        for key, value in data.items():
            writer.writerow([key,value])


def writePerfData(output_dir,matrix):
    sys_matric = matrix['System']
    proc_matric = matrix['Process']
    net_matric = matrix['Network']
    if output_dir:
        report_dir = os.path.join(output_dir, 'performancedata.csv')
        with open(report_dir, 'w') as csv_file:  # just use 'w' mode in 3.x
            writer = csv.writer(csv_file,lineterminator='\n')
            writer.writerow(["time","disk","memory","cpu"])
            for perf in sys_matric:
                writer.writerow([perf['time'],perf['disk'],perf['memory'],perf['cpu']])


        report_dir = os.path.join(output_dir, 'processdata.csv')
        with open(report_dir,'w') as csvfile:
            writer = csv.writer(csvfile,lineterminator='\n')
            writer.writerow(["time","cpu","memory"])

            for perf in proc_matric:
                writer.writerow([perf['time'],perf['cpu'],perf['memory']])
    else:
        print(sys_matric,proc_matric)





# try:
#     from http.server import HTTPServer,BaseHTTPRequestHandler # Python 3
# except ImportError:
#     from SimpleHTTPServer import BaseHTTPServer
#     HTTPServer = BaseHTTPServer.HTTPServer
#     from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler # Python 2

# import webbrowser
# import json
# global proc_data
# global sys_data
# proc_data = {}
# sys_data = {}

# def http_logger(HTTPServer):
#     HTTPServer.log_message()
#     pass





# def updateProcessData(datas):
#     global proc_data
#     proc_data = datas
#
# def updateSystemData(datas):
#     global sys_data
#     sys_data = datas
#
#
# class Serve(BaseHTTPRequestHandler):
#
#     def log_message(self, format, *args):
#         pass
#
#     def do_GET(self):
#         if self.path == '/api/proc':
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             try:
#                 data = json.dumps(proc_data)
#                 self.send_response(200)
#
#             except:
#                 data = "Server down"
#                 self.send_response(400)
#             try:
#                 self.wfile.write(bytes(data).encode('utf-8'))
#
#             except:
#                 self.wfile.write(bytes(data,'utf-8'))
#
#         if self.path == '/api/sys':
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             try:
#                 data = json.dumps(sys_data)
#                 self.send_response(200)
#
#             except:
#                 data = "Server down"
#                 self.send_response(400)
#             try:
#                 self.wfile.write(bytes(data).encode('utf-8'))
#
#             except:
#                 self.wfile.write(bytes(data,'utf-8'))
#
#         if self.path == '/report':
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             try:
#                 report = open("C:/Users/Yajana/Documents/GitHub/Perftool/perftool/reporter/report.html")
#                 self.send_response(200)
#
#             except:
#                 report =  open("C:/Users/Yajana/Documents/GitHub/Perftool/perftool/reporter/index.html")
#                 self.send_response(400)
#
#             try:
#                 self.wfile.write(report.read().encode('utf-8'))
#
#             except:
#                 self.wfile.write(bytes(report.read(),'utf-8'))
#
#
#
# class HttpServer():
#     def __init__(self):
#         self.log = logger(self.__class__.__name__)
#         self.log.info("starting server")
#         self.httpd = HTTPServer(('0.0.0.0',8060),Serve)
#
#     def stopServer(self):
#         self.httpd.shutdown()
#
#     def startServer(self):
#          thread = threading.Thread(target=self.httpd.serve_forever,args=())
#          thread.start()
#          self.log.info("Server started")
#          new = 2
#          webbrowser.open('http://localhost:8060/report',new=2)
