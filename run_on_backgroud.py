import subprocess


def main():
    # Launch the Python script in the background and redirect output to a file
    with open('output.log', 'w') as f:
        subprocess.Popen(['python', 'process_manager.py'], stdout=f, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main()
