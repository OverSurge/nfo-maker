import cmd
from NFO import NFO


def main() -> None:
    try:
        cmd.cls()
        print('NFO Maker CLI v{}\n'.format(cmd.VERSION))
        nfo = NFO()
        cmd.cls()
        cmd.print_cmds(nfo)
        while True:
            action = input('> ')
            cmd.cls()
            try:
                if action in cmd.available_cmds(nfo):
                    if action == 'h':
                        cmd.print_cmds(nfo)

                    elif action == 'q':
                        print('Exiting NFO Maker CLI.')
                        break

                    elif action == 'r':
                        nfo.rename()

                    elif action == 'p':
                        cmd.print_nfo(nfo)

                    elif action == 's':
                        nfo.save() if cmd.choose_path(nfo) else print('Canceled writing.')

                    elif action == 'ac':
                        nfo.add_ctg()

                    elif action == 'dc':
                        nfo.del_ctg()

                    elif action == 'mc':
                        nfo.move_ctg()

                    elif action == 'rc':
                        nfo.ren_ctg()

                    elif action == 'al':
                        nfo.add_line()

                    elif action == 'dl':
                        nfo.del_line()

                    elif action == 'ml':
                        nfo.move_line()

                    elif action == 'mlc':
                        nfo.move_line_to_ctg()

                    elif action == 'rl':
                        nfo.ren_line()

                    if action in ['r', 'ac', 'dc', 'mc', 'rc', 'al', 'dl', 'ml', 'mlc', 'rl']:
                        cmd.print_nfo(nfo)
                        cmd.print_cmds(nfo)
                else:
                    cmd.print_cmds(nfo)
            except (EOFError, IndexError, ValueError):
                cmd.cls()
                cmd.print_cmds(nfo)
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
