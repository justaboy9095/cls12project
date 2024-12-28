import time
import mysql.connector as con
import tabulate
import os
import matplotlib.pyplot as plt
import numpy as np


categories=['Food','Transport','Entertainment','Health','Education','Miscellaneous']
func=['Show Expenses','Add Expense','Delete Expense','Edit Expense','Add/Edit Categories','Show Visualisation','Reset Entries' ,'Exit']
flag=True

def setup_database():
    global cursor,conn
    conn = con.connect(host='localhost', user='root', password='root')

    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS expense_tracker')
    cursor.execute('USE expense_tracker')
    cursor.execute('CREATE TABLE IF NOT EXISTS expenses (Id int primary key auto_increment, Date varchar(255), Item varchar(255), Category varchar(255), Amount float)')

def setup_cat_file():
    global f,categories
    try:
        f=open('cat.txt', 'r')
        file_size=os.path.getsize('cat.txt')
        dat=f.read()
        if file_size==0:
            raise FileNotFoundError
        else:
            categories=eval(dat)
    except FileNotFoundError:
        f=open('cat.txt', 'w')
        f.write(f'{categories}')
    
    f.close()


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
    show_expenses()
    d=int(input('Select the expense no to delete (0 to cancel): '))
    if d==0:
        print('Canceled')
        return
    date=input('Enter date of purchase (DD/MM/YY): ')
    itsr=input('Enter item/service bought: ')
    print('Select Category: ')
    for i in range(len(categories)):
        print(f'{i+1}- {categories[i]}')
    cat=int(input('Enter category number (No beside the category): '))
    cat=categories[cat-1]
    amt=float(input('Enter amount spent: '))
    cursor.execute(f"UPDATE expenses set Date='{date}', Item='{itsr}', Category='{cat}', amount='{amt}' where id={d}")
    print(f'Updated data: {date}, {itsr}, {cat}, {amt}')
    print('Updating expenses...')
    time.sleep(2)
    print('Expense updated successfully!')
    

def edit_categories():
    f=open('cat.txt', 'w')
    print('Editor options: ')
    print('1- Add Category')
    print('2- Edit Category')
    print('3- Delete Category')
    choice=int(input('Select a function: '))
    if choice==1:
        cat=input('Enter new category name: ')
        categories.append(cat)
        f.write(f'{categories}')
        print('Adding category...')
        time.sleep(1)
        print('Category added successfully!')
    elif choice==2:
        print('Select category to edit: ')
        for i in range(len(categories)):
            print(f'{i+1}- {categories[i]}')
        c=int(input('Select category number (No beside the category): '))
        new_cat=input('Enter new category name: ')
        categories[categories.index(categories[c-1])]=new_cat
        f.write(f'{categories}')
        print('Editing category...')
        time.sleep(1)
        print('Category edited successfully!')
    elif choice==3:
        print('Select category to delete: ')
        for i in range(len(categories)):
            print(f'{i+1}- {categories[i]}')
        c=int(input('Select category number (No beside the category): '))
        categories.remove(categories[c-1])
        f.write(f'{categories}')
        print('Deleting category...')
        time.sleep(1)
        print('Category deleted successfully!')
    f.close()

def show_vis():
    print('Visualization types:')
    print('1- Pie Chart')
    print('2- Line graph')
    choice=int(input('Select a visualization: '))
    if choice==1:
        cursor.execute('select category,sum(amount) from expenses group by category;')
        data = cursor.fetchall()
        labels=[]
        values=[]
        for i in data:
            labels.append(i[0])
            values.append(i[1])

        d=sum(values)
        for i in range(len(values)):
            values[i]=(values[i]/d)*100

        explode=[]

        for i in values:
            if i==max(values):
                explode.append(0.05)
            else:
                explode.append(0)

        y = np.array(values)
        plt.pie(y, labels=labels, explode=explode)
        plt.title('Expenditure By Category')
        plt.show()
    elif choice==2:
        cursor.execute('select date,sum(amount) from expenses group by date;')
        data = cursor.fetchall()
        label=[]
        x=[]
        y=[]
        for i in range(len(data)):
            x.append(i+1)

        for i in data:
            label.append(i[0])
            y.append(i[1])
        y=np.array(y)
        plt.plot(x,y)
        plt.xlabel('Date')
        plt.ylabel("Amount spent")
        plt.title('Expenditure by date')
        plt.xticks(x,label)
        plt.show()


def reset():
    cursor.execute('drop table expenses')
    cursor.execute('CREATE TABLE IF NOT EXISTS expenses (Id int primary key auto_increment, Date varchar(255), Item varchar(255), Category varchar(255), Amount float)')

def redirect():
    conn.commit()
    input('Press Enter to return to menu > ')
    print('\nReturning to menu...\n')
    time.sleep(1)
    os.system('cls')
    
    

setup_database()
setup_cat_file()

while flag:
    print('---Expense Tracker---')
    print('Select a function: ')
    for i in range(len(func)):
        print(f'{i+1}- {func[i]}')
    try:
        choice=int(input('Select function: '))
    except ValueError:
        print('Invalid choice! Please enter the number beside the function.')
        time.sleep(2)
        os.system('cls')
        continue
    if choice==1:
        show_expenses()
        redirect()
    elif choice==2:
        add_expense()
        redirect()
    elif choice==3:
        delete_expense()
        redirect()
    elif choice==4:
        edit_expense()
        redirect()
    elif choice==5:
        edit_categories()
        redirect()
    elif choice==6:
        show_vis()
        redirect()
    elif choice==7:
        reset()
        redirect()
    elif choice==8:
        flag=False
    else:
        print('Invalid choice! Select between 1-8')
        time.sleep(1)
        os.system('cls')
        continue


