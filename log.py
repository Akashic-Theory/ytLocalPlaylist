import colorama


def error(message: str):
    print(f"{colorama.Fore.RED}{message}{colorama.Fore.RESET}")
