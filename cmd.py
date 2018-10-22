import os
from pathlib import Path
from NFO import NFO

VERSION = '1.0.5'
cmds = [{'h': 'show this Help / command list', 'q': 'Quit', 'p': 'Print .nfo', 's': 'Save .nfo'},
        {'ac': 'Add a Category', 'dc': 'Delete a Category', 'mc': 'Move a Category', 'rc': 'Rename a Category'},
        {'al': 'Add a Line to a category', 'dl': 'Delete a Line', 'ml': 'Move a Line inside a category',
         'mlc': 'Move a Line to another Category'}]


def available_cmds(nfo):
    res = ['h', 'q', 'p', 's', 'ac']
    nb_ctgs = len(nfo.ctgs)
    if nb_ctgs > 0:
        res.extend(['dc', 'rc', 'al'])
    if nb_ctgs > 1:
        res.append('mc')
    if nfo.contains_line():
        res.extend(['dl', 'ml'])
        if nb_ctgs > 1:
            res.append('mlc')
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
    res = '------------ Commands -----------\n'
    for cmd_type in cmds:
        lf = False
        for (cmd, desc) in cmd_type.items():
            if cmd in available:
                res += cmd.ljust(4) + desc + '\n'
                lf = True
        res += '\n' if lf else ''
    print(res[:-1] + '---------------------------------')


def print_nfo(nfo: NFO):
    cls()
    print(str(nfo) + '\n')
