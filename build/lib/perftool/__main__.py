import sys,os
from future.builtins import input
from manage import interactive,main

if __name__ == '__main__':
    if len(sys.argv) < 2:
        while True:
            command = input(">>")
            if command == "break":
                print("Exiting the application")
                break

            elif command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            else:
                interactive(command)
    else:
        main()
    

    
