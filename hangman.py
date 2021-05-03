from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QCursor, QFont
from PyQt5 import QtGui, QtCore
import sys
from random import randint


app = QApplication(sys.argv)
win = QWidget()
win.setGeometry(300,200,1300,900)
#. X co-ordinat, Y co-ordinate, Width of the window to be set,Height of the window to be set
win.setWindowTitle("Hangman")
win.setStyleSheet("background: #161219;")

grid = QGridLayout()

#title
label = QtWidgets.QLabel(win)
label.setText(f"Let's play \n          Hangman")
label.setFont(QFont('Roboto', 40))
label.setStyleSheet("margin-top: 5px; font-weight: bold; color: 'white'")
label.adjustSize()
grid.addWidget(label, 0, 0,1,3)

#display logo
logo = QLabel()
image = QPixmap('Hangman.png')
logo.setPixmap(image)
#logo.setAlignment(QtCore.Qt.AlignRight)
logo.setStyleSheet("margin-top: 70px;")
#logo.move(0,0)
grid.addWidget(logo, 0,7,7,5)


# Verlierer
winlost = QWidget()
winlost.setGeometry(500,500,700,300)
winlost.setStyleSheet("background: 'white'")
labelLost = QtWidgets.QLabel(winlost)
labelLost.setText("You lost! :-(")
labelLost.setFont(QFont('Roboto', 38))
labelLost.setStyleSheet("margin-top: 5px; font-weight: bold; color: #161219;")
labelLost.move(80,100) #x,y


#Gewinner
winwon = QWidget()
winwon.setGeometry(500,500,700,300)
winwon.setStyleSheet("background: 'white'")
labelwon = QtWidgets.QLabel(winwon)
labelwon.setText("You're a hero' :-)")
labelwon.setFont(QFont('Roboto', 38))
labelwon.setStyleSheet("margin-top: 5px; font-weight: bold; color: #161219;")
labelwon.move(80,100) #x,y



def new_game():
    f = open('nounlist.txt')
    all_lines = f.readlines()
    number_of_lines = len(all_lines)
    index =(randint(1,number_of_lines))
    secret = (all_lines[index - 1])
    global secret_word
    secret_word = [*secret]
    secret_word.pop()
    print(secret_word)
    lines = len(secret_word)*"_"
    global holder
    holder =[*lines]
    global trial
    trial = 0
    global count
    count = 0
    global letter_storage
    letter_storage=[]
    label = QtWidgets.QLabel(win)
    label.setText(f"Can you guess the secret word? It has {len(secret_word)} characters.")
    label.setFont(QFont('Monterrat', 16))
    label.setStyleSheet("margin-top: 10px;"+"color: 'white'")
    label.adjustSize()
    grid.addWidget(label, 1, 0,1,3)
    label_instructions = QtWidgets.QLabel(win)
    label_instructions.setText('Type a letter and click "Submit" to make a guess. \n Click "Solve" to solve.')
    label_instructions.setFont(QFont('Montserrat', 16))
    label_instructions.setStyleSheet("margin-top: 10px;"+"color: 'white'")
    label_instructions.adjustSize()
    grid.addWidget(label_instructions, 2, 0,1,3)
    #SChon geratene
    groupbox = QGroupBox("Bad guesses:")
    hbox = QHBoxLayout()
    groupbox.setLayout(hbox)
    groupbox.setFont(QFont('Monterrat', 14))
    groupbox.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'color: "white";'
                 'padding-left: 10px;'
                 'padding-right: 10px; }'
                 'border: 1px solid "white";'
                 'border-radius: 15px;')
    groupbox.setAlignment(QtCore.Qt.AlignCenter)
    grid.addWidget(groupbox,7,7,1,4)

    #Striche als Platzhalter
    label_blank = QtWidgets.QLabel(win)
    #label_blank.setText(len(secret_word)*"_ ")
    label_blank.setFont(QFont('Arial', 32))
    label_blank.setStyleSheet("color: 'white'")
    grid.addWidget(label_blank, 3,0,1,3)
    k=0
    for char in secret_word:
        if char == "-":
            holder[k]= "-"
        k = k + 1
    label_blank.setText(' '.join(holder))



    def compare_char(guess):
        guess = guess.lower()
        global trial
        global letter_storage
        global count
        while trial < 5:
            label_remaining_Trials= QtWidgets.QLabel(win)
            label_remaining_Trials.setText(f"Remaining trials: {5-trial}")
            label_remaining_Trials.setFont(QFont('Montserrat', 16))
            label_remaining_Trials.setStyleSheet("color: 'white'")
            label_remaining_Trials.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(label_remaining_Trials, 6,0,1,3)
            #print(letter_storage)
            if guess in letter_storage:
                #print("You already guessed that")
                break
            elif guess == "":
                #print("Your input is empty")
                break
            elif guess not in letter_storage and guess not in secret_word:
                #print("\n Bad guess! \n")
                letter_storage.append(guess)
                label_letter_storage =QtWidgets.QLabel(win)
                label_letter_storage.setText(guess)
                label_letter_storage.setFont(QFont('Arial',14))
                label_letter_storage.setStyleSheet("color: 'white'; margin-left: rand;" )
                #label_letter_storage.setAlignment(QtCore.Qt.AlignLeft)
                hbox.addWidget(label_letter_storage)

                trial += 1
                count+=1
                #print(count)
                break
            elif guess not in letter_storage and guess in secret_word:
                #print("\n Good guess! \n")
                count +=1
                #print(count)
                letter_storage.append(guess)
                k=0
                for char in secret_word:
                    if char == guess:
                        holder[k]=guess
                    k = k + 1
                label_blank.setText(' '.join(holder))
                break

        else:
            #print("You lose!")
            winlost.show()
    #Eingabemaske
    line_input = QtWidgets.QLineEdit(win)
    line_input.setMaxLength(1)
    line_input.setFont(QFont('Arial', 14))
    line_input.setStyleSheet("color: 'white'")
    grid.addWidget(line_input, 4, 0,1,3)

    #Submit
    button = QtWidgets.QPushButton(win)
    button.setText("Submit")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFont(QFont('Arial', 14))
    button.clicked.connect(lambda: compare_char(line_input.text()))
    button.clicked.connect(line_input.clear)
    button.setStyleSheet("margin-top: 5px; border: 1px solid 'white'; border-radius: 8px; width: 220px; color: 'white'")
    grid.addWidget(button, 5, 0)


