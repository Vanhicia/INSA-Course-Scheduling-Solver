from Numberjack import *


def get_model (N):
    slots = 17  # Max number of hours per week
    number_of_weeks = N
    limit_hours_course = 5  # leveling factor

    # Format : {name:bla, lecture : 0, tutorial:0, experiment:0}
    course_1 = {'name': 'math', 'lecture': 40, 'tutorial':0, 'experiment': 0}
    course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 15}
    course_3 = {'name': 'Chemistry', 'lecture': 10, 'tutorial':0, 'experiment': 0}
    course_4 = {'name': 'English', 'lecture': 20, 'tutorial':0, 'experiment': 0}
    course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial':0, 'experiment': 0}

    course_list = [course_1, course_2, course_3, course_4, course_5]
    lecture_list = []
    tutorial_list = []
    experiment_list = []

    group_1 = {'name': '4IR-A'}
    group_2 = {'name': '4IR-B'}
    group_3 = {'name': '4IR-C'}
    group_list = [group_1, group_2, group_3]

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

    model = Model(
        # Lectures
        # On the matrix, each row represents a lecture, and each column represent a week.
        # We then want the sum of a row to be equal to the corresponding lecture total hours,
        # and the sum of a column to be less than the max hours of class per week
        [Sum(row) == hours[1] for (row, hours) in zip(planning_lectures.row, lecture_list)],

        # experiments
        [Sum(row) == hours[1] for (row, hours) in zip(planning_experiments.row, experiment_list)],

        # tutorials
        [Sum(row) == hours[1] for (row, hours) in zip(planning_tutorials.row, tutorial_list)],

        # Sum of hours per week
        [(Sum(lect) + Sum(exp)*2 + Sum(tuto)) < slots for (lect, exp, tuto) in zip(planning_lectures.col, planning_experiments.col, planning_tutorials.col)],

    )

    return planning_lectures, planning_experiments, planning_tutorials, model


def solve(param):
    planning_lectures, planning_experiments, planning_tutorials, model = get_model(param['N'])
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
        out += '\n\nClassroom Experiments: \n' + str(planning_experiments)
        out += '\n\nTutorials: \n' + str(planning_tutorials)

        total_week_group = [(sum(lect) + sum(exp) * 2 + sum(tuto)) for (lect, exp, tuto) in zip(Solution(planning_lectures.col), Solution(planning_experiments.col), Solution(planning_tutorials.col))]
        # total_week_group = [0,0,0,0,0,0,0,0,0,0]
        # for i in range(len(planning_lectures.col)):
        #     for j in range(len(planning_lectures.row)):
        #         total_week_group[i] += (planning_lectures[j][i].get_value())

        out += ('\n\nTotal for each group: \n' + str(total_week_group))
        out += ('\n\nNodes: ' + str(solver.getNodes()))
    return out


default = {'solver': 'Mistral2', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}


if __name__ == '__main__':
    param = input(default)
    print(solve(param))
