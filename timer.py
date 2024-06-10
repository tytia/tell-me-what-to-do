import os, time, settings
from art import text2art

def get_length() -> int:
    return settings.get("timer_length", 30 * 60)

def format_seconds(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def format_seconds_duration(seconds: int) -> str:
    if seconds == 0: return "disabled"

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    res = ""

    if h: res += f"{h}h "
    if m: res += f"{m}m "
    if s: res += f"{s}s"

    return res.strip()

def start():
    # t is in seconds
    t = get_length()
    if t == 0:
        # timer is disabled
        os.system("pause")
        return

    try:
        print("\033[?25l", end="") # hide cursor
        prev_width = 0
        while t:
            timeformat = format_seconds(t)
            # add spaces to ensure that the previous time is fully overwritten
            # print(timeformat + (" " * max(prev_width - len(timeformat), 0)), end='\r')
            text = text2art(timeformat, font="roman")
            print(text, end="")
            prev_width = len(timeformat)

            time.sleep(1)
            clear_lines(text.count("\n"))
            t -= 1

    except KeyboardInterrupt:
        print("\nTimer stopped.")
        time.sleep(0.01) # https://stackoverflow.com/questions/57729782/ctrlc-sends-eoferror-once-after-cancelling-process
        os.system("pause")
        print("\033[?25h", end="") # show cursor
        return
    
    print("\nnice work :)")
    print("feel free to continue or receive a new task!")
    os.system("pause")
    print("\033[?25h", end="") # show cursor

def clear_lines(n: int) -> None:
    """
    Clear the last n lines of the terminal.
    """
    print("\033[F\033[K" * n, end="")


if __name__ == "__main__":
    start()