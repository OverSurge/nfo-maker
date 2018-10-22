import cmd

from NFO import NFO


def main() -> None:
    try:
        cmd.cls()
        print('NFO Maker cli v1.0.4\n')
        nfo = NFO()
        cmd.cls()
        cmd.print_cmds(nfo)
        while True:
            try:
                action = input('> ')
                cmd.cls()
                if action in cmd.available_cmds(nfo):
                    if action == '?' or action == 'h':
                        cmd.print_cmds(nfo)

                    elif action == 'q':
                        cmd.cls()
                        print('Exiting NFO Maker CLI.')
                        break

                    elif action == 'p':
                        cmd.print_nfo(nfo)

                    elif action == 's':
                        if nfo.is_valid():
                            nfo.save() if cmd.choose_path(nfo) else print('Canceled writing.')

                    elif action == 'ac':
                        nfo.add_ctg()
                        cmd.print_nfo(nfo)
                        cmd.print_cmds(nfo)

                    elif action == 'dc':
                        nfo.del_ctg()
                        cmd.print_nfo(nfo)

                    elif action == 'mc':
                        nfo.move_ctg()
                        cmd.print_nfo(nfo)
                        cmd.print_cmds(nfo)

                    elif action == 'rc':
                        nfo.ren_ctg()
                        cmd.print_nfo(nfo)

                else:
                    cmd.cls()
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
