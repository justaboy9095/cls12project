import mysql.connector as msc
import time
import matplotlib.pyplot as plt

def timer():
    pass

def stopwatch():
    pass

def calculator():
    pass

def alarm_clock():
    pass

def todo_list():
    pass

def Notes():
    pass

def expense_trac():
    pass

def quote_gen():
    pass

def Contacts():
    pass

def redirect():
    print('Redirecting to menu...')
    time.sleep(2)

menu = {
    '1': 'Timer',
    '2': 'Stopwatch',
    '3': 'Calculator',
    '4': 'Alarm Clock',
    '5': 'To-Do List',
    '6': 'Notes',
    '7': 'Expense Tracker',
    '8': 'Get a Quote',
    '9': 'Contacts'
}

while True:
    for key, value in sorted(menu.items()):
        print(f"{key}: {value}")
    ch = input("Select an option: ")

    if ch == '1':
        timer()
    elif ch == '2':
        stopwatch()
    elif ch == '3':
        calculator()
    elif ch == '4':
        alarm_clock()
    elif ch == '5':
        todo_list()
    elif ch == '6':
        Notes()
    elif ch == '7':
        expense_trac()
    elif ch == '8':
        quote_gen()
    elif ch == '9':
        Contacts()
    else:
        print("Invalid option, please try again.")