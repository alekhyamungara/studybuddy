from pywebio.input import input, input_group, PASSWORD
from pywebio.output import put_text, put_success, put_error, put_buttons, clear
import hashlib
import json
import os  # added to check file existence
from pywebio.input import input, select
from pywebio.output import put_text, put_markdown
import random

from pywebio.session import run_js, go_app


habitlist = None

# Simulated database (in-memory)
users = {}

# Load existing users from login_data.json if it exists
if os.path.exists("login_data.json"):
    with open("login_data.json", "r") as f:
        users = json.load(f)

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Home page
def home_page():
    clear()
    put_text("Home Page")
    put_buttons(["Go to Sign Up Page"], onclick=[sign_up])
    put_buttons(["Go to Sign In Page"], onclick=[sign_in])

def go_to_home_page():
    go_app('home_page', False)

# Sign Up Page
def sign_up():
    clear()
    put_text("Sign Up Page")
    put_buttons(["Go to Home Page"], onclick=[go_to_home_page])

    # Gather username and password
    username = input("Choose a username:")
    password = input("Choose a password:", type=PASSWORD)
    confirm_password = input("Confirm your password:", type=PASSWORD)
      
    # Check if the username already exists
    if username in users:
        put_error("Username is already taken! Please choose a different username.")
        return

    # Check if passwords match
    if password != confirm_password:
        put_error("Passwords do not match! Please try again.")
        return

    # Hash the password and save the new user
    hashed_password = hash_password(password)
    users[username] = hashed_password

    # Save updated users to file
    with open("login_data.json", "w") as f:
        json.dump(users, f)

    put_success(f"Account created successfully! Welcome, {username}.")
    put_buttons(["Go to Sign In Page"], onclick=[sign_in])

def habittracker(username=None):
    clear()
    put_text(f"Habit Tracker Page for {username}")
    put_buttons(["Add a Habit"], onclick=[lambda: habits(username)])

def healthy_habits_recommendation():
    put_text("\nHere are some healthy habits you can add to your daily routine:")
    put_text("1. Drink at least 8 glasses of water every day!")
    put_text("2. Eat healthy snacks like fruits and nuts!")
    put_text("3. Exercise for 30 minutes a day!")
    put_text("4. Get at least 8 hours of sleep each night.")

def habits(username=None):
    clear()
    habit = input("What habit would you like to add?")
    healthy_habits_recommendation()
    put_text(f"You've added '{habit}' to your habits/routine!")
    put_buttons(["View Habits"], onclick=[lambda: view_habits(username)])
    with open('habits.json', 'w') as file:
        json.dump(habitslist, file, indent=4)



def view_habits(username):
    clear()
    put_text("Current default habits:").style('font-size: 30px;')

    habits_list = [
        "Drink water after lunch",
        "Exercise for 30 mins",
        "Eat a healthy snack",
        "Meditate for 10 mins",
        "Take a walk",
        "Read a book",
        "Practice Math",
        "Write in your journal",
        "Listen to music"
    ]

    put_buttons(["I Finished A Habit!"], onclick=done)

def done(username):
    global habit_list
    # Ask user to type the habit they want to mark as done
    habitdone = input("Type the habit you want to mark as done, exactly as it appears in the list:")
    
    # Initialize flag to track if habit is found
    habit_found = False

    # Loop through habitlist and check if the habit matches
    for i in habitlist:
        if i == habitdone:
            habitlist.remove(habitdone)
            put_success(f"Habit '{habitdone}' marked as done!")
            habit_found = True
            break  # Exit loop after marking the habit

    # If habit was not found, show an error message
    if not habit_found:
        put_error("Habit not found in list!")

    # Optionally, you can return to the habit tracker or update the display
    put_buttons(["Go Back to Habit Tracker"], onclick=lambda: habittracker(username))


# Sign In Page
def sign_in():
    clear()
    put_text("Sign In Page")

    # Gather username and password
    username = input("Username:")
    password = input("Password:", type=PASSWORD)

    # Hash the password
    hashed = hash_password(password)

    # Check if the credentials are valid
    if username not in users or users[username] != hashed:
        put_error("Invalid credentials!")
        return

    # If the credentials are valid, welcome the user and provide buttons to proceed
    put_success(f"Welcome back, {username}!")
    put_buttons(["Go to Welcome Page", "Take the Test"], onclick=[lambda: welcome(username), lambda: take_test(username)])


