import os
import getpass
import subprocess
import time
import datetime as dt


def get_last_line(file_path):
    with open(file_path, 'rb') as file:
        file.seek(-2, 2)  # Seek to the second-to-last character

        while file.read(1) != b'\n':  # Iterate until finding the last newline character
            file.seek(-2, 1)  # Seek back by 2 characters

        last_line = file.readline().decode().strip()  # Read and decode the last line

    return last_line

def monitor():
    # monitors GRResult error
    user = getpass.getuser()
    debug_file_path = f"C:\\Users\\{user}\\.chia\\mainnet\\log\\debug.log"
    chia_location = f'C:\\Users\\{user}\\AppData\\Local\\Programs\\Chia\\'
    cli_location = os.path.join(chia_location, 'resources\\app.asar.unpacked\\daemon')


    # Continuously monitor the file for changes
    while True:
        line = get_last_line(debug_file_path)
        print(f'{dt.datetime.now()} : Monitoring for GRR Error')

        if 'GRResult'  in line:
            print(f'{dt.datetime.now()} : GRR Error found. Restarting harvester')
            command = cli_location + '\\chia start harvester -r'
            print(command)

            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Access the output and return code
            output = result.stdout
            error = result.stderr
            return_code = result.returncode

            print(f"{output} \n {error} \n {return_code}")

        time.sleep(30)


if __name__ == "__main__":
    monitor()
