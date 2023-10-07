import psutil
import os
import time
from colorama import Fore, Style

def listar_procesos():
    while True:
        os.system('clear')  # Limpia la pantalla en sistemas Unix-like (Linux, macOS)
        print(f"{Fore.CYAN}PID   Nombre{Fore.RESET}      {Fore.YELLOW}CPU (%)   RAM (%)")
        print("------------------------------------")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu_percent = proc.info['cpu_percent']
                memory_percent = proc.info['memory_percent']
                pid_color = Fore.CYAN if pid != os.getpid() else Fore.RED  # Resaltar el PID actual en rojo
                print(f"{pid_color}{pid}   {name[:15]:<15}{Fore.RESET}   {Fore.YELLOW}{cpu_percent:.2f}%    {memory_percent:.2f}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(5)  # Actualiza la lista cada 2 segundos

if __name__ == "__main__":
    listar_procesos()