def home(username):
    put_button("View Habits")
    with open('habits.json', 'r') as file:
        users = json.load(file)
    put_text(users)
    put_button("Make Routine", onclick=[lambda: routines(username)])
    put_button("View Routines", onclick=[lambda: viewroutine(username)])




# Welcome Page
def welcome(username=None):
    clear()
    if username:
        put_text(f"Hello, {username}! Welcome to the site.")
        put_text("The first thing you must do is take the test!")
        put_buttons("TAKE THE TEST", onclick=take_test)
    else:
        put_text("Welcome to our site! Please sign in.")

# Test Page
def take_test(username=None):
    clear()
    if not username:
        put_error("You must be signed in to take the test!")
        return
    else:
        put_text("Take the test!")
        put_buttons(["Go to Habit Tracker Page"], onclick=[lambda: habittracker(username)])
        main2()

def main2():
    username, favorite_character, age, grade, subject, available_times = collect_user_info()

def collect_user_info():
    put_text("Welcome to your Study and Health Assistant!")
    username = input("Please enter a username: ")
    favorite_character = input("What's your favorite character? ")
    age = input("How old are you? ")
    grade = input("What grade are you in? (1-7): ")
    subject = input("What subject do you want to study? (Math, Science, English): ")
    available_times = input("How many hours can you study each day? ")

    quiz_functions = {
        "math": math_quiz,
        "science": science_quiz,
        "english": english_quiz
    }

    if subject.lower() in quiz_functions:
        quiz_functions[subject.lower()](grade)
    else:
        put_text(f"Sorry, we do not have a quiz available for {subject} right now.")

    return username, favorite_character, age, grade, subject, available_times

def healthy_habits_recommendation():
    put_text("\nHere are some healthy habits you can add to your daily routine:")
    put_text("1. Drink at least 8 glasses of water every day!")
    put_text("2. Eat healthy snacks like fruits and nuts!")
    put_text("3. Exercise for 30 minutes a day!")
    put_text("4. Get at least 8 hours of sleep each night.")

def study_plan_recommendation():
    put_text("\nHere is your study plan:")
    put_text("1. Spend at least 30 minutes reviewing your notes.")
    put_text("2. Spend a minimum 15 minutes practicing problems.")
    put_text("3. Spend at least 15 minutes doing fun quizzes!")

def practice_feedback(score, questions, subject, grade):
    total = len(questions)
    percent = (score / total) * 100
    put_text(f"\nYour score is {score} out of {total} ({percent:.1f}%).")


    if percent == 100:
        put_text(f"🌟 Perfect! You're a {subject} superstar! Move up to the next level for more challenge!")
    elif percent >= 70:
        put_text(f"✅ Great job! You passed with {percent:.1f}%. You're ready for the next level in {subject}!")
    else:
        put_text(f"⚠️ You scored {percent:.1f}%. It’s okay—not everyone gets it on the first try.")
        put_text(f"📘 Here's what to do next:")
        for question in questions:
            if 'user_answer' in question and question['answer'].lower() not in question['user_answer'].lower():
                put_text(f"   • Review: {question['question']}")

        if grade == '1':
            put_text("🔁 You're already at the lowest grade level. Just review and try again!")
        else:
            put_text(f"🔄 Consider retrying this quiz or temporarily switching to Grade {int(grade)-1} for review.")

    # Suggest next steps
    if percent >= 70:
        next_grade = str(int(grade) + 1) if int(grade) < 7 else None
        if next_grade:
            put_text(f"👉 Want to challenge yourself? Try Grade {next_grade} in {subject} next!")
        else:
            put_text("🎓 You’ve reached the highest grade in this subject. Awesome work!")

# Insert your math_quiz, science_quiz, and english_quiz functions below:
# Make sure in each of them you do this inside the loop:
# question['user_answer'] = answer

  # Math quiz based on grade
