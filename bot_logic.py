import random

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

def toss_coin():
    s = ""
    a = random.randint(1,2)
    if a == 1:
        s = "Орёл"
    elif a == 2:
        s = "Решка"
    return s