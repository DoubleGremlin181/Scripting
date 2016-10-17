from random import randint

num = randint(1,100)
c = 1
n = int(raw_input("Guess the number between 1 and 100\n> "))
while n!= num:
    if(n>num):
        n = int(raw_input("Too high! Try again\n> "))
        c+=1
    elif(n<num):
        n = int(raw_input("Too low! Try again \n> "))
        c+=1

print "Congratulations!!\nYou win\nYou took " + str(c) + " tries"
