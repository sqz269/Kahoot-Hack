import logging
from colorama import init, Fore


def init_logging(level_stdout=logging.INFO, level_IO=logging.WARNING, name="bot"):
    init(autoreset=True)
    logging.addLevelName(logging.DEBUG, f"{Fore.CYAN}{logging.getLevelName(logging.DEBUG)}{Fore.RESET}")
    logging.addLevelName(logging.INFO, f"{Fore.LIGHTBLUE_EX}{logging.getLevelName(logging.INFO)}{Fore.RESET}")
    logging.addLevelName(logging.WARNING, f"{Fore.LIGHTYELLOW_EX}{logging.getLevelName(logging.WARNING)}{Fore.RESET}")
    logging.addLevelName(logging.ERROR, f"{Fore.LIGHTRED_EX}{logging.getLevelName(logging.ERROR)}{Fore.RESET}")
    logging.addLevelName(logging.CRITICAL, f"{Fore.LIGHTRED_EX}{logging.getLevelName(logging.CRITICAL)}{Fore.RESET}")
    server = logging.getLogger(name)
    server.setLevel(logging.DEBUG)

    file = f"{name}_ops.log"
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(level_IO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level_stdout)

    stream_handler.setFormatter(logging.Formatter('%(asctime)s | <%(name)s> [%(levelname)s]: %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
    file_handler.setFormatter(logging.Formatter('%(asctime)s | <%(name)s> [%(threadName)s] [%(levelname)s]: %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))

    server.addHandler(file_handler)
    server.addHandler(stream_handler)

    return name
