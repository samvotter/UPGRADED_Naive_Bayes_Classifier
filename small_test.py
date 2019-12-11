from Bayesian_Tables import BayesianTable
from Bayesian_Engine import BayesianEngine
from Mind_Web import MindManager

brain = MindManager()

table_a = BayesianTable("A")

table_b = BayesianTable("B")

table_c = BayesianTable("C")

table_d_a = BayesianTable("D")

table_e_b = BayesianTable("E")

table_f_c = BayesianTable("F")

string_a = "I like FM5 Cafe's seating much more than FM7's Cafe. However, FM7 has several food items that " \
           "FM5 does not. FM7's food is generally much better, even when both Cafe's carry the same items. " \
           "For example, the dedicated pizzeria at FM7 is far superior to the lamp-heated pizza at FM5."

string_b = "FM1 is the Information Security Command Center. There is no food allowed in FM1. If people in FM1 " \
           "want to get food, they must go to FM7. The last time I visited FM1, we were treated to free delicious " \
           "cake! They were celebrating the monthly birthday party for everyone in the whole department. It was great."

string_c = "In the hallway between FM1 and FM7 there is a game room with billards, foosball, and air hockey. I don't " \
           "get to play there much because FM7 is so far away from FM4, but foosball is definitely MY game. I crush at " \
           "foosball. There is no spinning allowed in foosball because it damages the machine and rewards unskillful play."

string_d_a = "The FM5 Cafe is better than FM7. While Fm5 has less things and lower quality than FM7, I love the " \
             "friendly atmosphere and open seating. Fm7 is crowded and awful. Sometimes when I eat at FM7 I want to " \
             "throw up. When I eat at FM5, my tastebuds are like: 'YUMYUM!' and that is the emotion I want from food."

string_e_b = "Information Security is super cool. If I wanted to do work with Information Security I would want " \
             "to work in fm1. It would mean that I would have to give up my precious fm5 cafe, as fm1 is much closer " \
             "to fm7. At least in fm1, there's plenty of free cake every month. Free cake is my favorite food!"

string_f_c = "Playing games is great! Over in fm5, we do not get to play games. Games are frown upon. Only the people " \
             "in fm7 get to play games. They invite their fm1 friends over to play foosball and other such events. " \
             "Sometimes I get jealous of such people and black out for a bit. If only I could get to the game room."

table_a.add_string(string_a)
table_b.add_string(string_b)
table_c.add_string(string_c)
table_d_a.add_string(string_d_a)
table_e_b.add_string(string_e_b)
table_f_c.add_string(string_f_c)

eng = BayesianEngine("Vendor Group", [table_a, table_b, table_c])

eng.format_tables()

print(eng.make_prediction(table_f_c, verbose=True))

for table in eng.tables:
    brain.export_memory("TEST", "TEST", eng.tables[table])

data = BayesianTable("BananaBanana", brain.import_memory("TEST", "A"))

print(data.frequencies)