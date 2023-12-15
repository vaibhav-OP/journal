import os
from datetime import date
import mysql.connector as sql
from colorama import Fore, Style

mycon = sql.connect(host="localhost", database="journal", user="root", password="123456")
cursor = mycon.cursor()

def clearConsole():
    os.system("cls")

def notifyError(text):
    clearConsole()
    print(Fore.RED + text)
    print(Style.RESET_ALL)

def notifySuccess(text):
    clearConsole()
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
        while len(title) == 0:
            title = input(Fore.RED + "Enter a valid title for today's journal\n" + Style.RESET_ALL)

        description = input("Enter the description for today's journal\n")
        while len(description) == 0:
            description = input(Fore.RED + "Enter the description for today's journal" + Style.RESET_ALL)

        cursor.execute("insert into journals(title, description, createdAt) values('{}', '{}', '{}')".format(title, description, currentDate))
        notifySuccess("Successfully added today's journal")

def viewTodaysJournal():
    currentDate = date.today()

    cursor.execute("select * from journals where createdAt = '{}'".format(currentDate))
    todayJournal = cursor.fetchone()

    if todayJournal == None:
        notifyError("You have not posted a journal today.")
    else:
        clearConsole()
        print("#{}".format(todayJournal[0]), end=" ")
        print(Fore.CYAN + "{}".format(todayJournal[1].capitalize()), end=Style.RESET_ALL + " ")
        print("({})".format(todayJournal[3]))
        print(todayJournal[2])

def updateJournal():
    currentDate = date.today()

    cursor.execute("select * from journals where createdAt = '{}'".format(currentDate))
    todayJournal = cursor.fetchone()

    if todayJournal == None:
        notifyError("You have not posted a journal today.")
    else:
        clearConsole()
        print(Fore.CYAN + "1 -", end=Style.RESET_ALL+" ")
        print(Fore.GREEN + "title", end=Style.RESET_ALL+"\n")
        print(Fore.CYAN + "2 -", end=Style.RESET_ALL+" ")
        print(Fore.GREEN + "description", end=Style.RESET_ALL+"\n")

        command = input("What you want to update? ")

        try:
            if (command == "1"):
                title = input("Enter a new title: ")
                cursor.execute("update journals set title = '{}' where createdAt = '{}'".format(title, currentDate))
            elif (command == "2"):
                description = input("Enter a new description: ")
                cursor.execute("update journals set description = '{}' where createdAt = '{}'".format(description, currentDate))
            else:
                raise ValueError("Invalid command")

            notifySuccess("Updated the journal successfully")
        except ValueError:
            notifyError("Invalid option")
        except:
            notifyError("Something went wrong")

def deleteJournal():
    currentDate = date.today()

    cursor.execute("select * from journals where createdAt = '{}'".format(currentDate))
    todayJournal = cursor.fetchone()

    if todayJournal == None:
        notifyError("You have not posted a journal today.")
    else:
        cursor.execute("delete from journals where createdAt = '{}'".format(currentDate))
        notifySuccess("Deleted todays journal successfully")

commandList = [
    {
        "ID": "1",
        "desc": "Create a journal for your day (you can only create one/day).",
        "call": createJournal,
    },
    {
        "ID": "2",
        "desc": "Displays today's journal.",
        "call": viewTodaysJournal,
    },
    {
        "ID": "3",
        "desc": "Update today's journal.",
        "call": updateJournal,
    },
    {
        "ID": "4",
        "desc": "Delete today's journal.",
        "call": deleteJournal,
    }

]

def main():
    while True:
        print("Please select a command by typing the prefixed number.")

        for command in commandList:
            print(Fore.CYAN + "{id} -".format(id=command["ID"]), end=Style.RESET_ALL+" ")
            print(Fore.GREEN + "{desc}".format(desc=command["desc"]), end=Style.RESET_ALL+"\n")
        print(Fore.CYAN + "X -", end=Style.RESET_ALL+" ")
        print(Fore.GREEN + "Exit the application.", end=Style.RESET_ALL+"\n")

        inputCommand = input("Enter what you want to do: ")
        if inputCommand.lower() == "x":
            print("Closing the applicaiton...")
            break

        for command in commandList:
            if inputCommand == command["ID"] :
                command["call"]()
                mycon.commit()
                print()
                break
        else:
            clearConsole()

clearConsole()
main()