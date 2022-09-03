import subprocess  # nosec


def run_commands(commands):
    for command in commands:
        subprocess.call(command.split(" "))  # nosec
