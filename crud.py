students = [
    {
        "fname" : "Nikos",
        "lname" : "Mitro",
        "fathersname" : "Kostas",
        "age" : 10,
        "class" : 4,
        "id" : 1001
    },
    {
        "fname" : "Xristina",
        "lname" : "Saroglou",
        "fathersname" : "Greg",
        "age" : 11,
        "class" : 5,
        "id" : 1002
    },
    {
        "fname": "Greg",
        "lname": "Masloumidis",
        "fathersname": "Pantelis",
        "age": 12,
        "class": 6,
        "id": 1003
    }
]
max_id = 0
found_student = False # flag to indicate if the student was found

def search_by_last_name(last_name):
    last_names = [student for student in students if student['lname'] == last_name]
    return last_names

def search_by_id(id):
    ids = [student for student in students if student['id'] == id]
    return ids

def update_by_id(id):
    for student in students:
        if student['id'] == id :
            id_age = input("Update Age : ")
            id_class = input("Update Class : ")

            student['age'] = id_age
            student['class'] = id_class

def print_student_details():
    for student in students:
        print(f"{student['fname']} {student['fathersname'][0]}. {student['lname']}")


def print_student_name_from_id():
    found = False
    student_name_id = input("Please provide a student id : ").strip()

    for student in students:
        if int(student_name_id) == student['id']:
            found = True
            print(f"Student id exists : {student['fname']}\n")

    if not found:
        print("Student id does not exists")

def create_record():

    name = input("Give Student's First name : ")
    while not name.isalpha():
        name = input("Give a legit First name : ")
    last_name = input("Give Student's Last Name : ")
    while not last_name.isalpha():
        last_name = input("Give A legit Last Name : ")
    father_name = input("Give Student's Fathers name : ")
    while not father_name.isalpha():
        father_name = input("Give A legit Father's name : ")

    stop = False
    for student in students:
        if name == student['fname'] and last_name == student['lname'] and father_name == student['fathersname']:
            print('Student Allready Exists')
            ch = input("Do you want to Continue? [y/n] : ")
            if ch == 'n':
                stop = True
                break  # break from the inner for
    if stop:
        stop = True

    age = input("Give Student's Age : ")
    while age.isalpha():
        age = input("Numbers Please. Give Student's Age : ")
    student_class = input("Give Student's Class : ")
    while student_class.isalpha():
        student_class = input("Numbers please. Give Student's Age : ")

    details = {
        'fname': name,
        'lname': last_name,
        'fathersname': father_name,
        'age': age,
        'class': student_class,
        'id': max_id + 1
    }
    students.append(details)
    print('Student List has been Updated')
    print(f'{students}\n')


def main():
    global max_id
    while True:

        for student in students:
            if student['id'] > max_id:
                max_id = student['id'] #find the max id and update it if needed
        print()
        print("*" * 25)
        print('Please choose from the Below Options :\n'
              '1. Create a Record\n'
              '2. Print a Record\n'
              '3. Update a Record\n'
              '4. Delete a Record\n'
              '5. Quit')
        print("*" * 25 + '\n')
        choise = int(input('Please Choose : '))

        if choise == 1:
            create_record()

        elif choise == 2:
            print("Please choose from the Below Options :\n"
                               "1. Print a Student\n"
                               "2. Print all Students\n"
                               "3. Print Students names\n")
            sub_choise = input("Please Choose : ")
            while sub_choise not in ["1", "2", "3"]:
                sub_choise = input("Please Choose [1-3]: ")

            if sub_choise == "1":
                print_student_name_from_id()

            elif sub_choise == "2":
                print("Student details are : ")
                for student in students:
                    print(student)
                print()

            elif sub_choise == "3":
                print("Student names are : ")
                print_student_details()
                print("\n")

        elif choise == 3:
            print("Please Choose From the below Options : \n"
                  "1. Search by Student's Last name\n"
                  "2. Search by Student's ID")
            ch = input("Please Choose : ")
            while ch not in ["1","2"] :
                ch = input("Please Choose {1,2] : ")

            if ch == '1':
                name_ch = input("Please Provide Student's Last Name : ")
                name_ch = search_by_last_name(name_ch)
                if len(name_ch) == 0 :
                    print('No Records')
                elif len(name_ch) == 1 :
                    print(name_ch)
                elif len(name_ch) >= 2 :
                    for student in name_ch:
                        print(student)
                    print('---------------------')
                    print('Update Student By ID')
                    name_id = input("Provide ID : ")
                    while name_id.isalpha():
                        name_id = input("No letters Please. Provide ID :")
                    name_id = int(name_id)
                    update_by_id(name_id)

            elif ch == "2":
                id_ch = input("Please Provide Student's ID : ")
                while id_ch.isalpha():
                    id_ch = input("No letters Please. Please Provide Student's ID : ")
                id_ch = int(id_ch)
                id_results = search_by_id(id_ch)
                if len(id_results) == 0:
                    print('No Records')
                else :
                    print(f"Student Details Are : {id_results}\n"
                          f"Update Records")
                    update_by_id(id_ch)

        elif choise == 4:
            ...

        elif choise == 5:
            print('Bye Bye')
            break

    print(f"Student list are {students}")


main()