def math_quiz(grade):
    put_text(f"\nStarting your Math quiz for Grade {grade}!")

    if grade == '1':
        questions = [
            {"question": "What is 1 + 1?", "answer": "2"},
            {"question": "What is 2 + 2?", "answer": "4"},
            {"question": "What is 3 + 3?", "answer": "6"},
            {"question": "What is 4 + 4?", "answer": "8"},
            {"question": "What is 5 + 5?", "answer": "10"},
            {"question": "What is 6 + 3?", "answer": "9"},
            {"question": "What is 7 + 2?", "answer": "9"},
            {"question": "What is 8 + 1?", "answer": "9"},
            {"question": "What is 9 + 0?", "answer": "9"},
        ]
    elif grade == '2':
        questions = [
            {"question": "What is 10 + 5?", "answer": "15"},
            {"question": "What is 20 - 10?", "answer": "10"},
            {"question": "What is 3 + 4?", "answer": "7"},
            {"question": "What is 8 - 3?", "answer": "5"},
            {"question": "What is 7 + 6?", "answer": "13"},
            {"question": "What is 12 - 5?", "answer": "7"},
            {"question": "What is 9 + 4?", "answer": "13"},
            {"question": "What is 15 - 7?", "answer": "8"},
            {"question": "What is 6 + 9?", "answer": "15"},
        ]
    elif grade == '3':
        questions = [
            {"question": "What is 12 + 8?", "answer": "20"},
            {"question": "What is 15 - 9?", "answer": "6"},
            {"question": "What is 6 + 7?", "answer": "13"},
            {"question": "What is 14 - 8?", "answer": "6"},
            {"question": "What is 18 + 7?", "answer": "25"},
            {"question": "What is 16 - 6?", "answer": "10"},
            {"question": "What is 9 + 5?", "answer": "14"},
            {"question": "What is 13 - 4?", "answer": "9"},
            {"question": "What is 10 + 10?", "answer": "20"},
        ]
    elif grade == '4':
        questions = [
            {"question": "What is 15 × 2?", "answer": "30"},
            {"question": "What is 36 ÷ 6?", "answer": "6"},
            {"question": "What is 8 × 7?", "answer": "56"},
            {"question": "What is 25 ÷ 5?", "answer": "5"},
            {"question": "What is 9 × 6?", "answer": "54"},
            {"question": "What is 56 ÷ 8?", "answer": "7"},
            {"question": "What is 13 × 3?", "answer": "39"},
            {"question": "What is 72 ÷ 9?", "answer": "8"},
            {"question": "What is 16 × 4?", "answer": "64"},
        ]
    elif grade == '5':
        questions = [
            {"question": "What is 1/2 + 1/4?", "answer": "3/4"},
            {"question": "What is 3/4 - 1/8?", "answer": "5/8"},
            {"question": "What is 0.75 + 0.25?", "answer": "1"},
            {"question": "What is 2/3 ÷ 1/6?", "answer": "4"},
            {"question": "If x + 5 = 12, what is x?", "answer": "7"},
            {"question": "What is 5 × 6?", "answer": "30"},
            {"question": "What is 250 ÷ 5?", "answer": "50"},
            {"question": "What is 9 × 7?", "answer": "63"},
            {"question": "What is 5.5 + 7.25?", "answer": "12.75"},
        ]
    elif grade == '6':
        questions = [
            {"question": "What is 3/5 + 4/10?", "answer": "7/10"},
            {"question": "What is 2.75 + 3.5?", "answer": "6.25"},
            {"question": "If 2x - 3 = 7, what is x?", "answer": "5"},
            {"question": "What is 6 × 12?", "answer": "72"},
            {"question": "What is 144 ÷ 12?", "answer": "12"},
            {"question": "What is the area of a rectangle with length 8 and width 5?", "answer": "40"},
            {"question": "What is 3/8 ÷ 1/4?", "answer": "3/2"},
            {"question": "What is 5²?", "answer": "25"},
            {"question": "What is 7.6 × 2.5?", "answer": "19"},
        ]
    elif grade == '7':
        questions = [
            {"question": "What is the solution to 4x + 5 = 21?", "answer": "4"},
            {"question": "What is 0.375 × 16?", "answer": "6"},
            {"question": "What is the volume of a cube with a side length of 3 cm?", "answer": "27 cm³"},
            {"question": "What is the perimeter of a rectangle with length 10 and width 4?", "answer": "28"},
            {"question": "If x² = 49, what is x?", "answer": "7"},
            {"question": "What is 12/7 as a mixed number?", "answer": "1 5/7"},
            {"question": "Solve for y: 3y + 6 = 15", "answer": "3"},
            {"question": "What is the area of a triangle with base 6 and height 9?", "answer": "27"},
            {"question": "What is 1/3 + 2/5?", "answer": "11/15"},
        ]
    score = 0
    for question in questions:
        answer = input(question['question'] + " ")
        question['user_answer'] = answer
        if answer.strip() == question['answer']:
            put_text("Correct!")
            score += 1
        else:
            put_text(f"Oops! The correct answer is {question['answer']}.")

    practice_feedback(score, questions, "Math", grade)

