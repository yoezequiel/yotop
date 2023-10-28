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
    max_bar_width = sw - 30

    init_colors()
    try:
        while True:
            stdscr.clear()

            # Actualiza las dimensiones de la ventana si cambia el tamaño de la terminal
            sh, sw = stdscr.getmaxyx()
            max_bar_width = sw - 30

            # Monitor de recursos
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            mem_info = psutil.virtual_memory()
            swap_info = psutil.swap_memory()

            stdscr.addstr(
                0,
                0,
                "yotop by:yoezequiel",
                curses.color_pair(COLOR_CYAN) | curses.A_BOLD,
            )
            for i, percent in enumerate(cpu_percent):
                bar_length = int(percent / 100 * max_bar_width)
                cpu_line = f"CPU {i + 1}: [{('=' * bar_length)}{(' ' * (max_bar_width - bar_length))}] {percent}%"
                if percent > 80:
                    stdscr.addstr(i + 2, 0, cpu_line, curses.color_pair(COLOR_RED))
                else:
                    stdscr.addstr(i + 2, 0, cpu_line, curses.color_pair(COLOR_GREEN))
            ram_bar_length = int((mem_info.used / mem_info.total) * max_bar_width)
            ram_line = f"RAM: [{('=' * ram_bar_length)}{(' ' * (max_bar_width - ram_bar_length))}] {mem_info.used / (1024**3):.2f} GB / {mem_info.total / (1024**3):.2f} GB"
            stdscr.addstr(
                len(cpu_percent) + 3, 0, ram_line, curses.color_pair(COLOR_YELLOW)
            )
            swap_bar_length = int((swap_info.used / swap_info.total) * max_bar_width)
            swap_line = f"Swp: [{('=' * swap_bar_length)}{(' ' * (max_bar_width - swap_bar_length))}] {swap_info.used / (1024**3):.2f} GB / {swap_info.total / (1024**3):.2f} GB"
            stdscr.addstr(
                len(cpu_percent) + 4, 0, swap_line, curses.color_pair(COLOR_YELLOW)
            )

            # Control de teclado
            key = stdscr.getch()
            if key == ord("q") or key == ord("Q"):
                break

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(mostrar_monitor_recursos)
