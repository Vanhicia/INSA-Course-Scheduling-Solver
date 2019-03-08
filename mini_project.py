from Numberjack import *
from collections import Counter

def card_sum(l, n): #Sum cardinality of all courses for a week n
    tmp=0
    for c in l:
        tmp += Cardinality(c,n)
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
    pw_1 = VarArray(30,weeks)  # computer science practical works

    course_list = [course_1, course_2, course_3, course_4, course_5, pw_1]
    #Definition of constraints
    model = Model()
    for i in range(10): #Constraint on number of courses in a week : slots
        model += card_sum(course_list,i) <= slots
        model += Cardinality(course_list[5], i) <= 6  #Constraint on number of (the same) pw in a week : 3 * 2 hours
        #load_balancing = card_sum(course_list,i)
    for j in range (0, 30, 2):
        model += course_list[5][j] == course_list[5][j+1]



    #Solver parameters
    solver = model.load("Mistral2")
    solver.setVerbosity(0)

    #Solve and print
    solver.solve()
    print("Solved")
    tmp=[]
    for course in course_list:
        print(course)
        tmp+= course
    print()

    sol = solver.get_solution()
    print(dict(sorted(Counter(sol).items())))

if __name__ == '__main__':
    #param = input(default)
    #print(solve(param))
    mini_project()
