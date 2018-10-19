import os

from pathlib import Path

from NFO import NFO


def commands(nfo: NFO):
    res = 'Choose an action :\n?|h Show this command list\nq   Quit\np   Print .nfo\nw   Write .nfo to file'
    if len(nfo.ctgs) > 1:
        res += 'mc  Move a category\n'
    return res


def main():
    print('NFO Maker cli v1.0.0\n')
    title = None
    while title is None:
        print('Please enter a title :')
        title = input()
    nfo = NFO(title)
    print(commands(nfo))
    while True:
        action = input()
        if action == '?' or action == 'h':
            print(commands(nfo))
        elif action == 'q':
            print('Closing NFO Maker cli...')
            break
        elif action == 'p':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(str(nfo))
        elif action == 'w':
            print('Enter a full file path or leave empty to write at {}'
                  .format(Path('.' + '/' + nfo.name + '.nfo').absolute()))
            path = input()
            print(nfo.write()) if path == '' else print(nfo.write(path))
        else:
            print(commands(nfo))


if __name__ == '__main__':
    main()
