from Numberjack import *


def get_model (N):
    slots = 17
    number_of_weeks = N
    limit_hours_course = 5  # leveling factor

    #  Format : [Total hours, Number of labs (TP) ]
    course_1 = [40, 5]  # Maths
    course_2 = [30, 1]  # CS, in cs_rooms
    course_3 = [10, 5]  # Chemistry
    course_4 = [20, 0]  # English
    course_5 = [10, 0]  # ppi
    lab_1 = 15  # CS labs

    course_list = [course_1, course_2, course_3, course_4, course_5]
    lab_list = [lab_1]

    planning_course = Matrix(len(course_list), number_of_weeks, 0, limit_hours_course)
    planning_labs = Matrix(len(lab_list), number_of_weeks, 1, limit_hours_course)

    model = Model(

        # Courses
        [Sum(row) == hours[0] for (row, hours) in zip(planning_course.row, course_list)],
        [Sum(col) < slots for col in planning_course.col],

        # TP
        [Sum(j > 1 for j in row) >= hours[1] for (row, hours) in zip(planning_course.row, course_list)],

        # Labs
        [Sum(row) == hours for (row, hours) in zip(planning_labs.row, lab_list)],
        [Sum(col) < slots // 2 for col in planning_labs.col]
    )

    return planning_course, planning_labs, model


def solve(param):
    planning_course, planning_labs, model = get_model(param['N'])
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
        out += '\n\nLabs: \n' + str(planning_labs)
    out += ('\n\nNodes: ' + str(solver.getNodes()))
    return out


default = {'solver': 'Mistral', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}


if __name__ == '__main__':
    param = input(default)
    print(solve(param))
