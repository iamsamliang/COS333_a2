# COS 333 Assignment 2: A Registrar Application Using Graphical User Interface and Network Programming
# Authors: Sam Liang, Sumanth Maddirala
# Description: Presents information on Princeton Course Offerings based on specified criteria

from os import path
from sys import argv, stderr, exit
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dump, load
from sqlite3 import connect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QScrollArea
from PyQt5.QtWidgets import QSlider, QCheckBox, QRadioButton
from PyQt5.QtWidgets import QListWidget, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFont, QEnterEvent
from PyQt5.QtCore import Qt, QItemSelectionModel
import argparse
import textwrap
from database_handler import create_sql_command

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
        # extracts the input in each of the 4 lines when the submit button is clicked, create a socket connection with regserver.py, and send the input to regserver.py. Retrieve the return value from regserver.py and close socket connection
        def retrieveText():
            dept = str(deptLine.text())
            course_num = str(courseNumLine.text())
            area = str(areaLine.text())
            title = str(titleLine.text())

            # prepare the packet to send to regserver.py
            packet = ["overviews", dept, course_num, area, title]

            # send the values to regserver.py
            sock = socket()
            sock.connect((host, port))
            out_flow = sock.makefile(mode='wb')
            dump(packet, out_flow)
            out_flow.flush()

            # retrieve the values from regserver.py
            in_flow = sock.makefile(mode='rb')
            db_rows = load(in_flow)

            # close connection
            sock.close()

            # clear list box and put appropriate items
            list_box.clear()
            for row in db_rows:
                line_string = "{:>5}{:>4}{:>5}{:>4} {}".format(
                    str(row[0]).strip(), str(row[1]).strip(), str(row[2]).strip(), str(row[3]).strip(), str(row[4]).strip())
                list_box.addItem(line_string)

            # automatically highlight first row each time
            list_box.setCurrentRow(0)

        def retrieveDetails():
            # get the courseId from the selection
            selected_str = str(list_box.currentItem().text())
            # selection = selectedRow[0]
            # print(selection)
            words = selected_str.split()
            class_id = int(words[0])
            packet = ["details", class_id]

            # send the values to regserver.py
            sock = socket()
            sock.connect((host, port))
            out_flow = sock.makefile(mode='wb')
            dump(packet, out_flow)
            out_flow.flush()

            # retrieve the values from regserver.py
            in_flow = sock.makefile(mode='rb')
            message = load(in_flow)

            # close connection
            sock.close()

            # create and display information via messageBox
            msgBox = QMessageBox.information(window, 'Class Details', message)

        # get the host and port
        host = argv[1]
        port = int(argv[2])

        # initiation code line
        app = QApplication(argv)

        # Labels and LineEdits for a dept, coursenum, area, title
        deptLab = QLabel("Dept: ")
        deptLab.setAlignment(Qt.AlignRight)
        deptLine = QLineEdit()
        deptLine.returnPressed.connect(retrieveText)

        courseLab = QLabel("Number: ")
        courseLab.setAlignment(Qt.AlignRight)
        courseNumLine = QLineEdit()
        courseNumLine.returnPressed.connect(retrieveText)

        areaLab = QLabel("Area: ")
        areaLab.setAlignment(Qt.AlignRight)
        areaLine = QLineEdit()
        areaLine.returnPressed.connect(retrieveText)

        titleLab = QLabel("Title: ")
        titleLab.setAlignment(Qt.AlignRight)
        titleLine = QLineEdit()
        titleLine.returnPressed.connect(retrieveText)

        # list box that can scroll vertically and horizontally
        list_box = QListWidget()
        list_box.setFont(QFont("Courier", 10))

        # submit button
        submit_but = QPushButton("Submit")

        # retrieve values when submit button is clicked
        submit_but.clicked.connect(retrieveText)

        # open details when user double clicks or hits enter on a list widget item
        list_box.itemActivated.connect(retrieveDetails)

        packet = ["overviews", "", "", "", ""]

        # send the values to regserver.py
        sock = socket()
        sock.connect((host, port))
        out_flow = sock.makefile(mode='wb')
        dump(packet, out_flow)
        out_flow.flush()

        # retrieve the values from regserver.py
        in_flow = sock.makefile(mode='rb')
        db_rows = load(in_flow)

        # close connection
        sock.close()

        # user interface (prints table layout)
        # wrapper = textwrap.TextWrapper(
        #     width=72, break_long_words=False, subsequent_indent=(23 * ' '))

        # user interface: gets information from the database
        # and prints to user
        for row in db_rows:
            line_string = "{:>5}{:>4}{:>5}{:>4} {}".format(
                str(row[0]).strip(), str(row[1]).strip(), str(row[2]).strip(), str(row[3]).strip(), str(row[4]).strip())
            list_box.addItem(line_string)

        # automatically highlight first row each time
        list_box.setCurrentRow(0)

        top_layout = QGridLayout()
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setRowStretch(0, 0)
        top_layout.setRowStretch(1, 0)
        top_layout.setRowStretch(2, 0)
        top_layout.setRowStretch(3, 0)
        top_layout.setColumnStretch(0, 0)
        top_layout.setColumnStretch(1, 1)
        top_layout.setColumnStretch(2, 0)

        # labels
        top_layout.addWidget(deptLab, 0, 0)
        top_layout.addWidget(courseLab, 1, 0)
        top_layout.addWidget(areaLab, 2, 0)
        top_layout.addWidget(titleLab, 3, 0)

        # line edits
        top_layout.addWidget(deptLine, 0, 1)
        top_layout.addWidget(courseNumLine, 1, 1)
        top_layout.addWidget(areaLine, 2, 1)
        top_layout.addWidget(titleLine, 3, 1)

        # submit button
        top_layout_right = QVBoxLayout()
        top_layout_right.setSpacing(0)
        top_layout_right.setContentsMargins(0, 0, 0, 0)
        top_layout_right.addWidget(submit_but)
        top_layout_right.setAlignment(Qt.AlignCenter)
        top_layout.addLayout(top_layout_right, 0, 2, 4, 1)

        # top layout frame
        top_frame = QFrame()
        top_frame.setLayout(top_layout)

        # bottom list layout frame
        bot_layout = QGridLayout()
        bot_layout.setSpacing(0)
        bot_layout.setContentsMargins(0, 0, 0, 0)
        bot_layout.addWidget(list_box, 0, 0)
        bot_frame = QFrame()
        bot_frame.setLayout(bot_layout)

        # overarching frame layout and frame
        centralFrameLayout = QGridLayout()
        centralFrameLayout.setSpacing(0)
        centralFrameLayout.setContentsMargins(0, 0, 0, 0)
        centralFrameLayout.setRowStretch(0, 0)
        centralFrameLayout.setRowStretch(1, 1)
        centralFrameLayout.setColumnStretch(0, 1)
        centralFrameLayout.addWidget(top_frame, 0, 0)
        centralFrameLayout.addWidget(bot_frame, 1, 0)
        centralFrame = QFrame()
        centralFrame.setLayout(centralFrameLayout)

        # ---------------------------------------------------

        # outer_layout = QVBoxLayout()
        # outer_layout.setSpacing(0)
        # outer_layout.setContentsMargins(0, 0, 0, 0)

        # top_layout = QHBoxLayout()
        # top_layout.setSpacing(0)
        # top_layout.setContentsMargins(0, 0, 0, 0)
        # top_layout.setStretch(0, 0)
        # top_layout.setStretch(1, 1)
        # top_layout.setStretch(2, 0)

        # top_layout_left = QVBoxLayout()
        # top_layout_left.setAlignment(Qt.AlignRight)
        # top_layout_left.addWidget(deptLab)
        # courseLab.setAlignment(Qt.AlignRight)
        # top_layout_left.addWidget(courseLab)
        # areaLab.setAlignment(Qt.AlignRight)
        # top_layout_left.addWidget(areaLab)
        # titleLab.setAlignment(Qt.AlignRight)
        # top_layout_left.addWidget(titleLab)
        # # top_layout_left.addRow("Dept: ", deptLine)
        # # top_layout_left.addRow("Number: ", courseNumLine)
        # # top_layout_left.addRow("Area: ", areaLine)
        # # top_layout_left.addRow("Title: ", titleLine)

        # top_layout_middle = QVBoxLayout()
        # top_layout_middle.addWidget(deptLine)
        # top_layout_middle.addWidget(courseNumLine)
        # top_layout_middle.addWidget(areaLine)
        # top_layout_middle.addWidget(titleLine)

        # top_layout_right = QVBoxLayout()
        # top_layout_right.setAlignment(Qt.AlignRight)
        # top_layout_right.addWidget(submit_but)

        # top_layout.addLayout(top_layout_left)
        # top_layout.addLayout(top_layout_middle)
        # top_layout.addLayout(top_layout_right)

        # list_layout = QVBoxLayout()
        # list_layout.addWidget(list_box)

        # outer_layout.addLayout(top_layout)
        # outer_layout.addLayout(list_layout)
        # # layout.addWidget(deptLab)
        # # layout.addWidget(courseLab)
        # # layout.addWidget(areaLab)
        # # layout.addWidget(titleLab)
        # # layout.addWidget(deptLine)
        # # layout.addWidget(courseLab, 1, 0)
        # # layout.addWidget(courseNumLine, 1, 1)
        # # layout.addWidget(areaLab, 2, 0)
        # # layout.addWidget(areaLab, 2, 1)
        # # layout.addWidget(titleLab, 3, 0)
        # # layout.addWidget(titleLab, 3, 1)
        # # layout.addWidget(list_box, 4, 0)
        # # layout.addWidget(submit_but, 4, 1)

        # frame = QFrame()
        # frame.setLayout(outer_layout)

        window = QMainWindow()
        window.setWindowTitle('Princeton University Class Search')
        window.setCentralWidget(centralFrame)
        screenSize = QDesktopWidget().screenGeometry()
        window.resize(screenSize.width()//2, screenSize.height()//2)

        window.show()
        exit(app.exec_())

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
