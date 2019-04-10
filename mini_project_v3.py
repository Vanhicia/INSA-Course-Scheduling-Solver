from Numberjack import *


# parameters: lecture/tutorial/experiment list, course
# return the index of the course in the lecture/tutorial/experiment list
def find_index_lesson_list(lesson_list, course):
    k = 0
    for lesson in lesson_list:
        if lesson[0] == course['name']:
            return k
        k += 1


# parameters: teacher, 'lecture'/'tutorial'/'experiment', course list
# return the index list of ?
def list_index_lesson(teacher, lesson_type, lesson_list):
    index_list = []

    if lesson_type == 'lecture':
        type_gp_nb = 'lecture_gp_nb'
    elif lesson_type == 'tutorial':
        type_gp_nb = 'tutorial_gp_nb'
    elif lesson_type == 'experiment':
        type_gp_nb = 'experiment_gp_nb'
    else:
        raise ValueError("'lesson_type' can only be either 'lecture','tutorial' or 'experiment'")

    for course in teacher:
        if course[type_gp_nb] > 0:
            index_list.append({'index': find_index_lesson_list(lesson_list, course['course']),
                               'gp_nb': course[type_gp_nb]})

    return index_list


# get teacher hours for a specific week
# Format : get_teacher_hours( teacher id, list of teachers by id, week, plannings * 3 )
def get_teacher_hours(teacher_index, index_teacher_list, week, planning_lectures, planning_tutorials,
                      planning_experiments):
    hours = 0
    teacher = index_teacher_list[teacher_index]

    for lecture in teacher['index_lecture_list']:
        hours += lecture['gp_nb'] * planning_lectures[lecture['index']][week]
    for tutorial in teacher['index_tutorial_list']:
        hours += tutorial['gp_nb'] * planning_tutorials[tutorial['index']][week]
    for experiment in teacher['index_experiment_list']:
        hours += experiment['gp_nb'] * 2 * planning_experiments[experiment['index']][week]

    return hours


def list_index_lesson_group(group, lesson_type, lesson_list):
    index_list = []
    for course in group['course_list']:
        if course[lesson_type] > 0:
            index_list.append({'index': find_index_lesson_list(lesson_list, course), 'number_of': course[lesson_type]})

    return index_list


def get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                    planning_experiments):
    hours = 0
    group = index_group_list[group_index]

    for lecture in group['index_lecture_list']:
        hours += planning_lectures[lecture['index']][week]
    for tutorial in group['index_tutorial_list']:
        hours += planning_tutorials[tutorial['index']][week]
    for experiment in group['index_experiment_list']:
        hours += 2 * planning_experiments[experiment['index']][week]

    return hours


