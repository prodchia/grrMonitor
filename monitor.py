import os
import getpass
import subprocess
import time
import datetime as dt


def get_last_lines(file_path, num_lines=5):
    with open(file_path, 'rb') as file:
        file.seek(-2, 2)  # Seek to the second-to-last character

        lines = []
        line_count = 0

        while line_count < num_lines:
            while file.read(1) != b'\n':  # Iterate until finding a newline character
                file.seek(-2, 1)  # Seek back by 2 characters

            lines.append(file.readline().decode().strip())  # Read and decode the line
            line_count += 1

            if file.tell() <= 1:  # Break the loop if reached the beginning of the file
                break

    return lines[::-1]

def monitor():
    # monitors GRResult error
    user = getpass.getuser()
    debug_file_path = f"C:\\Users\\{user}\\.chia\\mainnet\\log\\debug.log"
    chia_location = f'C:\\Users\\{user}\\AppData\\Local\\Programs\\Chia\\'
    cli_location = os.path.join(chia_location, 'resources\\app.asar.unpacked\\daemon')


    # Continuously monitor the file for changes
    while True:
        line = get_last_lines(debug_file_path)
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
