import psutil
import curses

COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_CYAN = 4
COLOR_WHITE = 5

def init_colors():
    curses.start_color()
    curses.init_pair(COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)

def mostrar_monitor_recursos(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    sh, sw = stdscr.getmaxyx()
    monitor_height = sh // 2
    max_bar_width = sw - 30
    selected_process = 0
    top_process = 0

    init_colors()
    try:
        while True:
            stdscr.clear()

            # Monitor de recursos en la parte superior
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            mem_info = psutil.virtual_memory()
            swap_info = psutil.swap_memory()

            stdscr.addstr(0, 0, "yotop by:yoezequiel", curses.color_pair(COLOR_CYAN) | curses.A_BOLD)
            for i, percent in enumerate(cpu_percent):
                bar_length = int(percent / 100 * max_bar_width)
                cpu_line = f"CPU {i + 1}: [{('=' * bar_length)}{(' ' * (max_bar_width - bar_length))}] {percent}%"                
                if percent > 80:
                    stdscr.addstr(i + 2, 0, cpu_line, curses.color_pair(COLOR_RED))
                else:
                    stdscr.addstr(i + 2, 0, cpu_line, curses.color_pair(COLOR_GREEN))
            ram_bar_length = int((mem_info.used / mem_info.total) * max_bar_width)
            ram_line = f"RAM: [{('=' * ram_bar_length)}{(' ' * (max_bar_width - ram_bar_length))}] {mem_info.used / (1024**3):.2f} GB / {mem_info.total / (1024**3):.2f} GB"
            stdscr.addstr(len(cpu_percent) + 3, 0, ram_line, curses.color_pair(COLOR_YELLOW))
            swap_bar_length = int((swap_info.used / swap_info.total) * max_bar_width)
            swap_line = f"Swp: [{('=' * swap_bar_length)}{(' ' * (max_bar_width - swap_bar_length))}] {swap_info.used / (1024**3):.2f} GB / {swap_info.total / (1024**3):.2f} GB"
            stdscr.addstr(len(cpu_percent) + 4, 0, swap_line, curses.color_pair(COLOR_YELLOW))

            # Lista de procesos en la parte inferior
            stdscr.addstr(monitor_height + 1, 0, "PID   Nombre      CPU (%)   RAM (%)", curses.color_pair(COLOR_CYAN) | curses.A_BOLD)
            stdscr.addstr(monitor_height + 2, 0, "------------------------------------", curses.color_pair(COLOR_CYAN) | curses.A_BOLD)
            processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            process_list = list(processes)
            num_processes = len(process_list)

            # Navegación por la lista de procesos
            max_display_lines = sh - monitor_height - 4
            for i in range(top_process, min(num_processes, top_process + max_display_lines)):
                proc = process_list[i]
                try:
                    pid = proc.info['pid']
                    name = proc.info['name'][:15]
                    cpu_percent = proc.info['cpu_percent']
                    memory_percent = proc.info['memory_percent']
                    proc_line = f"{pid}   {name:<15}   {cpu_percent:.2f}%    {memory_percent:.2f}%"
                    if i == selected_process:
                        stdscr.addstr(monitor_height + i - top_process + 3, 0, proc_line, curses.color_pair(COLOR_CYAN) | curses.A_STANDOUT)
                    else:
                        stdscr.addstr(monitor_height + i - top_process + 3, 0, proc_line)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            stdscr.refresh()

            # Control de teclado
            key = stdscr.getch()
            if key == curses.KEY_UP:
                selected_process = max(0, selected_process - 1)
                if selected_process < top_process:
                    top_process = selected_process
            elif key == curses.KEY_DOWN:
                selected_process = min(num_processes - 1, selected_process + 1)
                if selected_process >= top_process + max_display_lines:
                    top_process = selected_process - max_display_lines + 1
            elif key == ord('q'):
                break

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    curses.wrapper(mostrar_monitor_recursos)
