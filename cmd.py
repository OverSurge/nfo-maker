# NFO Maker
# Copyright (C) 2018  OverSurge
#
# NFO Maker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NFO Maker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NFO Maker.  If not, see <https://www.gnu.org/licenses/>.

import os
import typing
from NFO import NFO

VERSION = '1.0.9'
cmds = [{'h': 'show this Help / command list', 'q': 'Quit', 'r': 'Rename .nfo', 'p': 'Print .nfo', 's': 'Save .nfo',
         'l': 'Load .nfo'},
        {'ac': 'Add a Category', 'dc': 'Delete a Category', 'mc': 'Move a Category', 'rc': 'Rename a Category'},
        {'al': 'Add a Line to a category', 'dl': 'Delete a Line', 'ml': 'Move a Line inside a category',
         'mlc': 'Move a Line to another Category', 'rl': 'Rename a Line\'s name and/or value'}]


def available_cmds() -> typing.List[str]:
    res = ['h', 'q', 'r', 'p', 's', 'l', 'ac']
    nb_ctgs = len(NFO.ctgs)
    if nb_ctgs > 0:
        res.extend(['dc', 'rc', 'al'])
    if nb_ctgs > 1:
        res.append('mc')
    if NFO.contains_line():
        res.append('dl')
        for ctg in NFO.ctgs:
            if len(ctg.lines) > 1:
                res.append('ml')
                break
        if nb_ctgs > 1:
            res.append('mlc')
        res.append('rl')
    return res


def cls() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def print_cmds() -> None:
    available = available_cmds()
    res = '-------------- Commands -------------\n'
    for cmd_type in cmds:
        lf = False
        for (cmd, desc) in cmd_type.items():
            if cmd in available:
                res += cmd.ljust(4) + desc + '\n'
                lf = True
        res += '\n' if lf else ''
    print(res[:-1] + '-------------------------------------')


def print_nfo() -> None:
    cls()
    print(NFO)
