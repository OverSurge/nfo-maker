from NFO import NFO


def main():
    print("NFO Maker cli v1.0\n")
    title = None
    while title is None:
        print("Please enter a title :")
        title = input()
    nfo = NFO(title)
    while True:
        print(str(nfo))
        input()


if __name__ == "__main__":
    main()
