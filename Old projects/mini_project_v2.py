from Numberjack import *


def get_model (N):
    slots = 17  # Max number of hours per week
    number_of_weeks = N
    limit_hours_course = 5  # leveling factor

    # Format : [Lecture hours, Number of Experiments]
    course_1 = [40, 5]  # Maths
    course_2 = [30, 1]  # CS, in cs_rooms
    course_3 = [10, 5]  # Chemistry
    course_4 = [20, 0]  # English
    course_5 = [10, 0]  # ppi
    experiment_1 = 15  # CS classroom experiments

    course_list = [course_1, course_2, course_3, course_4, course_5]
    experiment_list = [experiment_1]

    # Groups are represented by a list of the courses they are taking
    group1 = [course_1, course_2, course_3, course_4, experiment_1]
    group2 = [course_1, course_2, course_3, course_5, experiment_1]
    group_list = [group1, group2]

    planning_course = Matrix(len(course_list), number_of_weeks, 0, limit_hours_course)
    planning_experiments = Matrix(len(experiment_list), number_of_weeks, 1, limit_hours_course) #pourquoi le min est 1 ?

    model = Model(

        # Courses
        # On the matrix, each row represents a course, and each column represent a week.
        # We then want the sum of a row to be equal to the corresponding course's total hours
        # and the sum of a column to be less than the max hours of class per week
        [Sum(row) == hours[0] for (row, hours) in zip(planning_course.row, course_list)],
        [Sum(col) < slots for col in planning_course.col],

        # TP
        [Sum(j > 1 for j in row) >= hours[1] for (row, hours) in zip(planning_course.row, course_list)],

        # experiments
        [Sum(row) == hours for (row, hours) in zip(planning_experiments.row, experiment_list)],
        [Sum(col) < slots // 2 for col in planning_experiments.col]
    )

    return planning_course, planning_experiments, model


def solve(param):
    planning_course, planning_experiments, model = get_model(param['N'])
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
        out = '\nCourses: \n' + str(planning_course)
        out += '\n\nClassroom Experiments: \n' + str(planning_experiments)
    out += ('\n\nNodes: ' + str(solver.getNodes()))
    return out


default = {'solver': 'Mistral', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}


if __name__ == '__main__':
    param = input(default)
    print(solve(param))
