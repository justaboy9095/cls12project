import time
import mysql.connector as con
import tabulate
import os
import matplotlib.pyplot as plt
import numpy as np

### Config for each funtion ###
# Expense tracker
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
    c=input('Are you sure you want to reset the expense tracker? (y/n): ')
    if c=='y':
        cursor.execute('drop table expenses')
        cursor.execute('CREATE TABLE IF NOT EXISTS expenses (Id int primary key auto_increment, Date varchar(255), Item varchar(255), Category varchar(255), Amount float)')
        time.sleep(1)
        print('Expense tracker reset successfully!')

# Notes
def open_notes():
    global file
    try:
        file = open("Notes.txt","r+")  
        f = file.readlines()
        return f
    except FileNotFoundError:     #Create a new file of it does not exist
        print("\n ~~~ FILE NOT FOUND ~~~")
        file = open("Notes.txt","w")
        file.close()
        print("~~~ CREATED FILE Notes.txt ~~~")
        open_notes()

def update(list):
    file.truncate(0)
    file.seek(0)
    file.write("".join(list))
    file.close()

def reset_notes():
    c=input("Are you sure you want to reset all notes? (y/n): ")
    if c.lower() == 'y':
        file = open("Notes.txt","w")
        file.close()
        print("\n ~~~ Notes reset successfully ~~~")
    else:
        print("\n ~~~ Reset canceled ~~~")

def view_notes():
    notes = open_notes()
    if len(notes) == 0:
        print("\n ~~~ No notes available ~~~")
    else:
        print("\n --- Your Notes --- \n")
        count = 1
        for note in notes:
            print("",count,"-",note)
            count += 1 

def add_note():
    notes = open_notes()
    note=input("Enter note:")
    notes.append(note + "\n")
    print("\n ~~~ Note added sucessfully ~~~")
    update(notes)

def edit_note():
    view_notes()
    notes = open_notes()
    while True:
        if len(notes) == 0:
            return
        else:
            note_index = input("\nEnter the number of the note you want to update (0 to cancel):  ")
            if note_index.isnumeric():
                note_index = (int(note_index)-1)
                if note_index < 0:
                    print("\n ~~~ Canceled ~~~")
                    return
                elif note_index>(len(notes)-1):
                    print("\n ~~~ invalid index ~~~")
                else:
                    new_note = input("\nEnter the new content for the note: ")
                    notes[note_index] = new_note + "\n"
                    update(notes)
                    print("\n ~~~ Note updated sucessfully ~~~")                    
                    return
            else:
                print("\n ~~~ Please input a numeric value ~~~ ")

def delete_note():
    view_notes()
    notes = open_notes()
    while True:
        if len(notes) == 0:
            print("\n ~~~ No notes to delete ~~~")
            return
        else:
            note_index = input("\nEnter the note number you want to delete (0 to cancel): ")
            if note_index.isnumeric():
                note_index = int(note_index) - 1
                if note_index < 0:
                    print("\n ~~~ Canceled ~~~")
                    return
                if note_index >= len(notes):
                    print("\n ~~~ Invalid index ~~~")
                else:
                    notes.pop(note_index)
                    update(notes)
                    print("\n ~~~ Deleted note successfully ~~~")
                    return
            else:
                print("\n ~~~ Please input a numeric value ~~~")

#Contact list

def setup_database_con():
    global cursor,conn
    conn = con.connect(host='localhost', user='root', password='root')

    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS contact_list')
    cursor.execute('USE contact_list')
    cursor.execute('CREATE TABLE IF NOT EXISTS contacts (Id int primary key auto_increment, Name varchar(255), Phone varchar(10), Email varchar(255))')


def phone_check():
    phone=input('Enter the phone number: ')
    if len(phone)!=10:
        print('Invalid phone number! Please enter a 10 digit number.')
        phone_check()
    else:
        return phone

def get_data_con():
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return data

def show_contacts():
    data=get_data_con()
    table=tabulate.tabulate(data, headers=['Id', 'Name', 'Phone', "Email"], tablefmt='rounded_grid')
    print(table)

def add_contact():
    name=input("Enter the name: ")
    phone=phone_check()
    email=input("Enter the email: ")
    cursor.execute(f'INSERT INTO contacts (name, phone, email) VALUES ("{name}",{phone},"{email}")')
    print(f'Contact data: {name}, {phone}, {email}')
    print('Adding contact details...')
    time.sleep(2)
    print('Contact added successfully!')


def edit_contact():
    show_contacts()
    d=int(input('Select the Contact Id to delete (0 to cancel): '))
    if d==0:
        print('Canceled')
        return
    name=input('Enter the name: ')
    phone=phone_check()
    email=input('Enter email: ')
    cursor.execute(f"UPDATE contacts set Name='{name}', phone={phone}, email='{email}' where id={d}")
    print(f'Updated data: {name}, {phone},{email}')
    print('Updating contact list...')
    time.sleep(2)
    print('Contacts updated successfully!')

