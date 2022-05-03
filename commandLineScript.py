import csv
import re

#Looks for (in file, words to look for, inside title/description/author)
def lookFor(file, look_for, inside):

    with open(file, 'r', encoding='utf-8') as f:
        csvreader = csv.reader(f, delimiter=',')

        if inside == 'title':
            inside = 0

        elif inside == 'description' or inside == 'descr' or inside == 'desc':
            inside = 3

        elif inside == 'author' or inside == 'channel' or inside == 'uploader':
            inside = 4

        for row in csvreader:
            if re.search(look_for, row[inside], re.IGNORECASE):
                print(row[0] + " |--> " + row[1] + f" [AUTHOR: {row[4]}]")

#Constant loop to find what you're looking for; exit to end it
while True:

    response = input("Searching for term(s): ")
    what_to_look_in = input("What to look into? (title/description/author): ")

    if what_to_look_in == "title":
        inside = "title"

    elif what_to_look_in == "description":
        inside = "descr"

    elif what_to_look_in == "author":
        inside = "author"

    else:
        inside = "title"

    lookFor('mock_my_liked_videos.csv', look_for=response, inside=inside)