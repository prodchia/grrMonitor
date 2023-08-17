import os
import re
import getpass
import subprocess
import time
import datetime as dt
import click


def read_file(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'GRResult', line)
            if match:
                lines.append(line)

    return lines



def monitor(monitor_freq = 30):

    # monitors GRResult error
    user = getpass.getuser()
    debug_file_path = f"C:\\Users\\{user}\\.chia\\mainnet\\log\\debug.log"
    chia_location1 = fr"C:\Users\{user}\AppData\Local\Programs\Chia\resources\app.asar.unpacked\daemon"
    chia_location2 = r'"C:\Program Files\Chia\resources\app.asar.unpacked\daemon"'


    if os.path.exists(chia_location1):
        command = chia_location1 + '\\chia start harvester -r'
    elif os.path.exists(chia_location2):
        command = '"C:\\Program Files\\Chia\\resources\\app.asar.unpacked\\daemon\\chia" start harvester -r'
    else:
        raise ValueError('Cannot find chia installed on this system')





    # Continuously monitor the file for changes
    print(f"Starting GRR error monitor at {dt.datetime.now()}. Checking every {monitor_freq} seconds")


    while True:
        line = read_file(debug_file_path)

        if len(line) > 0:
            date_str = re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', line[-1]).group()
            error_time = dt.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

            time_elapsed = (dt.datetime.now() - error_time).total_seconds()

            if time_elapsed < 1.8*monitor_freq:
                print(f'{dt.datetime.now()} : GRR Error found. Restarting harvester')
                print(line[-1])

                result = subprocess.run( command , shell=True, capture_output=True, text=True)

                # Access the output and return code
                output = result.stdout
                error = result.stderr
                return_code = result.returncode

                print(f"{output} \n {error} \n {return_code}")

        time.sleep(monitor_freq)

@click.command()
@click.option('--freq',
              required = False,
              type=int,
              default=30,
              show_default=True)

def main(freq):
    monitor(monitor_freq=freq)

if __name__ == "__main__":
    main()

