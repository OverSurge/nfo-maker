import os

from pathlib import Path

from NFO import NFO

cmds = [{'h': 'Show this help / command list', 'q': 'Quit', 'p': 'Print .nfo', 's': 'Save .nfo'},
        {'ac': 'Add a category', 'dc': 'Delete a category', 'mc': 'Move a category', 'rc': 'Rename a category'}]


def available_cmds(nfo):
    res = ['h', 'q', 'p', 's', 'ac']
    if len(nfo.ctgs) > 0:
        res.extend(['dc', 'rc'])
    if len(nfo.ctgs) > 1:
        res.append('mc')
    return res


def choose_path(nfo: NFO):
    folder = input('Enter a folder path (leave empty to save in {})\n> '.format(Path().absolute()))
    folder = '.' if folder == '' else folder
    filename = input('Enter a filename (leave empty to save as {})\n> '.format(nfo.name + '.nfo'))
    if filename == '':
        filename = nfo.name + '.nfo'
    else:
        filename += '.nfo' if filename[:-4] == '.nfo' else ''
    path = Path(folder + '/' + filename).absolute()
    if input('{}\nIs this path right ? (Y/n)\n> '.format(path)).lower() == 'y':
        nfo.path = path
        return True
    else:
        return False


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_cmds(nfo: NFO):
    available = available_cmds(nfo)
    res = '----------- Commands ------------\n'
    for cmd_type in cmds:
        for (cmd, desc) in cmd_type.items():
            if cmd in available:
                res += cmd.ljust(4) + desc + '\n'
        res += '\n'
    print(res[:-1])


def print_nfo(nfo: NFO):
    cls()
    print(str(nfo))
