from Numberjack import *
from collections import Counter

def card_sum(l, n): #Sum cardinality of all courses for a week n
    tmp=0
    for c in l:
        tmp += Cardinality(c,n)
    return tmp

def card_sum_lab(l, n): #Sum cardinality of all labs for a week n
    tmp=0
    for c in l:
        tmp += 2*Cardinality(c,n)
    return tmp

def mini_project():
    #Definition of constants
    weeks = 10
    groups = 2
    classrooms = 2
    cs_rooms = 1
    rooms_slots = 20
    slots = 17          #Slots per week

    #Definition of variables : courses

    course_1 = VarArray(40,weeks)  # Maths
    course_2 = VarArray(30,weeks)  # CS, in cs_rooms
    course_3 = VarArray(10,weeks)  # Chemistry
    course_4 = VarArray(20,weeks)  # English
    course_5 = VarArray(10,weeks)  # ppi
    lab_1 = VarArray(15,weeks)  # CS labs

    course_list = [course_1, course_2, course_3, course_4, course_5]
    lab_list =[lab_1]


    #Definition of constraints
    model = Model()
    for i in range(weeks): #Constraint on number of courses in a week : slots
        model += (card_sum(course_list,i) +card_sum_lab(lab_list,i))<= slots
        #to limit the number of lab in a week : 8h/week max
        model += card_sum_lab(lab_list, i) <= (slots//2)


    #Solver parameters
    solver = model.load("Mistral2")
    solver.setVerbosity(0)
    #Solve and print
    solver.solve()
    print("Solved")
    i=1
    for course in course_list:
        print("course_",i)
        i+=1
        #ca ne marche pas je sais pas pk
        #print(dict(sorted(Counter(course).items())))
        print(course)
    print()

    j = 1
    for lab in lab_list:
        print("lab_", j)
        print(lab)
    print()

    print("number of courses/week :")
    sol = solver.get_solution()
    print(dict(sorted(Counter(sol).items())))
    print()
if __name__ == '__main__':
    #param = input(default)
    #print(solve(param))
    mini_project()
