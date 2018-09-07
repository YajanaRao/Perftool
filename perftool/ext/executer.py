from __future__ import print_function
import subprocess
import logging
import os
import multiprocessing
from datetime import datetime
from colorlog import ColoredFormatter, getLogger
import shutil
import time
import configparser
from functools import reduce
# Custom Modules
from .listener import PerformanceMonitor, writePerfData,writeSystemInfo

def get_output_dir():
    current_time = datetime.now()
    dir_name = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(dir_name)
    return dir_name

class Logs():
    def __init__(self, output_dir,log_level):
        self.output_dir = output_dir

        if log_level == "DEBUG":
            self.log_level = logging.DEBUG

        elif log_level == "WARN":
            self.log_level = logging.WARN

        else:
            self.log_level = logging.INFO


    def logger(self,name):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')

        logger = getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        if self.output_dir:
            # create a file handler
            log_dir = os.path.join(self.output_dir, 'program.log')
            fh = logging.FileHandler(log_dir)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)

            logger.addHandler(fh)

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


class ExecutionInfo():
    def __init__(self):
        self.start_time = datetime.now()

    def get_logger(self):
        if self.report == "False":
            self.output_dir = None

        else:
            self.output_dir = get_output_dir()

        self.log = Logs(self.output_dir,self.log_level)

    def get_defaults(self):
        config = configparser.RawConfigParser()
        config.read(os.path.join(self.dir_path,'config/defaults.ini'))
        self.log_level = config.get('log', 'level')
        self.report = config.get('reporting','reports')
        self.live = config.get('reporting','live')
        self.duration = config.get('duration','duration')
        self.database = config.get('database','influx')


    def summary(self):
        if self.status:
            print("\t \033[1;31;40m FAILED \033[0m")

        else:
            print("\t \033[1;32;40m SUCCESS \033[0m")


        print("Execution Started at {}".format(self.start_time))
        print("Execution Completed at {}".format(self.end_time))

        time_taken = self.end_time - self.start_time
        print("Total Time Taken {}".format(time_taken))

        if self.output_dir:
            #print(self.output_dir)
            shutil.copy(os.path.join(self.dir_path,"Reporter/templates/index.html"),self.output_dir)
            shutil.copytree(os.path.join(self.dir_path,"Reporter/templates/css"), os.path.join(self.output_dir,"css"))
            shutil.copytree(os.path.join(self.dir_path,"Reporter/templates/js"), os.path.join(self.output_dir,"js"))
            print("Reports are at {}".format(self.output_dir))


class ExecutionHandler():
    def __init__(self,exe_info):
        self.execution = exe_info
        self.output_dir = exe_info.output_dir
        # self.command = exe_info.command
        # self.duration = exe_info.duration
        self.live = exe_info.live
        self.log = exe_info.log.logger(self.__class__.__name__)
        exe_info.status = self.manage()


    def manage(self):
        self.log.debug(self.execution.command)
        self.log.info("Started Terminal Execution")
        self.log.debug("Main Process Id {}".format(os.getpid()))
        self.log.info("Duration {}".format(self.execution.duration))
        self.log.debug("Live report is {}".format(self.live))
        try:
            pool = multiprocessing.Pool(processes=1)
            result = pool.apply_async(execute, (self.execution.command,self.live,self.execution.database))
            pool.close()
            pool.join()
            output = result.get(timeout=self.execution.duration)
        except Exception as exp:
            self.log.debug(exp)
            self.log.error("Execution did not completed in given period")
            return 1
        self.log.info("Terminal Execution Completed")
        self.execution_log(output)
        return 0

    def execution_log(self, output):
        if self.output_dir:
            writeSystemInfo(self.output_dir)
            writePerfData(self.output_dir,output['perf'])
            log_dir = os.path.join(self.output_dir, "execution.log")
            with open(log_dir, "a") as f:
                f.write(output['output'])
        else:
            print(output['output'])
            perf = output['perf']
            for title, item in perf.items():
                print("________________________________")
                print(title)
                cpu = []
                memory = []
                disk = []
                network_sent = []
                network_recv = []
                for val in item:
                    #print(val)
                    for key,value in val.items():
                        #print(key)
                        if "cpu" in key:
                            cpu.append(value)

                        if "memory" in key:
                            memory.append(value)

                        if "disk" in key:
                            disk.append(value)

                        if "sent" in key:
                            network_sent.append(value)

                        if "recv" in key:
                            network_recv.append(value)

                #print(cpu,disk,memory)
                if cpu:
                    print("\tCPU    : {}".format(reduce(lambda x, y: x + y, cpu) / len(cpu)))

                if memory:
                    print("\tMEMORY : {}".format(reduce(lambda x, y: x + y, memory) / len(memory)))

                if disk:
                    print("\tDISK   : {}".format(reduce(lambda x, y: x + y, disk) / len(disk)))

                if network_sent:
                    print("\tBYTES SENT   : {}".format(reduce(lambda x, y: x + y, network_sent) / len(network_sent)))

                if network_recv:
                    print("\tBYTES RECV   : {}".format(reduce(lambda x, y: x + y, network_recv) / len(network_recv)))

                print("________________________________")


def execute(command,live,database):
    dictn = {}
    perf = PerformanceMonitor(live,database)
    perf.start(os.getpid())
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.PIPE, universal_newlines=True)
    output = p.stdout.read()
    perf.stop()
    dictn['output'] = output
    dictn['perf'] = perf.getData()
    return dictn
