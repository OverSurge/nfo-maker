import os
import typing
from pathlib import Path
from NFO import NFO

VERSION = '1.0.8'
cmds = [{'h': 'show this Help / command list', 'q': 'Quit', 'r': 'Rename .nfo', 'p': 'Print .nfo', 's': 'Save .nfo'},
        {'ac': 'Add a Category', 'dc': 'Delete a Category', 'mc': 'Move a Category', 'rc': 'Rename a Category'},
        {'al': 'Add a Line to a category', 'dl': 'Delete a Line', 'ml': 'Move a Line inside a category',
         'mlc': 'Move a Line to another Category', 'rl': 'Rename a Line\'s name and/or value'}]


def available_cmds(nfo: NFO) -> typing.List[str]:
    res = ['h', 'q', 'r', 'p', 's', 'ac']
    nb_ctgs = len(nfo.ctgs)
    if nb_ctgs > 0:
        res.extend(['dc', 'rc', 'al'])
    if nb_ctgs > 1:
        res.append('mc')
    if nfo.contains_line():
        res.append('dl')
        for ctg in nfo.ctgs:
            if len(ctg.lines) > 1:
                res.append('ml')
                break
        if nb_ctgs > 1:
            res.append('mlc')
        res.append('rl')
    return res


def choose_path(nfo: NFO) -> bool:
    folder = input('Enter a folder path (leave empty to save in {})\n> '.format(Path().absolute()))
    folder = '.' if folder == '' else folder
    filename = input('Enter a filename (leave empty to save as {})\n> '.format(nfo.name + '.nfo'))
    if filename == '':
        filename = nfo.name + '.nfo'
    else:
        filename += '.nfo' if filename[:-4] == '.nfo' else ''
    path = Path(folder + '/' + filename).absolute()
    if input('{}\nIs this path right ? (Y/n)\n> '.format(path)).upper() == 'Y':
        nfo.path = path
        return True
    else:
        return False


def cls() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def print_cmds(nfo: NFO) -> None:
    available = available_cmds(nfo)
    res = '-------------- Commands -------------\n'
    for cmd_type in cmds:
        lf = False
        for (cmd, desc) in cmd_type.items():
            if cmd in available:
                res += cmd.ljust(4) + desc + '\n'
                lf = True
        res += '\n' if lf else ''
    print(res[:-1] + '-------------------------------------')


def print_nfo(nfo: NFO) -> None:
    cls()
    print(nfo)