def compare():
    try_solve = line_solve.text()
    try_solve = try_solve.lower()
    if [*try_solve] == secret_word:
        winwon.show()
    else:
        winlost.show()



new_game()

#Seite um zu lösen
winsolve = QWidget()
gridsolve = QGridLayout()
winsolve.setWindowTitle("Solve")
winsolve.setGeometry(500,500,800,500)
winsolve.setStyleSheet("background: 'white'")
label2 = QtWidgets.QLabel(winsolve)
label2.setText("Enter the secret word!")
label2.setFont(QFont('Roboto', 26))
label2.setStyleSheet("margin-bottom:70px;font-weight: bold; color: #161219;")
gridsolve.addWidget(label2,0,0,1,5)

# EIngabe Lösungswort
line_solve = QtWidgets.QLineEdit(winsolve)
line_solve.setFont(QFont('Arial', 16))
line_solve.setStyleSheet("margin-bottom:20px;border: 1px solid #161219;border-radius 8px;color: #161219;")
#line_solve.move(200,150)
gridsolve.addWidget(line_solve,1,1,1,2)
#print(line_solve.text())
#Sumbit
button_solve = QPushButton(winsolve)
button_solve.setText("Submit")
button_solve.setFont(QFont('Monsterrat',14))
button_solve.setStyleSheet("margin-bottom:100px;border: 1px solid #161219; border-radius: 8px; color: #161219;")
button_solve.clicked.connect(compare)
#button_solve.resize(200,32)
gridsolve.addWidget(button_solve, 2,1,1,2)
#button_solve.move(200, 200)
winsolve.setLayout(gridsolve)
def solve():
    winsolve.show()

# Neues Spiel nach verlieren
button = QtWidgets.QPushButton(winlost)
#button.setFixedWidth(250)
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
button.setText("New Game")
button.setFont(QFont('Arial', 14))
button.setStyleSheet("padding: 3px;margin-top: 5px;border: 1px solid #161219; border-radius: 8px; color: #161219;")
button.move(250,210)
button.clicked.connect(new_game)
button.clicked.connect(winlost.close)
button.clicked.connect(winsolve.close)

# Neues Spiel nach gewinnen
button = QtWidgets.QPushButton(winwon)
#button.setFixedWidth(250)
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
button.setText("New Game")
button.setFont(QFont('Arial', 14))
button.move(250,210)
button.setStyleSheet("padding: 3px;margin-top: 5px;border: 1px solid #161219; border-radius: 8px; color: #161219;")
button.clicked.connect(new_game)
button.clicked.connect(winwon.close)
button.clicked.connect(winsolve.close)


#Buttons main
button = QtWidgets.QPushButton(win)
button.setText("Solve")
#button.setFixedWidth(150)
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
button.setFont(QFont('Arial', 14))
button.setStyleSheet("margin-top: 5px; border: 1px solid 'white'; color: 'white'; border-radius: 8px;")
button.clicked.connect(solve)
grid.addWidget(button, 5, 1)

button = QtWidgets.QPushButton(win)
#button.setFixedWidth(250)
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
button.setText("New Game")
button.setFont(QFont('Arial', 14))
button.setStyleSheet("margin-top: 5px;border: 1px solid 'white'; border-radius: 8px; color: 'white';")
button.clicked.connect(new_game)
grid.addWidget(button, 5, 2)



win.setLayout(grid)
win.show()
sys.exit(app.exec_())
