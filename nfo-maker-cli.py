import os

from pathlib import Path

from NFO import NFO


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def commands(nfo: NFO):
    res = 'Choose an action :\n' \
          '?|h Show this command list\n' \
          'q   Quit\n' \
          'p   Print .nfo\n' \
          'w   Write .nfo to file\n\n' \
          'ac  Add a category\n' \
          'rc  Remove a category'
    if len(nfo.ctgs) > 1:
        res += 'mc  Move a category\n'
    return res


def main():
    print('NFO Maker cli v1.0.1\n')
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
        elif action == 'w':
            path = input('Enter a full file path or leave empty to write at {}\n'.format
                         (Path('.' + '/' + nfo.name + '.nfo').absolute()))
            # TODO : Print full path and ask for confirmation
            print(nfo.write()) if path == '' else print(nfo.write(path))
        else:
            print(commands(nfo))


if __name__ == '__main__':
    main()
