import Test
from Numberjack import *
from group_functions import *
from room_functions import *
from teacher_functions import *


def sum_row_1_to_n(planning, row, n):
    Sum = 0
    for k in range(n):
        Sum += sum(planning[row][k])
    return Sum


def get_model(N):
    slots = 17  # Max number of hours per week
    number_of_weeks = N
    resource_per_room = 3
    limit_hours_course = 5  # leveling factor

    #Get a data set from Test.py
    course_list,teacher_list,group_list = Test.data_set(2)

    lecture_list = []
    tutorial_list = []
    experiment_list = []

    for course in course_list:
        if course['lecture'] > 0:
            lecture_list += [[course['name'], course['lecture']]]
        if course['tutorial'] > 0:
            tutorial_list += [[course['name'], course['tutorial']]]
        if course['experiment'] > 0:
            experiment_list += [[course['name'], course['experiment']]]

    # planning for each lesson type, represented by a matrix
    planning_lectures = Matrix(len(lecture_list), number_of_weeks, 0, limit_hours_course)
    planning_tutorials = Matrix(len(tutorial_list), number_of_weeks, 0, limit_hours_course)
    planning_experiments = Matrix(len(experiment_list), number_of_weeks, 0, limit_hours_course)


    index_group_list = []
    for group in group_list:
        index_group_list.append({'index_lecture_list': list_index_lesson_group(group, 'lecture', lecture_list),
                                 'index_tutorial_list': list_index_lesson_group(group, 'tutorial', tutorial_list),
                                 'index_experiment_list': list_index_lesson_group(group, 'experiment', experiment_list)})

    teacher_max_hours = 12  # maximum slot number for a teacher per week

    index_teacher_list = []
    for teacher in teacher_list:
        index_teacher_list.append({'index_lecture_list': list_index_lesson(teacher, 'lecture', lecture_list),
                                   'index_tutorial_list': list_index_lesson(teacher, 'tutorial', tutorial_list),
                                   'index_experiment_list': list_index_lesson(teacher, 'experiment', experiment_list)})

    # Rooms #
    room_1 = {'name': "GEI 15", 'is_CS_room': False}
    room_2 = {'name': "GEI 13", 'is_CS_room': False}
    room_3 = {'name': "GEI 111", 'is_CS_room': True}
    room_4 = {'name': "GEI 109", 'is_CS_room': True}
    room_5 = {'name': "GEI 213", 'is_CS_room': False}

    rooms_list = [room_1, room_2, room_3, room_4, room_5]


    # Model : add all the constraints #

    model = Model()

    # Lectures
    # On the matrix, each row represents a lecture, and each column represent a week.
    # We then want the sum of a row to be equal to the corresponding lecture total hours,
    # and the sum of a column to be less than the max hours of class per week
    model += [Sum(row) == hours[1] for (row, hours) in zip(planning_lectures.row, lecture_list)]

    # tutorials
    model += [Sum(row) == hours[1] for (row, hours) in zip(planning_tutorials.row, tutorial_list)]

    # experiments
    model += [Sum(row) == hours[1] for (row, hours) in zip(planning_experiments.row, experiment_list)]

    # Sum of hours per week
    # should be deleted ???
    model += [(Sum(lect) + Sum(tuto) + Sum(exp) * 2) < slots for (lect, tuto, exp)
     in zip(planning_lectures.col, planning_tutorials.col, planning_experiments.col)]

    # Constraints between the different lesson types #

    # for course_2, tutorials can start only after 3 lectures at least
    for i in range(number_of_weeks):
        model += (planning_tutorials[0][i] <= sum_row_1_to_n(planning_lectures, 1, i + 1) * 3)

    # Group constraints #

    for group_index in range(len(group_list)):
        for week in range(number_of_weeks):
            hours_lectures, hours_tutorials, hours_experiments, hours_total = get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                                    planning_experiments)
            model += (hours_total <= slots)

    # Teacher constraints #

    for teacher_index in range(len(teacher_list)):
        for week in range(number_of_weeks):
            hours = get_teacher_hours(teacher_index, index_teacher_list, week, planning_lectures, planning_tutorials,
                                      planning_experiments)
            model += (hours <= teacher_max_hours)

    # Specific teacher constraints #

    # teacher_1 is not available the first week
    teacher_index = 0
    max_hours = 0
    hours = get_teacher_hours(teacher_index, index_teacher_list, 0, planning_lectures, planning_tutorials,
                              planning_experiments)
    model += (hours <= max_hours)

    # teacher_6 is not available the fourth week
    teacher_index = 5
    max_hours = 0
    hours = get_teacher_hours(teacher_index, index_teacher_list, 3, planning_lectures, planning_tutorials,
                              planning_experiments)
    model += (hours <= max_hours)

    return planning_lectures, planning_experiments, planning_tutorials, index_teacher_list, index_group_list, rooms_list, resource_per_room, model


