1️) Install Required Software

Make sure you have the following installed on your system:

-Python 3.10+
-MySQL Server & MySQL Workbench
-Python Libraries:
1) customtkinter
2) datetime
3) csv
4) msq.connector
5) tkinter
6) os

 2) MySQL Setup

Open MySQL Workbench or the MySQL Command Line.
Log in to MySQL using your credentials (e.g. username root and your password).
Run this command to create the database:

CREATE DATABASE company;

Make sure your MySQL server is running before launching the program.

3) Update MySQL Credentials (if needed)
In your billing.py file, change this line if your MySQL password or user is different:
mycon = mys.connect(host="localhost", user="root", passwd="1234", database="company")


 Replace "1234" with your own MySQL password.

4) Run the Program

Run:
python maingui.py
The main GUI will appear 
