from sys import stdin, stdout
from pybifrost.server import Server

def main():
    server = Server(infile=stdin, outfile=stdout)
    server.start()
