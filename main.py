from bot import start
from parse_data import get_current_df, last_update_time
from datetime import datetime
import time


def main():
    _ = start()
    while True:
        current_time = datetime.now()
        if current_time.hour == 17 and current_time.minute == 37:
            get_current_df()
            time.sleep(80)


if __name__ == '__main__':
    main()
