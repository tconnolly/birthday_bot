import logging
from birthday.client import Client

logging.basicConfig(level=logging.INFO)


def main():
    client = Client()
    client.run('NTA0MjQyMjkxMTk2NjkwNDQ0.DrCL5g.7AKoVGHQIUKzFJhkEetQefE3FSg')


if __name__ == '__main__':
    main()
