import sys,os

from perftool import interactive,main

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\t \033[2;32;40m PERF\033[1;31;40mTOOL")
        print("\t \t \033[0m :- Yajana.N.Rao")
        print("Enter 'break' to exit the console")
        print("Performance Testing Tool")
        while True:
            if sys.version_info[0] > 2:
                #print(sys.version_info)
                #from future.builtins import input
                command = input(">>")

            else:
                command = raw_input(">>")

            if "break" in command:
                print("Exiting the application")
                break

            elif command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            else:
                interactive(command)
    else:
        main()
    

    
