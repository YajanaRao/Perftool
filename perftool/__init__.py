import sys,os

from perftool import interactive,main

if __name__ == '__main__':
    if len(sys.argv) < 2:
        while True:
            command = input(">>")
            if command == "break":
                break

            elif "clear" in command:
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                interactive(command)
    else:
        main()
    

    
