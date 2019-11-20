# UPGRADED_Naive_Bayes_Classifier
An upgraded and generalized version of the Naive Bayes Classifier.

This program contains two modules. 

1. Bayesian_Tables
2. Bayesian_Engine

"Tables" is designed to ingest string data and organize it into a data structure readable to the classifier engine. 
"Engine" performs the math needed to make comparisons and bucket new data. 

The following is a test implementation to make sure the algorithm functions as anticipated and represents the basic structure for calling these two modules.

*******************************************************************************************************************
import Bayesian_Tables as b
from Bayesian_Engine import BayesianEngine

table_a = b.FrequencyTable("A")

table_b = b.FrequencyTable("B")

table_c = b.FrequencyTable("C")

table_d_a = b.FrequencyTable("D")

table_e_b = b.FrequencyTable("E")

table_f_c = b.FrequencyTable("F")
*******************************************************************************************************************
# Notice how the frequency table is initialized without providing any data. The argument is only the name to call that
# particular table. Both the buckets you wish to create and then the string data you wish to classify are FrquencyTables
*******************************************************************************************************************

string_a = "I like FM5 Cafe's seating much more than FM7's Cafe. However, FM7 has several food items that " \
           "FM5 does not. FM7's food is generally much better, even when both Cafe's carry the same items. " \
           "For example, the dedicated pizzeria at FM7 is far superior to the lamp-heated pizza at FM5".split()

string_b = "FM1 is the Information Security Command Center. There is no food allowed in FM1. If people in FM1 " \
           "want to get food, they must go to FM7. The last time I visited FM1, we were treated to free delicious " \
           "cake! They were celebrating the monthly birthday party for everyone in the whole department. It was great.".split()

string_c = "In the hallway between FM1 and FM7 there is a game room with billards, foosball, and air hockey. I don't " \
           "get to play there much because FM7 is so far away from FM4, but foosball is definitely MY game. I crush at " \
           "foosball. There is no spinning allowed in foosball because it damages the machine and rewards unskillful play.".split()

string_d_a = "The FM5 Cafe is better than FM7. While Fm5 has less things and lower quality than FM7, I love the " \
             "friendly atmosphere and open seating. Fm7 is crowded and awful. Sometimes when I eat at FM7 I want to " \
             "throw up. When I eat at FM5, my tastebuds are like: 'YUMYUM!' and that is the emotion I want from food.".split()

string_e_b = "Information Security is super cool. If I wanted to do work with Information Security I would want " \
             "to work in fm1. It would mean that I would have to give up my precious fm5 cafe, as fm1 is much closer " \
             "to fm7. At least in fm1, there's plenty of free cake every month. Free cake is my favorite food!".split()

string_f_c = "Playing games is great! Over in fm5, we do not get to play games. Games are frown upon. Only the people " \
             "in fm7 get to play games. They invite their fm1 friends over to play foosball and other such events. " \
             "Sometimes I get jealous of such people and black out for a bit. If only I could get to the game room.".split()
             
*******************************************************************************************************************
# In this example:
#   1. string_a mostly contains discusion about fm5 and fm7 cafes. I expect string data which deals heavily in food
#       and those locations will get classified as belonging to 'A'
#   2. string_b mostly contains discussion of FM1 and information security. It also mentions cake, this is to try and
#       create some overlap with string_a but with enough differences that fm1 and info security should be classified here
#   3. string_c mostly contains discussions of games and the game room. It also mentions fm1 and fm7 to create overlap
#       with string_b. I expect game strings to be classified here
#   4. strings d_a e_b and f_c are named in continuing alphabetical order suffixed with the classification bucket I expect
#       them to fall into.
*******************************************************************************************************************

for word in string_a:
    table_a.add_word(word)

for word in string_b:
    table_b.add_word(word)

for word in string_c:
    table_c.add_word(word)

for word in string_d_a:
    table_d_a.add_word(word)

for word in string_e_b:
    table_e_b.add_word(word)

for word in string_f_c:
    table_f_c.add_word(word)

*******************************************************************************************************************
# each table is built up word by word using the add_word() function
*******************************************************************************************************************

eng = BayesianEngine([table_a, table_b, table_c])

eng.account_for_unknowns()

*******************************************************************************************************************
# instantiate the Engine object by passing in the frequencytables that new data will be classified into
# also performs math functions to adjust the frequency tables into proportions and create a system such that 
# unknown values will be accounted for
*******************************************************************************************************************

eng.make_prediction(table_f_c)

*******************************************************************************************************************
# prints out a prediction in the form of the name assigned to the frequency table 
*******************************************************************************************************************
