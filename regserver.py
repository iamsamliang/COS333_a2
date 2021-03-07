from os import path
from sys import argv, stderr, exit
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dump, load
from sqlite3 import connect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QScrollArea
from PyQt5.QtWidgets import QSlider, QCheckBox, QRadioButton
from PyQt5.QtWidgets import QListWidget, QDesktopWidget
from PyQt5.QtCore import Qt
import argparse
import textwrap
from database_handler import create_sql_command


# determine whether to call handleOverviews or handleDetails
def handler(sock, cursor):
    in_flow = sock.makefile(mode="rb")
    package = load(in_flow)
    if package[0] == "overviews":
        handleOverviews(sock, cursor, package)
    else:
        handleDetails(sock, cursor, package)


# handle getOverviews:
def handleOverviews(sock, cursor, args):
    print("Received command: getOverviews")

    # args is a list that stores all the arguments needed for sql command
    # create appropriate sql command
    sql_command, arg_arr = create_sql_command(args)
    # cursor.execute here
    cursor.execute(sql_command, arg_arr)
    # then return cursor.fetchall (all rows from database) here using dump() and flush()
    out_flow = sock.makefile(mode="wb")
    rows = cursor.fetchall()
    dump(rows, out_flow)
    out_flow.flush()


# handle getDetails
def handleDetails(sock, cursor, package):
    sql_command1 = "SELECT classes.courseid, classes.days, classes.starttime, classes.endtime, classes.bldg, classes.roomnum, crosslistings.dept, crosslistings.coursenum, courses.area, courses.title, courses.descrip, courses.prereqs FROM classes, crosslistings, courses WHERE classes.courseid = courses.courseid AND crosslistings.courseid = courses.courseid AND classid=? ORDER BY dept ASC, coursenum ASC"

    # fetching professors if any
    sql_command2 = "SELECT profs.profname FROM coursesprofs, profs WHERE coursesprofs.courseid=? AND coursesprofs.profid=profs.profid ORDER BY profname"

    # get the arguments from the client and load them into args
    flo = sock.makefile(mode="rb")
    args = load(flo)

    cursor.execute(sql_command1, args.classid)
    row = cursor.fetchone()

    if row is None:
        print(f"{argv[0]}: no class with classid " +
              str(args.classid[0]) + " exists", file=stderr)
        exit(1)

    firstrow = row
    courseid = str(row[0])
    wrapper = textwrap.TextWrapper(
        width=72, break_long_words=False)
    wrapper_spec = textwrap.TextWrapper(
        width=72)
    print(wrapper.fill(f"Course Id: {courseid}"))
    print()
    print(f"Days: {str(row[1])}")
    print(f"Start time: {str(row[2])}")
    print(f"End time: {str(row[3])}")
    print(f"Building: {str(row[4])}")
    print(f"Room: {str(row[5])}")
    print()
    print(wrapper.fill(f"Dept and Number: {str(row[6])} {str(row[7])}"))

    row = cursor.fetchone()
    while row is not None:
        print(wrapper.fill(f"Dept and Number: {str(row[6])} {str(row[7])}"))
        row = cursor.fetchone()

    print()
    # print(wrapper.fill("Area: " + str(firstrow[8])))
    print(f"Area: {str(firstrow[8])}")
    print()
    print(wrapper.fill(f"Title: {str(firstrow[9])}"))
    print()
    print(wrapper.fill(f"Description: {str(firstrow[10])}"))
    print()
    print(wrapper_spec.fill(f"Prerequisites: {str(firstrow[11])}"))
    print()

    cursor.execute(sql_command2, [courseid])
    row = cursor.fetchone()
    while row is not None:
        print(f"Professor: {str(row[0])}")
        row = cursor.fetchone()


def main(argv):
    DATABASE_NAME = "reg.sqlite"

    # user-interface code
    if not path.isfile(DATABASE_NAME):
        print(f'{argv[0]}: database reg.sqlite not found', file=stderr)
        exit(1)

    # argparse is user-interface related code
    # Create parser that has a description of the program and host/port positional arguments
    parser = argparse.ArgumentParser(
        description='Server for the registrar application', allow_abbrev=False)
    parser.add_argument(
        "port", type=int, help="the port at which the server should listen", nargs=1)
    args = parser.parse_args()

    try:
        # connect to database
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()

        # make this server bind a socket to this port and listen for a connection from a client
        port = int(argv[1])
        serverSock = socket()
        print('Opened server socket')
        serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSock.bind(('', port))
        print("Bound server socket to port")
        serverSock.listen()
        print('Listening')

        while True:
            try:
                sock, client_addr = serverSock.accept()
                print('Accepted connection, opened socket')
                handler(sock, cursor)
                sock.close()
                print('Closed socket')
            except Exception as e:
                print(e, file=stderr)

        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)


if __name__ == '__main__':
    main(argv)
