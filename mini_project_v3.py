import Test
from Numberjack import *
from group_functions import *
from room_functions import *
from teacher_functions import *

# useless for the moment #
def sum_row_1_to_n(planning, row, n):
    Sum = 0
    for k in range(n):
        Sum += sum(planning[row][k])
    return Sum

# count the number of forced lectures before a tuto, exp #
def sum_forced_lectures(n,limit):
    mod = n % limit
    nbr = (n-mod)/limit
    return (mod,int(nbr))

# for course_y, tutorials/experiments can start only after x lectures at least
def exercises_only_after_x_lectures(course, lecture_list, exercise_list, nb_lec, x):
    y = find_index_lesson_list(lecture_list, course)
    z = find_index_lesson_list(exercise_list, course)
    return (x ,y ,z, nb_lec)

def get_model(N):
    slots = 17              # Max number of hours per week
    number_of_weeks = N     # Number of weeks in a year, for our test we put 10 weeks
    resource_per_room = 6   # Number of slots per week a room could contained
    limit_hours_course = 5  # leveling factor

    # Get a data set from Test.py
    course_list, teacher_list, group_list = Test.data_set(2)

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
    # TODO : need to know if experiment hours need CS_room -> precise it in course data ?
    # TODO : need to know if groups are in the same promotion or not for lectures room -> make a list promotion ?
    room_1 = {'name': "GEI 15", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'is_CS_room': False}
    room_2 = {'name': "GEI 13", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'is_CS_room': False}
    room_3 = {'name': "GEI 111", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True, 'is_CS_room': True}
    room_4 = {'name': "GEI 109", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True, 'is_CS_room': True}
    room_5 = {'name': "GEI 213", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'is_CS_room': False}

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

    # Specific constraints #

    # exercises start after X lectures #

    # format {course_list, index_of_course, lecture_list, tutorial_list, nbr_of_lec_before_start, limit_hours_course}
    # c : tuto/exp index in matrix, b : lect index in matrix, a : the tuto/exp start only after a lectures
    """
    (a, b, c) = exercises_only_after_x_lectures(course_list[1], lecture_list, tutorial_list, 6)
    if (a > limit_hours_course):
        (mod, nbr) = sum_forced_lectures(a, limit_hours_course)
        for i in range(nbr):
            model += (planning_lectures[b][i] == limit_hours_course)
            model += (planning_tutorials[c][i] == 0)

        model += (planning_lectures[b][nbr + 1] >= mod)
    else:
        model += (planning_lectures[b][0] >= a)
    """
    """
    # solution propre, mais qui ne trouve pas de solution #
    (a, b, c) = exercises_only_after_x_lectures(course_list[1], lecture_list, tutorial_list, 6)
    for i in range(number_of_weeks):
        model += ((planning_tutorials[c][i] == 0) or ((planning_tutorials[c][i] > 0) and (planning_lectures[b][range(i)] >= a)))
    """
    # format : {'course_list':course_list, 'lecture_list': lecture_list, 'tutorial_list': tutorial_list,'nb_lec_before_tut':6}

    (a, b, c, nb_lec) = exercises_only_after_x_lectures(course_list[1], lecture_list, tutorial_list,course_list[1]['lecture'], 6)
    middle = int(limit_hours_course*number_of_weeks*0.5)
    if ((a < middle) and (a<nb_lec)):
        for i in range(int(number_of_weeks*0.5)):
            model += (planning_tutorials[c][i] == 0)
        for i in range(int(number_of_weeks * 0.5),number_of_weeks):
            model += (planning_lectures[b][i] <= int((nb_lec-a)/(number_of_weeks*0.5)))

    # Group constraints #

    # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
    total_hours_group_list = []
    total_lecture_hours_group_list = []
    total_tutorial_hours_group_list = []
    total_experiment_hours_group_list = []

    for group_index in range(len(group_list)):

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
        total_lecture_hours_one_group = []
        total_tutorial_hours_one_group = []
        total_experiment_hours_one_group = []
        total_hours_one_group = []

        for week in range(number_of_weeks):

            hours_lectures, hours_tutorials, hours_experiments, hours_total = get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                                    planning_experiments)

            # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
            total_lecture_hours_one_group.append(hours_lectures)
            total_tutorial_hours_one_group.append(hours_tutorials)
            total_experiment_hours_one_group.append(hours_experiments)
            total_hours_one_group.append(hours_total)

            model += (hours_total <= slots)

        # Add details of one group in the groups' lists
        total_lecture_hours_group_list.append(total_lecture_hours_one_group)
        total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
        total_experiment_hours_group_list.append(total_experiment_hours_one_group)
        total_hours_group_list.append(total_hours_one_group)

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

    # ----------------- #
    # ----- Rooms ----- #
    # ----------------- #

    # Instantiate lists to know what rooms could be use for lecture/tutorial/experiment
    rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(rooms_list)

    # Instantiate union lists
    # union_lectures_tutorials : rooms that could be use for lectures or/and tutorials
    # union_lectures_experiments : rooms that could be use for lectures or/and experiments
    # union_tutorials_experiments : rooms that could be use for tutorials or/and experiments
    union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments = get_union_list_rooms_according_type_hours(rooms_list)

    # Instantiate lists containing total of lectures/tutorials/experiments hours per week
    total_hours_lecture = get_total_hours_week(total_lecture_hours_group_list) # total_lecture_hours_group_list should be modify, here, we don't take into account if groups are in the same promotion
    total_hours_tutorial = get_total_hours_week(total_tutorial_hours_group_list)
    total_hours_experiment = get_total_hours_week(total_experiment_hours_group_list)

    # Instantiate sum total of lectures/tutorials/experiments per week
    # total_hours_union_lecture_tutorial : sum total of lectures and tutorials
    # total_hours_union_lecture_experiment : sum total of lectures and experiments
    # total_hours_union_tutorial_experiment : sum total of tutorials and experiments
    total_hours_union_lecture_tutorial = get_total_hours_week([total_hours_lecture, total_hours_tutorial])
    total_hours_union_lecture_experiment = get_total_hours_week([total_hours_lecture, total_hours_experiment])
    total_hours_union_tutorial_experiment = get_total_hours_week([total_hours_tutorial, total_hours_experiment])

    # Constraint : Lecture should be done in a room that is for lectures
    model += is_lesson_hours_lt_resources(total_hours_lecture, len(rooms_lectures), resource_per_room)

    # Constraint : Tutorial should be done in a room that is for tutorials
    model += is_lesson_hours_lt_resources(total_hours_tutorial, len(rooms_tutorials), resource_per_room)

    # Constraint : Experiment should be done in a room that is for experiments
    model += is_lesson_hours_lt_resources(total_hours_experiment, len(rooms_experiments), resource_per_room)

    # Constraint : Lecture and tutorial should not be done in the same room at the same time
    model += is_lesson_hours_lt_resources(total_hours_union_lecture_tutorial, len(union_lectures_tutorials), resource_per_room)

    # Constraint : Lecture and experiment should not be done in the same room at the same time
    model += is_lesson_hours_lt_resources(total_hours_union_lecture_experiment, len(union_lectures_experiments), resource_per_room)

    # Constraint : Tutorial and experiment should not be done in the same room at the same time
    model += is_lesson_hours_lt_resources(total_hours_union_tutorial_experiment, len(union_tutorials_experiments), resource_per_room)

    # Constraint : They should not have more lectures,tutorials and experiments than available rooms
    model += is_lesson_hours_lt_resources(get_total_hours_week(total_hours_group_list), len(rooms_list), resource_per_room)


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

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
        total_hours_group_list = []
        total_lecture_hours_group_list = []
        total_tutorial_hours_group_list = []
        total_experiment_hours_group_list = []

        # print groups' hours
        for group_index in range(len(index_group_list)):
            out += ('\n\nGroup ' + str(group_index + 1) + ': \n')

            # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
            total_lecture_hours_one_group = []
            total_tutorial_hours_one_group = []
            total_experiment_hours_one_group = []
            total_hours_one_group = []

            for week in range(len(planning_lectures.col)):
                hours_lectures, hours_tutorials, hours_experiments, hours_total = get_group_hours(group_index, index_group_list, week, Solution(planning_lectures),
                                        Solution(planning_tutorials),
                                        Solution(planning_experiments))

                # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
                total_lecture_hours_one_group.append(hours_lectures)
                total_tutorial_hours_one_group.append(hours_tutorials)
                total_experiment_hours_one_group .append(hours_experiments)
                total_hours_one_group.append(hours_total)

            # Print details of the current group
            out += "Lecture" + str(total_lecture_hours_one_group)
            out += "\nTutorial" + str(total_tutorial_hours_one_group)
            out += "\nExperiments" + str(total_experiment_hours_one_group )
            out += "\n\nTotal" + str(total_hours_one_group)
            out += "\n\n"

            # Add details of one group in the groups' lists
            total_lecture_hours_group_list.append(total_lecture_hours_one_group)
            total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
            total_experiment_hours_group_list.append(total_experiment_hours_one_group)
            total_hours_group_list.append(total_hours_one_group)

        # print teachers' hours
        for teacher_index in range(len(index_teacher_list)):
            out += ('\n\nTeacher ' + str(teacher_index + 1) + ': \n')
            total_teacher_hours = []
            for week in range(len(planning_lectures.col)):
                hours = get_teacher_hours(teacher_index, index_teacher_list, week, Solution(planning_lectures),
                                          Solution(planning_tutorials), Solution(planning_experiments))
                total_teacher_hours.append(hours)
            out += str(total_teacher_hours)

        # ---------------------- #
        # ----- Rooms Test ----- #
        # ---------------------- #

        rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(rooms_list)
        # union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments =
        # get_union_list_rooms_according_type_hours(rooms_list)

        # Lists containing total of lectures/tutorials/experiments hours per week
        total_hours_lecture = get_total_hours_week(total_lecture_hours_group_list)
        total_hours_tutorial = get_total_hours_week(total_tutorial_hours_group_list)
        total_hours_experiment = get_total_hours_week(total_experiment_hours_group_list)

        # Lists containing sum total of lectures/tutorials/experiments per week
        total_hours_union_lecture_tutorial = get_total_hours_week([total_hours_lecture, total_hours_tutorial])
        total_hours_union_lecture_experiment = get_total_hours_week([total_hours_lecture, total_hours_experiment])
        total_hours_union_tutorial_experiment = get_total_hours_week([total_hours_tutorial, total_hours_experiment])

        out += "\n\n"
        out += "\n\n        # ---------------- ----- #"
        out += "\n\n        # ----- Rooms Test ----- #"
        out += "\n\n        # ---------------- ----- #"
        out += "\n\nTotal hours lecture: " + str(total_hours_lecture)
        out += "\nTotal hours tutorial: " + str(total_hours_tutorial)
        out += "\nTotal hours experiment: " + str(total_hours_experiment)
        out += "\n"
        out += "\n\nTotal hours lecture+tutorial: " + str(total_hours_union_lecture_tutorial)
        out += "\nTotal hours lecture+experiment: " + str(total_hours_union_lecture_experiment)
        out += "\nTotal hours tutorial+experiment: " + str(total_hours_union_tutorial_experiment)
        out += "\n"
        out += "\nResources max for lectures per week: " + str(resource_per_room*len(rooms_lectures))
        out += "\nResources max for tutorials per week: " + str(resource_per_room*len(rooms_tutorials))
        out += "\nResources max for experiments per week: " + str(resource_per_room*len(rooms_experiments))

    else:
        out = "No solution has been found !"

    return out


default = {'solver': 'Mistral2', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}

if __name__ == '__main__':
    param = input(default)
    print(solve(param))
