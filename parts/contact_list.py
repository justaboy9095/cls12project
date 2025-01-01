import time
import mysql.connector as con
import os
import tabulate

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


def redirect():
    input('Press Enter > ')
    print('\nReturning to menu...\n')
    time.sleep(1)
    os.system('cls')

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
