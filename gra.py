import os
import random
import subprocess


# --------------------------------------------------- SETUP -----------------------------------------------------------
class Game1:
    nick1 = 'Samsung'
    nick2 = 'Nokia'
    nick3 = 'Huawei'
    nick4 = 'Apple'


class Game2:
    nick1 = 'Apple'
    nick2 = 'Acer'
    nick3 = 'Lenovo'
    nick4 = 'HP'


class Game3:
    nick1 = 'Ukraine'
    nick2 = 'Russia'
    nick3 = 'UK'
    nick4 = 'USA'


class Game4:
    nick1 = 'Volvo'
    nick2 = 'VW'
    nick3 = 'TESLA'
    nick4 = 'Ford'


class Game5:
    nick1 = 'BMW'
    nick2 = 'Jaguar'
    nick3 = 'Jeep'
    nick4 = 'Mercedes'

 
class Game6:
    nick1 = 'Books'
    nick2 = 'Games'
    nick3 = 'PC'
    nick4 = 'Phones'


# ------------------------------------------------ RETURN PLAYER NICK ------------------------------------------------
games = [Game1, Game2, Game3, Game4, Game5, Game6]


class ChoosePlayer:
    names = random.choice(games)
    player1 = names.nick1
    player2 = names.nick2
    player3 = names.nick3
    player4 = names.nick4
    print(names.nick1)
    print(names.nick2)
    print(names.nick3)
    print(names.nick4)



choice = ChoosePlayer
p1 = choice.player1
p2 = choice.player2
p3 = choice.player3
p4 = choice.player4
c5 = 'RESTART'


# --------------------------------------------------RUN SCRIPTS ------------------------------------------------------
subprocess.run(f'python ./data_scrape.py {p1} {p2} {p3} {p4} {c5} & '
               f'python ./game.py {p1} {p2} {p3} {p4} {c5}',
               shell=True)

