import sys
from parser_toml import Parser


def main():
    language = sys.argv[1]
    file_path = sys.argv[2]

    parser = Parser(language)
    with open(file_path, 'r') as f:
        toml = f.read()
    output = parser.parse(toml)

    with open('output.' + language.lower(), 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()
