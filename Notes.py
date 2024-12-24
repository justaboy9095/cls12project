#Note Taking App

def add_note():
    note=input("Enter note:")
    notes.append(note)
    print("\n ~~~ Note added sucessfully ~~~")
    
def view_notes():
    if len(notes)==0:
        print("\n ~~~ No notes available ~~~")
    else:
        print("\n --- Your Notes --- \n")
        count=1
        for note in notes:
            print("",count,"-",note)
            count+=1
            
def edit_note():
    view_notes()
    if len(notes)==0:
        return
    else:
        note_index=int(input("\nEnter the number of the note you want to update:  ")) - 1
        if note_index<0 or note_index>(len(notes)-1):
            print("\n ~~~ invalid index ~~~")
        else:
            new_note=input("\nEnter the new content for the note: ")
            notes[note_index] = new_note
            print("\n ~~~ Note updated sucessfully ~~~")
        
def delete_note():
    view_notes()
    if len(notes)==0:
        return
    else:
        note_index=int(input("\nEnter note number you want to delete: ")) - 1
        if note_index<0 or note_index>(len(notes)-1):
            print("\n ~~~ invalid index ~~~")
        else:
            removed_note=notes.pop(note_index)
            print("\n ~~~ deleted note:",removed_note,"sucessfully ~~~")
    
def Notes():
    while True:
        print("\n\n\n\n\n --- Notes --- \n\n 1 - Add Note\n 2 - View Notes\n 3 - Edit Note\n 4 - Delete Note\n 5 - Exit\n")
        choice=input("Enter your choice (1-5): ")
        if choice.isnumeric():
            choice=int(choice)
            if choice==1:
                add_note()
            elif choice==2:
                view_notes()
            elif choice==3:
                edit_note()
            elif choice==4:
                delete_note()
            elif choice==5:
                print("Exiting Notes...")
                break
            else:
                print("\n ~~~ Please select a valid option (1-5) ~~~")
        else:
            print("\n ~~~ Please input a numeric value ~~~ ")

notes=[]        
Notes()