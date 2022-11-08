import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["StudentDB"]

mycoll = mydb["students"]

# Update Attendance

def updateAttend(regNo):
    mycoll.update_one({"_id":int(regNo)},{"$set":{"Attendance":"P"} })
    # print(mycoll.find_one({"_id":int(regNo)}))

#For ADMIN

def insertRecord():
    while True:
        regNo = int(input("Enter RegNo: "))
        name = input("Enter Name: ")
        myDict = { "_id": regNo, "Name": name, "Attendance": "A" }
        x = mycoll.insert_one(myDict)
        mycoll.find().sort("_id")
        yn = input("Continue to Insert Record?(Y/N)")
        if(yn=='Y' or yn=='y'):
            continue
        else:
            break

def removeRecord():
    while True:
        regNo = int(input("Enter RegNo: "))
        myQuery = { "_id": regNo}
        x = mycoll.delete_one(myQuery)
        yn = input("Continue to Delete Record?(Y/N)")
        if(yn=='Y' or yn=='y'):
            continue
        else:
            break

#For Teacher and Admin
# print(mydb.list_collection_names())

# x=mycoll.insert_one({"_id":40731004, "Name":"Anish", "Attendance":"A"})
# for x in  mycoll.find():
#     print(x)

#insert a record and then 
# print(myClient.list_database_names())

# dblist = myClient.list_database_names()
# if "mydatabase" in dblist:
#     print("The database exists.")

def displayRecord(ch):
    
    if ch==0:          #For Admin FULL Class' Attendance
        print("\nRegNO\t\tName\n")
        x = mycoll.find({},{"Attendance":0}).sort("_id")
        for xi in x :
          print(xi)
    
    
    if ch==1:          #For TeacherFULL Class' Attendance
        print("\nRegNO\t\tName\t\t\tAttendance\n")
        x = mycoll.find().sort("_id")
        for xi in x:
            print(xi)

    if ch==2:          #For Teacher Present Class' Attendance
        print("\nRegNO\t\tName\t\t\tAttendance\n")
        x = mycoll.find({"Attendance": "P"}).sort("_id")
        for xi in x:
            print(xi)
    
    if ch==3:          #For Teacher Absent Class' Attendance
        print("\nRegNO\t\tName\t\t\tAttendance\n")
        x = mycoll.find({"Attendance": "A"}).sort("_id")
        for xi in x:
            print(xi)

if __name__ == '__main__':
    while True:
        ch1 = int(input("1.Teacher\n2.Admin\n3.Exit\nEnter your Choice: "))
        if ch1==1:
            while True: 
                ch2 = int(input("1.Full Attendance\n2.Present Students\n3.Absent Students\n4.Refresh\nEnter your Choice: "))
                if ch2==1:
                    displayRecord(ch2)
                elif ch2==2:
                    displayRecord(ch2)
                elif ch2==3:
                    displayRecord(ch2)
                elif ch2==4:
                    mycoll.update({{"Attendance": "P"}},{"$set":{"Attendance": "A"} })
                               
                else:
                    pass

                yn = input("Continue as Teacher?(Y/N)")
                if(yn=='Y' or yn=='y'):
                    continue
                else:
                    break


        elif ch1 == 2:
            while True:
                ch2 = int(input("1.Insert Record\n2.Delete Record\n3.Display Record\nEnter your Choice: "))
                if ch2==1:
                    insertRecord()
                elif ch2==2:
                    removeRecord()
                elif ch2==3:
                    displayRecord(0)
                else:
                    break

                yn = input("Continue as ADMIN?(Y/N)")
                if(yn=='Y' or yn=='y'):
                    continue
                else:
                    break

        elif ch1 == 3:
            exit(0)


        yn = input("Continue as USER?(Y/N)")
        if(yn=='Y' or yn=='y'):
            continue
        else:
            break

