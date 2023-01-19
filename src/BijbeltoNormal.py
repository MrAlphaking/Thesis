from Levenshtein import distance as levenshtein_distance
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def printString(pre, text):
    if not (text == "\n" or text == " \n"):
        print(f"{pre}: {text}")

oldList = []
modernList = []
oldcounter = 0
list1 = []
list2 = []
with open('../data/Basisbijbel - kopie') as modern:
    with open('../data/Statenvertaling - 1637 - kopie') as old:
        modern = modern.readlines()
        old = old.readlines()
        # lines = lines.split("\n\n")
        # print(old)
        # print(modern)

        print(len(modern))
        print(len(old))
        maxcount = 0
        nprevious = "\n"


        for index, modern_line in enumerate(modern[:12000]):
            if index >= len(old):
                print("Out of range")
                break
            # if modern_line[:1].isnumeric():
            #     modern_line = modern_line.replace("\n", "")
            #     modern_line = modern_line.split(": ", maxsplit=1)
            #     if len(modern_line) < 2:
            #         print(modern_line)
            #         continue
            #     if "-" in modern_line[0]:
            #         number = modern_line[0].split("-")
            #         old_string = old[oldcounter]
            #         for i in range(int(number[1]) - int(number[0])):
            #             old_string += ' ' + old[oldcounter + 1 + i]
            #         oldcounter += int(number[1]) - int(number[0]) + 1
            #     else:
            #         old_string = old[oldcounter]
            #         oldcounter += 1
            #
            #     oldList.append(old_string.replace("\n", ""))
            #     modernList.append(modern_line[1].replace("\n", ""))
            # if len(modern_line) > 24 and modern_line != "\n":
            if modern_line != "\n":
                if (modern_line[:1].isnumeric() and modern_line[1:2] == ":") or modern_line[:2].isnumeric() or "-" in modern_line:
                    # print(modern_line)
                    modern_line = modern_line.replace("\n", "")
                    modern_line = modern_line.split(": ", maxsplit=1)
                    if "-" in modern_line[0]:
                        number = modern_line[0].split("-")
                        old_string = old[oldcounter]
                        for i in range(int(number[1]) - int(number[0])):
                            old_string += ' ' + old[oldcounter + 1 + i]
                        oldcounter += int(number[1]) - int(number[0]) + 1
                    else:
                        old_string = old[oldcounter]
                        oldcounter += 1

                    oldList.append(old_string.replace("\n", ""))
                    modernList.append(modern_line[1].replace("\n", ""))

                    if index % 100 == 0:
                        print(f"{index}\nOLD: {oldList[len(oldList) - 1]}\nNEW: {modernList[len(modernList) - 1]}\n\n\n")
                else:
                    printString("Else", modern_line)
            else:
                printString("empty", modern_line)


# print(oldList)
# print(modernList)

# print(list1)

# for i in range(len(list1)):
#     score = similar(list1[i], list2[i])
#     print(score)
#     print(f"{list1[i]}: {list2[i]}")

# print(len(oldList))
# print(len(modernList))

with open('../data/Basisbijbel_cleaned', 'w') as fp:
    for item in modernList:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
with open('../data/Statenvertaling - 1637_cleaned', 'w') as fp:
    for item in oldList:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')

                # print(modern_line)