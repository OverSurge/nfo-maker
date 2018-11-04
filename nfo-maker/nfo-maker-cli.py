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

"""Command Line Interface version of NFO Maker."""

import os
import commands
from NFO import NFO

VERSION = '1.2.3'


def cls() -> None:
    """Clear the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main() -> None:
    try:
        cls()
        mode = input('┌──────────────────────────┐\n│   NFO Maker CLI v{}   │\n└╥─────────────────────────┘\n ║\n'
                     ' ╠ n: Create a new .nfo\n ║\n ╠ l: Load an existing .nfo\n ║\n ╚ q: Quit\n\n> '
                     .format(VERSION))
        cls()
        if mode == 'l':
            loaded = False
            while not loaded:
                try:
                    NFO.load()
                    loaded = True
                except (IndexError, ValueError):
                    print('Incorrect index.')
        elif mode == 'q':
            print('Exiting NFO Maker CLI.')
            return
        else:
            NFO()
        cls()
        print(NFO)
        commands.print_commands()
        while True:
            action = input('> ')
            cls()
            try:
                if action in commands.available_commands():
                    if action == 'h':
                        commands.print_commands()

                    elif action == 'q':
                        print('Exiting NFO Maker CLI.')
                        break

                    elif action == 'r':
                        NFO.rename()

                    elif action == 'p':
                        cls()
                        print(NFO)

                    elif action == 's':
                        NFO.save()

                    elif action == 'l':
                        NFO.load()

                    elif action == 'w':
                        NFO.set_max_width()

                    elif action == 'ac':
                        NFO.add_ctg()

                    elif action == 'dc':
                        NFO.del_ctg()

                    elif action == 'mc':
                        NFO.move_ctg()

                    elif action == 'rc':
                        NFO.ren_ctg()

                    elif action == 'al':
                        NFO.add_line()

                    elif action == 'dl':
                        NFO.del_line()

                    elif action == 'ml':
                        NFO.move_line()

                    elif action == 'mlc':
                        NFO.move_line_to_ctg()

                    elif action == 'rl':
                        NFO.ren_line()

                    if action in ['r', 'l', 'w', 'ac', 'dc', 'mc', 'rc', 'al', 'dl', 'ml', 'mlc', 'rl']:
                        cls()
                        print(NFO)
                        commands.print_commands()
                else:
                    commands.print_commands()
            except (EOFError, FileExistsError, FileNotFoundError, IndexError, ValueError):
                cls()
                commands.print_commands()
            except KeyboardInterrupt:
                cls()
                print('Exiting NFO Maker CLI.')
                break
    except (EOFError, KeyboardInterrupt):
        cls()
        print('Exiting NFO Maker CLI.')
        exit()


if __name__ == '__main__':
    main()