# Science quiz based on grade
def science_quiz(grade):
    put_text(f"\nStarting your Science quiz for Grade {grade}!")

    if grade == '1':
        questions = [
            {"question": "What color is the sky?", "answer": "Blue"},
            {"question": "What do plants need to grow?", "answer": "Water"},
            {"question": "What animal barks?", "answer": "Dog"},
            {"question": "What is the main source of light during the day?", "answer": "Sun"},
            {"question": "What do we call the water that falls from the sky?", "answer": "Rain"},
            {"question": "What is the name of our planet?", "answer": "Earth"},
            {"question": "What do we call the place where animals live?", "answer": "Habitat"},
            {"question": "What do bees make?", "answer": "Honey"},
            {"question": "What is the name of the season when it snows?", "answer": "Winter"},
        ]
    elif grade == '2':
        questions = [
            {"question": "What is the process by which plants make their food?", "answer": "Photosynthesis"},
            {"question": "What are the three states of matter?", "answer": "Solid, Liquid, Gas"},
            {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
            {"question": "What is the process by which a caterpillar turns into a butterfly?", "answer": "Metamorphosis"},
            {"question": "What do we call the force that pulls objects toward the Earth?", "answer": "Gravity"},
            {"question": "Which part of the plant absorbs water?", "answer": "Roots"},
            {"question": "What is the main source of energy for life on Earth?", "answer": "Sunlight"},
            {"question": "What type of rock is formed by volcanic activity?", "answer": "Igneous"},
            {"question": "What is the name of the gas that plants use for photosynthesis?", "answer": "Carbon dioxide"},
        ]
    elif grade == '3':
        questions = [
            {"question": "What is the process by which plants turn sunlight into food?", "answer": "Photosynthesis"},
            {"question": "What is the water cycle?", "answer": "Evaporation, Condensation, Precipitation"},
            {"question": "What are the five senses?", "answer": "Sight, Hearing, Taste, Touch, Smell"},
            {"question": "What is the Earth’s atmosphere made of?", "answer": "Nitrogen, Oxygen, Argon"},
            {"question": "What do we call the animal that eats plants?", "answer": "Herbivore"},
            {"question": "What do we call the animal that eats meat?", "answer": "Carnivore"},
            {"question": "What part of the plant takes in sunlight?", "answer": "Leaves"},
            {"question": "What is the name of the process that allows fish to breathe underwater?", "answer": "Gills"},
            {"question": "What is the smallest planet in our solar system?", "answer": "Mercury"},
        ]
    elif grade == '4':
        questions = [
            {"question": "What is the process by which plants make their food?", "answer": "Photosynthesis"},
            {"question": "What is the only planet that supports life?", "answer": "Earth"},
            {"question": "What is the force that keeps us on the ground?", "answer": "Gravity"},
            {"question": "What do we call the gas we breathe?", "answer": "Oxygen"},
            {"question": "What is the process by which plants lose water?", "answer": "Transpiration"},
            {"question": "What is the biggest planet?", "answer": "Jupiter"},
            {"question": "What gas do plants take in from the air?", "answer": "Carbon dioxide"},
            {"question": "What type of rock is formed from cooled lava?", "answer": "Igneous rock"},
            {"question": "What is the center of the solar system?", "answer": "The Sun"},
        ]
    elif grade == '5':
        questions = [
            {"question": "What is the gas that humans breathe out?", "answer": "Carbon dioxide"},
            {"question": "What is the process of water changing from liquid to gas?", "answer": "Evaporation"},
            {"question": "What is the Earth's core made of?", "answer": "Iron and nickel"},
            {"question": "What is the largest land animal?", "answer": "Elephant"},
            {"question": "Which planet is known as the 'Red Planet'?", "answer": "Mars"},
            {"question": "What is the longest river in the world?", "answer": "Amazon River"},
            {"question": "What is the name of our galaxy?", "answer": "Milky Way"},
            {"question": "What is the force that causes objects to fall to the ground?", "answer": "Gravity"},
            {"question": "What is the name of the nearest star to Earth?", "answer": "The Sun"},
        ]
    elif grade == '6':
        questions = [
            {"question": "What is the chemical formula for water?", "answer": "H2O"},
            {"question": "How many continents are there on Earth?", "answer": "7"},
            {"question": "What is the process by which rocks are formed?", "answer": "The rock cycle"},
            {"question": "What is the primary source of energy for the Earth?", "answer": "The Sun"},
            {"question": "What is the process by which animals breathe in oxygen?", "answer": "Respiration"},
            {"question": "What type of energy does the sun provide?", "answer": "Solar energy"},
            {"question": "What type of clouds bring rain?", "answer": "Cumulonimbus"},
            {"question": "What is the outermost layer of the Earth?", "answer": "The crust"},
            {"question": "What is the name of the force that attracts objects toward the Earth?", "answer": "Gravity"},
        ]
    elif grade == '7':
        questions = [
            {"question": "What is the chemical symbol for oxygen?", "answer": "O2"},
            {"question": "What is the primary function of the heart?", "answer": "To pump blood"},
            {"question": "What is the process by which plants make food?", "answer": "Photosynthesis"},
            {"question": "What is the name of the nearest galaxy to the Milky Way?", "answer": "Andromeda"},
            {"question": "What is the primary gas in Earth's atmosphere?", "answer": "Nitrogen"},
            {"question": "What is the chemical formula for carbon dioxide?", "answer": "CO2"},
            {"question": "What is the process of water moving through plants?", "answer": "Transpiration"},
            {"question": "What is the chemical formula for methane?", "answer": "CH4"},
            {"question": "What is the name of the Earth's outermost layer?", "answer": "The crust"},
        ]


    score = 0
    for question in questions:
        answer = input(question['question'] + " ")
        question['user_answer'] = answer
        if answer.lower().strip() == question['answer'].lower():
            put_text("Correct!")
            score += 1
        else:
            put_text(f"Oops! The correct answer is {question['answer']}.")

    practice_feedback(score, questions, "Science", grade)

def english_quiz(grade):
    put_text(f"\nStarting your English quiz for Grade {grade}!")

    if grade == '1':
        questions = [
            {"question": "What is the opposite of 'hot'?", "answer": "cold"},
            {"question": "What letter comes after B?", "answer": "C"},
            {"question": "Which one is a noun: cat, run, happy?", "answer": "cat"},
            {"question": "What do you put at the end of a question?", "answer": "question mark"},
            {"question": "What sound does 'sh' make in 'shoe'?", "answer": "sh"},
            {"question": "Which word rhymes with 'hat'? Bat or big?", "answer": "bat"},
            {"question": "Is 'run' a verb or a noun?", "answer": "verb"},
        ]
    elif grade == '2':
        questions = [
            {"question": "What is the past tense of 'walk'?", "answer": "walked"},
            {"question": "Which is a pronoun: she, red, car?", "answer": "she"},
            {"question": "What do we call a name of a person, place, or thing?", "answer": "noun"},
            {"question": "What punctuation ends a sentence?", "answer": "period"},
            {"question": "What word is opposite of 'fast'?", "answer": "slow"},
            {"question": "Which word is an adjective: blue, jump, cat?", "answer": "blue"},
            {"question": "What is a sentence?", "answer": "a complete thought"},
        ]
    elif grade == '3':
        questions = [
            {"question": "What is a synonym for 'happy'?", "answer": "joyful"},
            {"question": "What is an antonym for 'cold'?", "answer": "hot"},
            {"question": "What is a compound word made of 'sun' and 'shine'?", "answer": "sunshine"},
            {"question": "What do you call a word that describes a noun?", "answer": "adjective"},
            {"question": "What is the plural of 'baby'?", "answer": "babies"},
            {"question": "Is 'quickly' an adverb or an adjective?", "answer": "adverb"},
            {"question": "What is a verb?", "answer": "an action word"},
        ]
    elif grade == '4':
        questions = [
            {"question": "What is the subject in the sentence: 'The dog ran fast.'?", "answer": "dog"},
            {"question": "Which word is a preposition: under, jump, dog?", "answer": "under"},
            {"question": "What is the past tense of 'run'?", "answer": "ran"},
            {"question": "What is a conjunction?", "answer": "a word that connects sentences"},
            {"question": "What is a simile?", "answer": "a comparison using like or as"},
            {"question": "What is an antonym of 'laugh'?", "answer": "cry"},
            {"question": "What is a proper noun?", "answer": "a specific name"},
        ]
    elif grade == '5':
        questions = [
            {"question": "What is an adverb?", "answer": "a word that describes a verb"},
            {"question": "What is a metaphor?", "answer": "a direct comparison without like or as"},
            {"question": "What is the root word of 'unhappily'?", "answer": "happy"},
            {"question": "What does an interjection do?", "answer": "shows emotion"},
            {"question": "What is the plural of 'child'?", "answer": "children"},
            {"question": "Which is a complete sentence: 'Went to the store.' or 'She went to the store.'?", "answer": "She went to the store."},
            {"question": "What part of speech is 'because'?", "answer": "conjunction"},
        ]
    elif grade == '6':
        questions = [
            {"question": "What is a thesis statement?", "answer": "the main idea of an essay"},
            {"question": "What is an idiom?", "answer": "a phrase with a different meaning than the words"},
            {"question": "What is a synonym for 'angry'?", "answer": "mad"},
            {"question": "What is personification?", "answer": "giving human traits to non-human things"},
            {"question": "What is an article in grammar?", "answer": "a, an, the"},
            {"question": "What does a conjunction do?", "answer": "connects clauses/sentances"},
            {"question": "What is a compound sentence?", "answer": "two sentences joined by a conjunction"},
        ]
    elif grade == '7':
        questions = [
            {"question": "What is a clause?", "answer": "a group of words with a subject and verb"},
            {"question": "What is a complex sentence?", "answer": "a sentence with one independent and one dependent clause"},
            {"question": "What is the passive voice?", "answer": "when the subject receives the action"},
            {"question": "What is a gerund?", "answer": "a verb form ending in -ing used as a noun"},
            {"question": "What is an oxymoron?", "answer": "two opposite words used together"},
            {"question": "What is a transition word?", "answer": "a word that connects ideas"},
            {"question": "What is the difference between 'its' and 'it's'?", "answer": "'its' is possessive, 'it's' means 'it is'"},
        ]



def routines(username):
    clear()
    put_text(f"Routine Page")
    put_buttons(["Add a Routine"], onclick=addroutine)

def addroutine(username):
    clear()
    routine = input("What routine would you like to add?")
    put_buttons("Add Habit Into Routine", onclick=addhabit(username))
    with open('routinehabits.json', 'w') as file:
        users = json.load(file)

def addhabit(username):
    clear()
    habit = input("What habit would you like to add?")
    with open('routinehabits.json', 'w') as file:
        users = json.dump(file)
    

def viewroutine(username):
    clear()
    with open('routinehabits.json', 'r') as file:
        users = json.load(file)
    put_text(users)



    random.shuffle(questions)
    score = 0
    for question in questions:
        answer = input(question['question'] + " ")
        question['user_answer'] = answer
        if answer.lower().strip() == question['answer'].lower():
            put_text("Correct!")
            score += 1
        else:
            put_text(f"Oops! The correct answer is {question['answer']}.")

    practice_feedback(score, questions, "English", grade)
