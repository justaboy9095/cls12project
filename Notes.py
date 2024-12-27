#Note Taking App

#ADD NEW NOTE
def add_note():
    notes = open_notes()
    note=input("Enter note:")
    notes.append(note + "\n")
    print("\n ~~~ Note added sucessfully ~~~")
    update(notes)
    
#VIEW NOTES
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
                      
#EDIT NOTE
def edit_note():
    view_notes()
    notes = open_notes()
    while True:
        if len(notes) == 0:
            return
        else:
            note_index = input("\nEnter the number of the note you want to update:  ")
            if note_index.isnumeric():
                note_index = (int(note_index)-1)
                if note_index < 0 or note_index>(len(notes)-1):
                    print("\n ~~~ invalid index ~~~")
                else:
                    new_note = input("\nEnter the new content for the note: ")
                    notes[note_index] = new_note + "\n"
                    update(notes)
                    print("\n ~~~ Note updated sucessfully ~~~")                    
                    return
            else:
                print("\n ~~~ Please input a numeric value ~~~ ")
  
#DELETE NOTE              
def delete_note():
    view_notes()
    notes = open_notes()
    while True:
        if len(notes) == 0:
            print("\n ~~~ No notes to delete ~~~")
            return
        else:
            note_index = input("\nEnter the note number you want to delete: ")
            if note_index.isnumeric():
                note_index = int(note_index) - 1
                if note_index < 0 or note_index >= len(notes):
                    print("\n ~~~ Invalid index ~~~")
                else:
                    notes.pop(note_index)
                    update(notes)
                    print("\n ~~~ Deleted note successfully ~~~")
                    return
            else:
                print("\n ~~~ Please input a numeric value ~~~")
         
#MAIN MENU   
def Notes():
    notes=open_notes()
    while True:
        print("\n\n\n\n\n --- Notes --- \n\n 1 - Add Note\n 2 - View Notes\n 3 - Edit Note\n 4 - Delete Note\n 5 - Exit\n")
        choice = input(" Enter your choice (1-5): ")
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
                print(" Exiting Notes...")
                break
            else:
                print("\n ~~~ Please select a valid option (1-5) ~~~")
        else:
            print("\n ~~~ Please input a numeric value ~~~ ")

#OPEN Notes.txt
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

#UPDATE Notes.txt       
def update(list):
    file.truncate(0)
    file.seek(0)
    file.write("".join(list))
    file.flush()
            
Notes()