def solve(param):
    planning_lectures, planning_experiments, planning_tutorials, index_teacher_list, index_group_list, rooms_list, resource_per_room, model = get_model(param['N'])
    solver = model.load(param['solver'])
    solver.setVerbosity(param['verbose'])
    solver.setHeuristic(param['var'], param['val'], param['rand'])
    solver.setTimeLimit(param['cutoff'])

    if param['restart'] == 'yes':
        solver.solveAndRestart()
    else:
        solver.solve()

    # if a solution has been found
    if solver.is_sat():

        # print plannings
        out = '\nLectures: \n' + str(planning_lectures)
        out += '\n\nTutorials: \n' + str(planning_tutorials)
        out += '\n\nClassroom Experiments: \n' + str(planning_experiments)

        # out += ('\n\nNodes: ' + str(solver.getNodes()))

        total_hours_group_list =[]
        # print groups' hours
        for group_index in range(len(index_group_list)):
            out += ('\n\nGroup ' + str(group_index + 1) + ': \n')
            total_group_hours_lectures = []
            total_group_hours_tutorials = []
            total_group_hours_experiments = []
            total_group_hours_total = []
            for week in range(len(planning_lectures.col)):
                hours_lectures, hours_tutorials, hours_experiments, hours_total = get_group_hours(group_index, index_group_list, week, Solution(planning_lectures),
                                        Solution(planning_tutorials),
                                        Solution(planning_experiments))
                total_group_hours_lectures.append(hours_lectures)
                total_group_hours_tutorials.append(hours_tutorials)
                total_group_hours_experiments.append(hours_experiments)
                total_group_hours_total.append(hours_total)

            out += "Lecture" + str(total_group_hours_lectures)
            out += "\nTutorial" + str(total_group_hours_tutorials)
            out += "\nExperiments" + str(total_group_hours_experiments)
            out += "\n\nTotal" + str(total_group_hours_total)
            out += "\n\n"

            total_hours_group_list.append(total_group_hours_total)

        # print teachers' hours
        for teacher_index in range(len(index_teacher_list)):
            out += ('\n\nTeacher ' + str(teacher_index + 1) + ': \n')
            total_teacher_hours = []
            for week in range(len(planning_lectures.col)):
                hours = get_teacher_hours(teacher_index, index_teacher_list, week, Solution(planning_lectures),
                                          Solution(planning_tutorials), Solution(planning_experiments))
                total_teacher_hours.append(hours)
            out += str(total_teacher_hours)

        out += '\n\nTotal hours per week:\n' + str(get_total_hours_week(total_hours_group_list))
        out += '\n\nEnough resources ? :\n' + str(is_lesson_hours_lt_resources(get_total_hours_week(total_hours_group_list), len(rooms_list), resource_per_room))
    else:
        out = "No solution has been found !"

    return out


default = {'solver': 'Mistral2', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}

if __name__ == '__main__':
    param = input(default)
    print(solve(param))