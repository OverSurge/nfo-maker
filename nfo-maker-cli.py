import os

from pathlib import Path

from NFO import NFO


def choose_path(nfo: NFO):
    folder = input('Enter a folder path (leave empty to save in {})\n'.format(Path().absolute()))
    folder = '.' if folder == '' else folder
    filename = input('Enter a filename (leave empty to save as {})\n'.format(nfo.name + '.nfo'))
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


def commands(nfo: NFO):
    res = 'Choose an action :\n' \
          '?|h Show this command list\n' \
          'q   Quit\n' \
          'p   Print .nfo\n' \
          's   Save .nfo\n\n' \
          'ac  Add a category\n' \
          'rc  Remove a category'
    if len(nfo.ctgs) > 1:
        res += 'mc  Move a category\n'
    return res


def main():
    print('NFO Maker cli v1.0.2\n')
    title = input('Please enter a title :\n')
    if title == '':
        title = 'Unnamed'
    cls()
    nfo = NFO(title)
    print(commands(nfo))
    while True:
        action = input('\n> ')
        cls()
        if action == '?' or action == 'h':
            print(commands(nfo))

        elif action == 'q':
            print('Closing NFO Maker cli...')
            break

        elif action == 'p':
            print(str(nfo))

        elif action == 's':
            if nfo.is_valid():
                nfo.save() if choose_path(nfo) else print('Writing canceled.')

        else:
            print(commands(nfo))


if __name__ == '__main__':
    main()
