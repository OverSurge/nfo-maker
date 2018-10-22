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
                    if action == '?' or action == 'h':
                        cmd.print_cmds(nfo)

                    elif action == 'q':
                        print('Exiting NFO Maker CLI.')
                        break

                    elif action == 's':
                        if nfo.is_valid():
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

                    if action in ['p', 'ac', 'dc', 'mc', 'rc', 'al']:
                        cmd.print_nfo(nfo)
                else:
                    cmd.print_cmds(nfo)
            except EOFError:
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
