import cmd

from NFO import NFO
from Category import Category


def main():
    cmd.cls()
    print('NFO Maker cli v1.0.3\n')
    nfo = NFO(input('Please enter a title :\n> '))
    cmd.cls()
    cmd.print_cmds(nfo)
    while True:
        action = input('> ')
        cmd.cls()
        if action in cmd.available_cmds(nfo):
            if action == '?' or action == 'h':
                cmd.print_cmds(nfo)

            elif action == 'q':
                print('Closing NFO Maker cli...')
                break

            elif action == 'p':
                cmd.print_nfo(nfo)

            elif action == 's':
                if nfo.is_valid():
                    nfo.save() if cmd.choose_path(nfo) else print('Canceled writing.')

            elif action == 'ac':
                nfo.add_ctg(Category(input('Enter new category name :\n> ')))
                cmd.print_nfo(nfo)
                cmd.print_cmds(nfo)

            elif action == 'dc':
                print(nfo.list_ctgs())
                nfo.del_ctg(int(input('Enter the number of the category to delete :\n> ')))
                cmd.print_nfo(nfo)

            elif action == 'mc':
                # TODO : Move categories
                print('Upcoming feature !\n')
                cmd.print_cmds(nfo)

            elif action == 'rc':
                print(nfo.list_ctgs())
                nfo.ren_ctg(int(input('Enter the number of the category to rename :\n> ')))
                cmd.print_nfo(nfo)

        else:
            cmd.cls()
            cmd.print_cmds(nfo)


if __name__ == '__main__':
    main()
