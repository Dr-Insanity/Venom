from typing import Union
from colorama import init, Fore

init(autoreset=True)

BOLD = "\033[1m"
PURPLE = "\033[38;5;57m"


class OccuredEventTypes:
    class Command:
        def __init__(self, stealth: bool):
            self._stealth = stealth

        def __str__(self):
            if not self._stealth:
                return f"{BOLD+Fore.MAGENTA}ON COMMAND{Fore.RESET} "
            return (
                f"{BOLD+Fore.MAGENTA}ON COMMAND{PURPLE} 🛡️ STEALTH{Fore.RESET} "
            )

    class DeletedMessage:
        def __str__(self):
            return f"{BOLD+PURPLE}MSG DELETE{Fore.RESET} "

    class BulkDeletedMessages:
        def __str__(self):
            return f"{BOLD+PURPLE}BULK MSG DELETE{Fore.RESET} "


class TerminalLogType:
    class ExecutedCommmand:
        def __str__(self):
            return f"{BOLD+PURPLE}COMMAND{Fore.RESET} "

    class EventOccured:
        def __init__(
            self,
            event_type: Union[
                OccuredEventTypes.Command, OccuredEventTypes.DeletedMessage
            ],
        ):
            self._event_type = event_type

        def __str__(self):
            return f"{BOLD+PURPLE}EVENT {self._event_type}{Fore.RESET}"

    class Testing:
        def __str__(self):
            return f"{BOLD+PURPLE}TEST{Fore.RESET} "


class TerminalSeverities:
    class INFO:
        def __str__(self):
            return f" {BOLD+Fore.BLUE}INFO{Fore.RESET} "

    class TEST:
        def __str__(self):
            return f" {BOLD+Fore.YELLOW}TEST{Fore.RESET} "

    class WARN:
        def __str__(self):
            return f" {BOLD+Fore.YELLOW}WARN{Fore.RESET} "

    class FATAL:
        def __str__(self):
            return f" {BOLD+Fore.RED}FATAL{Fore.RESET} "
