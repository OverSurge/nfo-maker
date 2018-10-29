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

import cmd
from NFO import NFO


def main() -> None:
    try:
        cmd.cls()
        print('NFO Maker CLI v{}\n'.format(cmd.VERSION))
        NFO()
        cmd.cls()
        cmd.print_cmds()
        while True:
            action = input('> ')
            cmd.cls()
            try:
                if action in cmd.available_cmds():
                    if action == 'h':
                        cmd.print_cmds()

                    elif action == 'q':
                        print('Exiting NFO Maker CLI.')
                        break

                    elif action == 'r':
                        NFO.rename()

                    elif action == 'p':
                        cmd.print_nfo()

                    elif action == 's':
                        NFO.save()

                    elif action == 'l':
                        NFO.load()

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

                    if action in ['r', 'l', 'ac', 'dc', 'mc', 'rc', 'al', 'dl', 'ml', 'mlc', 'rl']:
                        cmd.print_nfo()
                        cmd.print_cmds()
                else:
                    cmd.print_cmds()
            except (EOFError, IndexError, ValueError):
                cmd.cls()
                cmd.print_cmds()
            except KeyboardInterrupt:
                cmd.cls()
                print('Exiting NFO Maker CLI.')
                break
    except (EOFError, KeyboardInterrupt):
        cmd.cls()
        print('Exiting NFO Maker CLI.')
        exit()


if __name__ == '__main__':
    main()
