import time
import mysql.connector as con
import tabulate
import os


categories=['Food','Transport','Entertainment','Health','Education','Miscellaneous']
func=['Show Expenses','Add Expense','Delete Expense','Edit Expense','Edit Categories','Show Visualisation','Set Budget','Edit Budget','Exit']
flag=True

def setup_database():
    global cursor,conn
    conn = con.connect(host='localhost', user='root', password='root')

    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS expense_tracker')
    cursor.execute('USE expense_tracker')
    cursor.execute('CREATE TABLE IF NOT EXISTS expenses (Id int primary key auto_increment, Date varchar(255), Item varchar(255), Category varchar(255), Amount float)')

def get_data():
    cursor.execute('SELECT * FROM expenses')
    data = cursor.fetchall()
    return data

def show_expenses():
    t=get_data()
    table=tabulate.tabulate(t, headers=['No', 'Date of purchase', 'Purpose','Category','Amount Spent'], tablefmt='rounded_grid')
    print(table)

def add_expense():
    date=input('Enter date of purchase (DD/MM/YY): ')
    itsr=input('Enter item/service bought: ')
    print('Select Category: ')
    for i in range(len(categories)):
        print(f'{i+1}- {categories[i]}')
    cat=int(input('Enter category number (No beside the category): '))
    cat=categories[cat-1]
    amt=float(input('Enter amount spent: '))
    cursor.execute(f'INSERT INTO expenses (Date, Item, Category, Amount) VALUES ("{date}","{itsr}","{cat}",{amt})')
    print(f'Expense data: {date}, {itsr}, {cat}, {amt}')
    print('Adding expense...')
    time.sleep(2)
    print('Expense added successfully!')

def delete_expense():
    show_expenses()
    d=int(input('Select the expense no to delete (0 to cancel): '))
    if d==0:
        print('Canceled')
        return
    cursor.execute(f'delete from expenses where Id ={d}')
    dat=get_data()
    cursor.execute('drop table expenses')
    cursor.execute('CREATE TABLE IF NOT EXISTS expenses (Id int primary key auto_increment, Date varchar(255), Item varchar(255), Category varchar(255), Amount float)')
    for i in dat:
        date=i[1]
        itsr=i[2]
        cat=i[3]
        amt=i[4]
        cursor.execute(f'INSERT INTO expenses (Date, Item, Category, Amount) VALUES ("{date}","{itsr}","{cat}",{amt})')
    print('Expense deleted successfully!')

def edit_expense():
    pass

def edit_categories():
    pass

def show_vis():
    pass

def set_budget():
    pass

def edit_budget():
    pass

def redirect():
    conn.commit()
    input('Press Enter to return to menu > ')
    print('\nReturning to menu...\n')
    time.sleep(1)
    os.system('cls')
    
    

setup_database()

while flag:
    print('---Expense Tracker---')
    print('Select a function: ')
    for i in range(len(func)):
        print(f'{i+1}- {func[i]}')
    try:
        choice=int(input('Select function (Enter the no beside the function): '))
    except ValueError:
        print('Invalid choice! Please try again.')
        time.sleep(1)
        os.system('cls')
        continue
    if choice==1:
        show_expenses()
    elif choice==2:
        add_expense()
    elif choice==3:
        delete_expense()
    elif choice==4:
        edit_expense()
    elif choice==5:
        edit_categories()
    elif choice==6:
        show_vis()
    elif choice==7:
        set_budget()
    elif choice==8:
        edit_budget()
    elif choice==9:
        flag=False
    else:
        print('Invalid choice! Please try again.')
    redirect()

