from Numberjack import *
from teacher_functions import *
from group_functions import *
from room_functions import *

def sum_row_1_to_n(planning, row, n):
    Sum = 0
    for k in range(n):
        Sum += sum(planning[row][k])
    return Sum


def get_model(N):
    slots = 17  # Max number of hours per week
    number_of_weeks = N
    number_of_rooms = 10
    resource_per_room = 2
    limit_hours_course = 5  # leveling factor

    # Courses #

    # Format : {name:bla, lecture : 0, tutorial:0, experiment:0}
    course_1 = {'name': 'math', 'lecture': 40, 'tutorial': 0, 'experiment': 0}
    course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 15}
    course_3 = {'name': 'Chemistry', 'lecture': 10, 'tutorial': 0, 'experiment': 0}
    course_4 = {'name': 'English', 'lecture': 20, 'tutorial': 0, 'experiment': 0}
    course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial': 0, 'experiment': 0}

    # Course list and different lesson type lists
    course_list = [course_1, course_2, course_3, course_4, course_5]
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

    # Groups #

    # Groups are represented by their name and their course list
    # Format: {'name': "gpA", 'course_list': [course_1, course_2]}
    group_1 = {'name': "4IR-A", 'course_list': [course_1, course_2]}
    group_2 = {'name': "4IR-B", 'course_list': [course_2, course_3]}
    group_3 = {'name': "4IR-C", 'course_list': [course_4, course_5]}
    group_list = [group_1, group_2, group_3]

    index_group_list = []
    for group in group_list:
        index_group_list.append({'index_lecture_list': list_index_lesson_group(group, 'lecture', lecture_list),
                                 'index_tutorial_list': list_index_lesson_group(group, 'tutorial', tutorial_list),
                                 'index_experiment_list': list_index_lesson_group(group, 'experiment',
                                                                                  experiment_list)})

    # Teachers #

    # Teachers are represented by the list of the courses which they teach
    # Format: {'name':"Michel Dumont", 'course_list' : [{course:course_n , lecture_gp_nb: 0, tutorial_gp_nb: 0, experiment_gp_nb: 0},...]}
    teacher_1 = {'name': "Michel Dumont", 'course_list': [{'course': course_1, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0},
                 {'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 1}]}
    teacher_2 = {'name': "Hélène Michou", 'course_list': [{'course': course_2, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 0}]}
    teacher_3 = {'name': "Benoit Jardin", 'course_list': [{'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 2}]}
    teacher_4 = {'name': "Kate Stuart", 'course_list': [{'course': course_3, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
    teacher_5 = {'name': "Hervé Vieux", 'course_list': [{'course': course_4, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
    teacher_6 = {'name': "Christiane Colin", 'course_list': [{'course': course_5, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}

    teacher_list = [teacher_1, teacher_2, teacher_3, teacher_4, teacher_5, teacher_6]
    teacher_max_hours = 12  # maximum slot number for a teacher per week

    index_teacher_list = []
    for teacher in teacher_list:
        index_teacher_list.append({'index_lecture_list': list_index_lesson(teacher, 'lecture', lecture_list),
                                   'index_tutorial_list': list_index_lesson(teacher, 'tutorial', tutorial_list),
                                   'index_experiment_list': list_index_lesson(teacher, 'experiment', experiment_list)})

    # Model : add all the constraints #

    model = Model()

    # Constraints between the different lesson types #

    # for course_2, tutorials can start only after 3 lectures at least
    for i in range(number_of_weeks):
        model += (planning_tutorials[0][i] <= sum_row_1_to_n(planning_lectures, 1, i + 1) * 3)

    # Group constraints #

    for group_index in range(len(group_list)):
        for week in range(number_of_weeks):
            hours = get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                                    planning_experiments)
            model += (hours <= slots)

    # Teacher constraints #

    for teacher_index in range(len(teacher_list)):
        for week in range(number_of_weeks):
            hours = get_teacher_hours(teacher_index, index_teacher_list, week, planning_lectures, planning_tutorials,
                                      planning_experiments)
            model += (hours <= teacher_max_hours)

    # Specific teacher constraints #

    # teacher_1 is not available the first week
    teacher_index = teacher_list.index(teacher_1)
    max_hours = 0
    hours = get_teacher_hours(teacher_index, index_teacher_list, 0, planning_lectures, planning_tutorials,
                              planning_experiments)
    model += (hours <= max_hours)

    # teacher_6 is not available the fourth week
    teacher_index = teacher_list.index(teacher_6)
    max_hours = 0
    hours = get_teacher_hours(teacher_index, index_teacher_list, 3, planning_lectures, planning_tutorials,
                              planning_experiments)
    model += (hours <= max_hours)

    return planning_lectures, planning_experiments, planning_tutorials, index_teacher_list, index_group_list, number_of_rooms, resource_per_room, model


def solve(param):
    planning_lectures, planning_experiments, planning_tutorials, index_teacher_list, index_group_list, number_of_rooms, resource_per_room, model = get_model(param['N'])
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

        out += ('\n\nNodes: ' + str(solver.getNodes()))

        total_hours_group_list =[]
        # print groups' hours
        for group_index in range(len(index_group_list)):
            out += ('\n\nGroup ' + str(group_index + 1) + ': \n')
            total_group_hours = []
            for week in range(len(planning_lectures.col)):
                hours = get_group_hours(group_index, index_group_list, week, Solution(planning_lectures),
                                        Solution(planning_tutorials),
                                        Solution(planning_experiments))
                total_group_hours.append(hours)
            out += str(total_group_hours)
            total_hours_group_list.append(total_group_hours)

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
        out += '\n\nEnough resources ? :\n' + str(is_lesson_hours_lt_resources(get_total_hours_week(total_hours_group_list), number_of_rooms, resource_per_room))
        out += '\n\n'+ str(index_group_list)
    else:
        out = "No solution has been found !"

    return out


default = {'solver': 'Mistral2', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}

if __name__ == '__main__':
    param = input(default)
    print(solve(param))