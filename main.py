from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
currentCard = {}
toLearn = {}

# ---------------------------- PREPARE FILE ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")  # Prepare French words data frame
except FileNotFoundError:
    originalData = pandas.read_csv("data/french_words.csv")  # Prepare French words data frame
    toLearn = originalData.to_dict(orient="records")
else:
    toLearn = data.to_dict(orient="records")  # Turn dataframe to list of dictionaries {'French': 'partie', 'English': 'part'}


# ---------------------------- FUNCTIONS ------------------------------- #
def nextCard():
    global currentCard, flipTimer
    window.after_cancel(flipTimer)  # When a button is clicked, invalidate the timer
    currentCard = random.choice(toLearn)  # Choose a random French-English word pair
    # Show the French word side of the card
    canvas.itemconfig(cardTitle, text="French", fill="black")  # Present the language
    canvas.itemconfig(cardWord, text=currentCard["French"], fill="black")  # Present the word in the language
    canvas.itemconfig(cardBackground, image=cardFrontImg)
    flipTimer = window.after(3000, func=flipCard)  # After card setup, set up a new timer


def flipCard():
    # Show the English word on the other side of the card
    canvas.itemconfig(cardTitle, text="English", fill="white")
    canvas.itemconfig(cardWord, text=currentCard["English"], fill="white")
    canvas.itemconfig(cardBackground, image=cardBackImg)


def isKnown():
    toLearn.remove(currentCard)  # Remove a French-English word pair the user already knows
    data = pandas.DataFrame(toLearn)
    data.to_csv("data/words_to_learn.csv", index=False)  # Save the modified data with no index numbers
    nextCard()  # Show the next card


# ---------------------------- UI SETUP ------------------------------- #
# Setting up the main window
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flipTimer = window.after(3000, func=flipCard)

canvas = Canvas(width=800, height=526)

# Prepare the flash card
cardFrontImg = PhotoImage(file="images/card_front.png")
cardBackImg = PhotoImage(file="images/card_back.png")
cardBackground = canvas.create_image(400, 263, image=cardFrontImg)

# Prepare the texts on the flash card
cardTitle = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
cardWord = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# The Red X Button
crossImage = PhotoImage(file="images/wrong.png")
redXButton = Button(image=crossImage, highlightthickness=0, command=nextCard)
redXButton.grid(row=1, column=0)

# The Green Check Mark Button
checkImage = PhotoImage(file="images/right.png")
greenCheckButton = Button(image=checkImage, highlightthickness=0, command=isKnown)
greenCheckButton.grid(row=1, column=1)

nextCard()  # Show a French word card right from the get go

window.mainloop()
