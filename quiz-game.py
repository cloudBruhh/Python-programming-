print("Welcome to the Quiz Game!")
score = 0
playing = input("Do you want to play? (yes/no): ")

if playing.lower() != "yes":
    print("Maybe next time. Goodbye!")
    exit()

print("Great! Let's get started.")

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is Central Processing Unit.")

answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is Random Access Memory.")

answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is Graphics Processing Unit.")

print("Thanks for playing! Your final score is: " + str(score))
