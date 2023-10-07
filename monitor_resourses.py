import psutil
from blessings import Terminal

def mostrar_monitor_recursos():
    term = Terminal()

    try:
        while True:
            with term.fullscreen():
                cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
                mem_info = psutil.virtual_memory()
                swap_info = psutil.swap_memory()

                max_bar_width = term.width - 30 

                cpu_lines = []
                for i, percent in enumerate(cpu_percent):
                    bar_length = int(percent / 100 * max_bar_width)
                    cpu_line = f"CPU {i + 1}: [{term.green('=' * bar_length)}{term.normal}{(' ' * (max_bar_width - bar_length))}] {percent}%"
                    cpu_lines.append(cpu_line)

                ram_bar_length = int((mem_info.used / mem_info.total) * max_bar_width)
                ram_line = f"RAM: [{term.yellow('=' * ram_bar_length)}{term.normal}{(' ' * (max_bar_width - ram_bar_length))}] {mem_info.used / (1024**3):.2f} GB / {mem_info.total / (1024**3):.2f} GB"

                swap_bar_length = int((swap_info.used / swap_info.total) * max_bar_width)
                swap_line = f"Swp: [{term.red('=' * swap_bar_length)}{term.normal}{(' ' * (max_bar_width - swap_bar_length))}] {swap_info.used / (1024**3):.2f} GB / {swap_info.total / (1024**3):.2f} GB"

                print(term.clear)

                print(term.bold("yotop by:yoezequiel"))
                print()
                for line in cpu_lines:
                    print(line)
                print()
                print(ram_line)
                print(swap_line)

    except KeyboardInterrupt:
        print(term.clear)

if __name__ == "__main__":
    mostrar_monitor_recursos()
