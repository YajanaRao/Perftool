import sys,os

from perftool import interactive,main

from os import path
import sys
import random

import sys
sys.path.insert(0, path.dirname(path.abspath(path.dirname(__file__))))

class color:
    HEADER = '\033[95m'
    IMPORTANT = '\33[35m'
    NOTICE = '\033[33m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    UNDERLINE = '\033[4m'
    LOGGING = '\33[34m'


class welcome:
    color_random=[color.HEADER,color.IMPORTANT,color.NOTICE,color.OKBLUE,color.OKGREEN,color.WARNING,color.RED,color.END,color.UNDERLINE,color.LOGGING]
    random.shuffle(color_random)
    note = color_random[0] +'''
      ____    _____   ____    _____   _____    ___     ___    _
     |  _ \  | ____| |  _ \  |  ___| |_   _|  / _ \   / _ \  | |
     | |_) | |  _|   | |_) | | |_      | |   | | | | | | | | | |
     |  __/  | |___  |  _ <  |  _|     | |   | |_| | | |_| | | |___
     |_|     |_____| |_| \_\ |_|       |_|    \___/   \___/  |_____|
                                                                    '''+color.END

    inputPrompt = ">>"




#sys.path.append( path.dirname(path.abspath(path.dirname(__file__))) )

# sys.path.insert(0, path.dirname(path.abspath(path.dirname(__file__))))

import sys
print(sys.path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(welcome.note)
        print("\t \t \033[0m :- Yajana.N.Rao")
        print("Enter 'break' to exit the console")
        while True:
            if sys.version_info[0] > 2:
                #print(sys.version_info)
                #from future.builtins import input
                command = input(welcome.inputPrompt)
                
            else:
                command = raw_input(welcome.inputPrompt)

            if "break" in command:
                print("Exiting the application")
                break

            elif command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            else:
                interactive(command)
    else:
        main()
