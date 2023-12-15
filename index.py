import os
from datetime import date
import mysql.connector as sql
from colorama import Fore, Style

mycon = sql.connect(host="localhost", database="journal", user="root", password="123456")
cursor = mycon.cursor()

def notifyError(text):
    os.system("cls")
    print(Fore.RED + text)
    print(Style.RESET_ALL)

def notifySuccess(text):
    os.system("cls")
    print(Fore.GREEN + text)
    print(Style.RESET_ALL)

def createJournal():
    currentDate = date.today()

    cursor.execute("select * from journals where createdAt = '{}'".format(currentDate))
    todayJournal = cursor.fetchone()

    if todayJournal:
        notifyError("You already have posted a journal today.")
    else:
        title = input("Enter the title for today's journal\n")
        description = input("Enter the description for today's journal\n")

        cursor.execute("insert into journals(title, description, createdAt) values('{}', '{}', '{}')".format(title, description, currentDate))
        notifySuccess()

commandList = [
    {
        "ID": "1",
        "desc": "Create a journal for your day (you can only create one/day)",
        "call": createJournal,
    }

]

def main():
    print("Hey, How's your days?")

    while True:
        print("Please select a command by typing the prefixed number.")

        for command in commandList:
            print("{id} - {desc}".format(id=command["ID"], desc=command["desc"]))
        inputCommand = input("Enter what you want to do: ")

        for command in commandList:
            if inputCommand == command["ID"] :
                command["call"]()
                break

main()