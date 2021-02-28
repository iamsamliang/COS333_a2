# COS 333 Assignment 2: A Registrar Application Using Graphical User Interface and Network Programming
# Authors: Sam Liang, Sumanth Maddirala
# Description: Presents information on Princeton Course Offerings based on specified criteria

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
from regdetails import course_details

# regserver.py handles database


def main(argv):
    # argparse is user-interface related code
    # Create parser that has a description of the program and host/port positional arguments
    parser = argparse.ArgumentParser(
        description='Client for the registrar application', allow_abbrev=False)
    parser.add_argument(
        "host", type=str, help="the host on which the server is running", nargs=1)
    parser.add_argument(
        "port", type=int, help="the port at which the server is listening", nargs=1)
    args = parser.parse_args()

    # database code
    try:
        # initiation code line
        app = QApplication(argv)

        # Textfields for a dept, coursenum, area, title
        deptLab = QLabel("Dept:")
        deptLine = QLineEdit()
        courseLab = QLabel("Number:")
        courseNumLine = QLineEdit()
        areaLab = QLabel("Area:")
        areaLine = QLineEdit()
        titleLab = QLabel("Title:")
        titleLine = QLineEdit()
        listWidget = QListWidget()

        # submit button
        submit_but = QPushButton("Submit")

        # FIX THIS
        def buttonSlot():
            QMessageBox.information(window, 'Class Details')
            textEdit.append()

        # source: https://www.programcreek.com/python/example/101657/PyQt5.QtCore.Qt.Key_Up
        def keyPressEvent(self, event):
            key = event.key()
            if (key == Qt.Key_Tab):

            elif (key == Qt.Key_Up):

            elif (key == Qt.Key_Left):

            elif (key == Enter):

        def
        submit_but.clicked.connect(buttonSlot)

        # list box that can scroll vertically and horizontally
        list_box = QListWidget()

        # when the user opens the application or has nothing in the input boxes, we need to display all classes in order of classid, department, coursenum, area, title. must have table format

        # when the user hits the submit button, we need to extract the input arguments and list all the classes that match those criteria. Use reg.py to get the list of entries

        # in the list box, must default highlight the first entry before any user clicks
        # when the user single clicks on an entry, we need to highlight it
        # when the user double clicks on an entry, we need to display details about the class in a popup and format it. Use regdetails.py to display the correct information

        # keyboard functionality
        # cycle through the widgets with the tab key
        # in the list box, use arrow keys to go up and down
        # in the list box, hitting enter on a highlighted item opens it
        # close the details box for a selected class item by hitting enter

        # user interface (prints table layout)
        print("ClsId Dept CrsNum Area Title")
        print("----- ---- ------ ---- -----")
        wrapper = textwrap.TextWrapper(
            width=72, break_long_words=False, subsequent_indent=(23 * ' '))

        # user interface: gets information from the database
        # and prints to user
        row = cursor.fetchone()
        while row is not None:
            unformatted_str = "{:>5} {:>4} {:>6} {:>4} {}".format(
                str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))

            print(wrapper.fill(unformatted_str))
            row = cursor.fetchone()

# exit(2) case handled by arg_parse module, exit(1) case handled on lines 11-18
# If some other program has corrupted the reg.sqlite database file
# (missing table, missing field, etc.) such that a database query
# performed by reg.py throws an exception, then reg.py must write
# the message that is within that exception to stderr. exit status 1
    except Exception as e:
        print(f'{argv[0]}: {e}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main(argv)