def search_contact():
    d=get_data_con()
    s=input('Enter the keyword to search: ')
    res=[]
    print('Searching...')
    time.sleep(1)
    for i in d:
        if s in i[1]:
            res.append(i)
    if len(res)==0:
        print('No contacts found!')
    else:
        print(f'Results containing {s}')
        table=tabulate.tabulate(res, headers=['Id', 'Name', 'Phone', "Email"], tablefmt='rounded_grid')
        print(table)

def reset_con():
    c=input('Are you sure you want to reset the contact list? (y/n): ')
    if c=='y':
        cursor.execute('drop table contacts')
        cursor.execute('CREATE TABLE contacts (Id int primary key auto_increment, Name varchar(255), Phone varchar(10), Email varchar(255))')
        time.sleep(1)
        print('Contact list reset successfully!')

def delete_contact():
    show_contacts()
    d=int(input('Select the contact id to delete (0 to cancel): '))
    if d==0:
        print('Canceled')
        return
    cursor.execute(f'delete from contacts where Id ={d}')
    dat=get_data_con()
    cursor.execute('drop table contacts')
    cursor.execute('CREATE TABLE IF NOT EXISTS contacts (Id int primary key auto_increment, Name varchar(255), Phone varchar(10), Email varchar(255))')
    for i in dat:
        name=i[1]
        phone=i[2]
        email=i[3]
        cursor.execute(f'INSERT INTO contacts (name, phone, email) VALUES ("{name}",{phone},"{email}")')
    print(f'Contact Id({d}) deleted successfully!')


#General

def redirect():
    input('Press Enter > ')
    print('\nReturning to menu...\n')
    time.sleep(1)
    os.system('cls')

def start_fn(fn):
    os.system('cls')
    print(f'Starting {fn}...')
    time.sleep(1)
    os.system('cls')

def exit_fn(fn):
    os.system('cls')
    print(f'Exiting {fn}...')
    time.sleep(1)
    os.system('cls')

    
###############################


def todo_list():
    pass

def Notes():
    notes=open_notes()
    while True:
        print("\n --- Notes --- \n\n 1 - Add Note\n 2 - View Notes\n 3 - Edit Note\n 4 - Delete Note\n 5 - Reset Notes\n 6 - Exit")
        choice = input(" Enter your choice (1-6): ")
        if choice.isnumeric():
            choice = int(choice)
            if choice == 1:
                add_note()
            elif choice == 2:
                view_notes()
            elif choice == 3:
                edit_note()
            elif choice == 4:
                delete_note()
            elif choice == 5:
                reset_notes()
            elif choice == 6:
                return
            else:
                print("\n ~~~ Please select a valid option (1-5) ~~~")
        else:
            print("\n ~~~ Please input a numeric value ~~~ ")
        redirect()

def expense_trac():
    categories=['Food','Transport','Entertainment','Health','Education','Miscellaneous']
    func=['Show Expenses','Add Expense','Delete Expense','Edit Expense','Add/Edit Categories','Show Visualisation','Reset Entries' ,'Exit']
    flag=True
    
    setup_database()
    setup_cat_file()

    while flag:
        print('---Expense Tracker---\n')
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
            reset()
        elif choice==8:
            flag=False
        else:
            print('Invalid choice! Select between 1-8')
            time.sleep(1)
            os.system('cls')
            continue
        if choice !=8:
            conn.commit()
            redirect()

def Contacts():
    fn=['Show Contacts', 'Search by Name', 'Add a contact', 'Edit a contact', 'Delete a contact', 'Reset data', 'Exit']
    flag=True
    setup_database_con()
    while flag:
        print('---Contact List---')
        for i in range(len(fn)):
            print(f'{i+1}- {fn[i]}')
        try:
            ch=int(input('Enter choice: '))
        except ValueError:
            print('Invalid choice! Please enter the number beside the function.')
            continue
        if ch==1:
            show_contacts()
            redirect()
            conn.commit()
        elif ch==2:
            search_contact()
            redirect()
            conn.commit()
        elif ch==3:
            add_contact()
            redirect()
            conn.commit()
        elif ch==4:
            edit_contact()
            redirect()
            conn.commit()
        elif ch==5:
            delete_contact()
            redirect()
            conn.commit()
        elif ch==6:
            reset_con()
            redirect()
            conn.commit()
        elif ch==7:
            flag=False
        else:
            print('Invalid choice! Select between 1-7')

menu = ['To-Do List','Notes','Expense Tracker','Contacts', 'Exit']

while True:
    print('--- Personal Assistant ---')
    for i in range(len(menu)):
        print(f"{i+1}: {menu[i]}")
    try:
        ch=int(input('Select function: '))
    except ValueError:
        print('Invalid choice! Please enter the number beside the function.')
        time.sleep(2)
        os.system('cls')
        continue
    if ch != 5:
        start_fn(menu[ch-1])
    if ch == 1:
        todo_list()
    elif ch == 2:
        Notes()
    elif ch == 3:
        expense_trac()
    elif ch == 4:
        Contacts()
    elif ch == 5:
        print('Exiting...')
        break
    else:
        print("Invalid option, please try again.")
        time.sleep(1)
        os.system('cls')
    
    if ch != 5:
        exit_fn(menu[ch-1])

    
