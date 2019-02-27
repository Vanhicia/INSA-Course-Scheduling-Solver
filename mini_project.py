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
    course_2 = VarArray(60,weeks)  # CS, in cs_rooms
    course_3 = VarArray(10,weeks)  # Chemistry
    course_4 = VarArray(20,weeks)  # English
    course_5 = VarArray(10,weeks)  # ppi

    course_list = [course_1, course_2, course_3, course_4, course_5]

    #Definition of constraints
    model = Model()
    for i in range(10): #Constraint on number of courses in a week : slots
        model += card_sum(course_list,i) <= slots


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
