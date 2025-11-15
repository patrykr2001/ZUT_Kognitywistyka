from time import sleep, time
from pygame import mixer
import datetime
import os

mixer.init()
sound=mixer.Sound("brown_noise.wav")
beep=mixer.Sound("beep.wav")

long_wait = 60
short_wait = 30

with open("Events.txt", "a") as file:
    file.writelines("Latency         timeStamp          type")

start_time = time()


def time_measurement(start_time: float, end_time: float, type: str) -> None:
    latency = (end_time - start_time).__round__(3)
    timeStamp = datetime.datetime.now().timestamp()

    with open("Events.txt", "a") as file:
        file.writelines(f"\n{round(latency, 4)}      {timeStamp}     {type}")

    print("File saved!")

def playSound():
    sound.play(-1)
    sleep(long_wait)
    sound.stop()

def activities():
    l_wait = 10
    s_wait = 5
    print("Dodaj liczby: 198 + 679")
    sleep(s_wait)
    print("Pomnóż liczby: 54 * 23")
    sleep(s_wait)
    print("Podziel liczby: 987 / 32")
    sleep(s_wait)
    print("Wyobraź sobie najdokładniej jak potrafisz fioletową krowę latającą nad zielonymi wzgórzami.")
    sleep(l_wait)
    print("Policz w myślach od 100 do 0 co 3.")
    sleep(l_wait)
    print("Wyobraź sobie, że lecisz na wielorybie przez ocean.")
    sleep(l_wait)
    print("Znajdź niepasujący element: jabłko, banan, marchewka, gruszka.")
    sleep(s_wait)
    print("Znajdź niepasujący element: stół, krzesło, sofa, rower.")
    sleep(s_wait)
    print("Dodaj liczby: 345 + 678")
    sleep(s_wait)

for i in range(10):
    end_time = time()
    beep.play()
    time_measurement(start_time, end_time, f"Task {i+1}")

    os.system('cls')

    match i:
        case 0:
            print("1 - zamknięte oczy")
            sleep(short_wait)
        case 1:
            print("2 - otwarte oczy, normalne mruganie")
            sleep(short_wait)
        case 2:
            print("3 - otwarte oczy, bez mrugania")
            sleep(short_wait)
        case 3:
            print("4 - szybkie mruganie")
            sleep(short_wait)
        case 4:
            print("5 - zaciskanie szczęk, normalne mruganie")
            sleep(short_wait)
        case 5:
            print("6 - ruchy oczu w prawo i w lewo")
            sleep(short_wait)
        case 6:
            print("7 - mówienie, normalne mruganie")
            sleep(short_wait)
        case 7:
            print("8 - ruchy głowy bez mrugania")
            sleep(short_wait)
        case 8:
            print("9 - relaks przy muzyce")
            playSound()
        case 9:
            activities()


print("Dziękujemy za udział w badaniu C:")