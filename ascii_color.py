class Tc:
    '''Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    RESET='\033[0m'
    BOLD='\033[01m'
    DISABLE='\033[02m'
    UNDERLINE='\033[04m'
    REVERSE='\033[07m'
    STRIKETHROUGH='\033[09m'
    INVISIBLE='\033[08m'
    ITALIC='\33[3m'
    class Fg:
        BLACK='\033[30m'
        RED='\033[31m'
        GREEN='\033[32m'
        BLUE='\033[34m'
        PURPLE='\033[35m'
        CYAN='\033[36m'
        LIGHTGREY='\033[37m'
        DARKGREY='\033[90m'
        LIGHTRED='\033[91m'
        LIGHTGREEN='\033[92m'
        YELLOW='\033[93m'
        LIGHTBLUE='\033[94m'
        PINK='\033[95m'
        LIGHTCYAN='\033[96m'
    class Bg:
        BLACK='\033[40m'
        RED='\033[41m'
        GREEN='\033[42m'
        YELLOW='\033[43m'
        BLUE='\033[44m'
        PURPLE='\033[45m'
        CYAN='\033[46m'
        LIGHTGREY='\033[47m'