def get_model(N):
    slots = 17  # Max number of hours per week
    number_of_weeks = N
    limit_hours_course = 5  # leveling factor

    # Courses #

    # Format : {name:bla, lecture : 0, tutorial:0, experiment:0}
    course_1 = {'name': 'math', 'lecture': 40, 'tutorial': 0, 'experiment': 0}
    course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 15}
    course_3 = {'name': 'Chemistry', 'lecture': 10, 'tutorial': 0, 'experiment': 0}
    course_4 = {'name': 'English', 'lecture': 20, 'tutorial': 0, 'experiment': 0}
    course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial': 0, 'experiment': 0}

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

    planning_lectures = Matrix(len(lecture_list), number_of_weeks, 0, limit_hours_course)
    planning_tutorials = Matrix(len(tutorial_list), number_of_weeks, 0, limit_hours_course)
    planning_experiments = Matrix(len(experiment_list), number_of_weeks, 0, limit_hours_course)

    # Groups #

    group_1 = {'name': "4IR-A", 'course_list': [course_1, course_2]}
    group_2 = {'name': "4IR-A", 'course_list': [course_2, course_3]}
    group_3 = {'name': "4IR-A", 'course_list': [course_4, course_5]}
    group_list = [group_1, group_2, group_3]

    index_group_list = []
    for group in group_list:
        index_group_list.append({'index_lecture_list': list_index_lesson_group(group, 'lecture', lecture_list),
                                 'index_tutorial_list': list_index_lesson_group(group, 'tutorial', tutorial_list),
                                 'index_experiment_list': list_index_lesson_group(group, 'experiment', experiment_list)})

    # Teachers #

    # They are represented by the list of the courses which they teach
    # Format [{course:course_n , lecture_gp_nb: 0, tutorial_gp_nb: 0, experiment_gp_nb: 0},...]
    teacher_1 = [{'course': course_1, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0},
                {'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 1}]
    teacher_2 = [{'course': course_2, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 0}]
    teacher_3 = [{'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 2}]
    teacher_4 = [{'course': course_3, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]
    teacher_5 = [{'course': course_4, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]
    teacher_6 = [{'course': course_5, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]

    teacher_list = [teacher_1, teacher_2, teacher_3, teacher_4, teacher_5, teacher_6]
    teacher_max_hours = 12  # maximum slot number for a teacher per week

    index_teacher_list = []
    for teacher in teacher_list:
        index_teacher_list.append({'index_lecture_list': list_index_lesson(teacher, 'lecture', lecture_list),
                                  'index_tutorial_list': list_index_lesson(teacher, 'tutorial', tutorial_list),
                                   'index_experiment_list': list_index_lesson(teacher, 'experiment', experiment_list)})

    model = Model(
        # Lectures
        # On the matrix, each row represents a lecture, and each column represent a week.
        # We then want the sum of a row to be equal to the corresponding lecture total hours,
        # and the sum of a column to be less than the max hours of class per week
        [Sum(row) == hours[1] for (row, hours) in zip(planning_lectures.row, lecture_list)],

        # tutorials
        [Sum(row) == hours[1] for (row, hours) in zip(planning_tutorials.row, tutorial_list)],

        # experiments
        [Sum(row) == hours[1] for (row, hours) in zip(planning_experiments.row, experiment_list)],

        # Sum of hours per week
        [(Sum(lect) + Sum(tuto) + Sum(exp)*2) < slots for (lect, tuto, exp)
            in zip(planning_lectures.col, planning_tutorials.col, planning_experiments.col)],

    )

    # group constraints

    for group_index in range(len(group_list)):
        for week in range(number_of_weeks):
            hours = get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials, planning_experiments)
            model += (hours <= slots)

    print('\n')

    # teacher constraints
    for teacher_index in range(len(teacher_list)):
        for week in range(number_of_weeks):
            hours = get_teacher_hours(teacher_index, index_teacher_list, week, planning_lectures, planning_tutorials, planning_experiments)
            model += (hours <= teacher_max_hours)

    # specific teacher constraints

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

    return planning_lectures, planning_experiments, planning_tutorials, index_teacher_list, index_group_list, model


def solve(param):
    planning_lectures, planning_experiments, planning_tutorials, index_teacher_list, index_group_list, model = get_model(param['N'])
    solver = model.load(param['solver'])
    solver.setVerbosity(param['verbose'])
    solver.setHeuristic(param['var'], param['val'], param['rand'])
    solver.setTimeLimit(param['cutoff'])

    if param['restart'] == 'yes':
        solver.solveAndRestart()
    else:
        solver.solve()

    out = ''
    if solver.is_sat():
        out = '\nLectures: \n' + str(planning_lectures)
        out += '\n\nTutorials: \n' + str(planning_tutorials)
        out += '\n\nClassroom Experiments: \n' + str(planning_experiments)

        total_week_group = [(sum(lect) + sum(exp) * 2 + sum(tuto)) for (lect, exp, tuto) in zip(Solution(planning_lectures.col), Solution(planning_experiments.col), Solution(planning_tutorials.col))]
        # total_week_group = [0,0,0,0,0,0,0,0,0,0]
        # for i in range(len(planning_lectures.col)):
        #     for j in range(len(planning_lectures.row)):
        #         total_week_group[i] += (planning_lectures[j][i].get_value())

        out += ('\n\nTotal for each group: \n' + str(total_week_group))
        out += ('\n\nNodes: ' + str(solver.getNodes()))

        # print teachers' hours
        for teacher_index in range(len(index_teacher_list)):
            out += ('\n\nTeacher ' + str(teacher_index+1) + ': \n')
            total_teacher_hours = []
            for week in range(len(planning_lectures.col)):
                hours = get_teacher_hours(teacher_index, index_teacher_list, week, Solution(planning_lectures),
                                          Solution(planning_tutorials), Solution(planning_experiments))
                total_teacher_hours.append(hours)
            out += str(total_teacher_hours)

        for group_index in range(len(index_group_list)):
            out += ('\n\nGroup ' + str(group_index+1) + ': \n')
            total_group_hours = []
            for week in range(len(planning_lectures.col)):
                hours = get_group_hours(group_index, index_group_list, week, Solution(planning_lectures), Solution(planning_tutorials),
                                Solution(planning_experiments))
                total_group_hours.append(hours)
            out += str(total_group_hours)
    else:
        out = "No solution has been found !"

    return out


default = {'solver': 'Mistral2', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}


if __name__ == '__main__':
    param = input(default)
    print(solve(param))
