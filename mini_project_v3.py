import Test
from Numberjack import *
from group_functions import *
from room_functions import *
from teacher_functions import *
from course_functions import *


class Planning:

    def __init__(self):
        self.planning_lectures = None
        self.planning_tutorials_group = None
        self.planning_experiments_group = None
        self.planning_tutorials_teacher = None
        self.planning_experiments_teacher = None
        self.index_teacher_list = None
        self.index_group_list = None

        self.rooms_list = None
        self.resource_per_room = None

        # Added for printing
        self.group_list = None
        self.lecture_list = None
        self.tutorial_list_per_group = None
        self.experiment_list_per_group = None
        self.N = None

    def print_csv(self, filename):
        file = open(filename, "w")
        cpt = 0
        for grp in self.index_group_list:
            file.write(self.group_list[cpt]['name']+"\n")

            total = [0]*self.N

            for week in range(self.N):
                file.write(";Semaine "+str(week+1))

            for cs in grp['index_lecture_list']:
                file.write("\n CM : "+self.lecture_list[cs['index']][0])
                for wk in range(self.N): #TODO Change to use parameter
                    total[wk] += int(str(self.planning_lectures[cs['index']][wk]))
                    file.write(";"+str(self.planning_lectures[cs['index']][wk]))

            for cs in grp['index_tutorial_list']:
                file.write("\n TD : "+self.tutorial_list_per_group[cpt][cs['index']][0])
                for wk in range(self.N): #TODO Change to use parameter
                    total[wk] += int(str(self.planning_tutorials_group[cpt][cs['index']][wk]))
                    file.write(";"+str(self.planning_tutorials_group[cpt][cs['index']][wk]))

            for cs in grp['index_experiment_list']:
                file.write("\n TP : "+self.experiment_list_per_group[cpt][cs['index']][0])
                for wk in range(self.N): #TODO Change to use parameter
                    total[wk] += (int(str(self.planning_experiments_group[cpt][cs['index']][wk]))*2)
                    file.write(";"+str(int(str(self.planning_experiments_group[cpt][cs['index']][wk]))*2))

            file.write("\n Total ")
            for tot in total:
                file.write(";"+str(tot))
            file.write("\n\n")
            cpt += 1
        # TODO csv for teacher part
        file.close()

    def get_model(self, N):
        # --------------------------------------------------------------------------------------------------- #
        # ------------------------------------------ Initialization ----------------------------------------- #
        # --------------------------------------------------------------------------------------------------- #

        slots = 17              # Max number of hours per week
        number_of_weeks = N     # Number of weeks in a year, for our test we put 10 weeks
        resource_per_room = 27   # Number of slots per week a room could contained
        limit_hours_course = 5  # leveling factor

        # Get a data set from Test.py
        course_list, teacher_list, group_list, rooms_list = Test.data_set(2)

        # ----------------------------------- Course initialization ------------------------------------ #

        # Create lecture/tutorial/experiment list
        # One element contains the name of the subject + the number of lectures/tutorials/experiments
        lecture_list = []
        tutorial_list_per_group = []
        experiment_list_per_group = []

        # ---------------------------------- Initialize planning_lecture ----------------------------------- #

        for course in course_list:
            # some courses have only lectures, only tutorials or only experiments,
            # so we need to check if we have lectures in the current course
            if course['lecture'] > 0:
                lecture_list += [[course['name'], course['lecture']]]

        # Matrix representing planning for lecture lessons
        planning_lectures = Matrix(len(lecture_list), number_of_weeks, 0, limit_hours_course)

        # --------------------- Initialize planning tutorial and experiment for groups --------------------- #

        # Lists containing matrix representing planning for tutorial/experiment per group
        planning_tutorials_per_group = []
        planning_experiments_per_group = []

        # a list is created, which contains for each group the promotion,
        # and a sublist for each type of class (lecture, tutorial, and experiment).
        # each sublist presents every course followed by the group,
        # and a number of hours for the present type of class for the present course
        index_group_list = []

        for group in group_list:
            tutorial_list_one_group = []
            experiment_list_one_group = []
            for course in group['course_list']:
                if course['tutorial'] > 0:  # The current group has tutorials' current course
                    tutorial_list_one_group += [[course['name'], course['tutorial']]]
                if course['experiment'] > 0:  # The current group has experiments' current course
                    experiment_list_one_group += [[course['name'], course['experiment']]]

            index_group_list.append({'promo': group['promo'],
                                     'index_lecture_list': list_index_lesson_group(group, 'lecture', lecture_list),
                                     'index_tutorial_list': list_index_lesson_group(group, 'tutorial', tutorial_list_one_group),
                                     'index_experiment_list': list_index_lesson_group(group, 'experiment', experiment_list_one_group)})
            # Tutorials
            tutorial_list_per_group.append(tutorial_list_one_group)
            planning_tutorials_per_group.append(Matrix(len(tutorial_list_one_group), number_of_weeks, 0, limit_hours_course))

            # Experiments
            experiment_list_per_group.append(experiment_list_one_group)
            planning_experiments_per_group.append(Matrix(len(experiment_list_one_group), number_of_weeks, 0, limit_hours_course))

        # ------------------------ Initialize tutorial and experiment lists for teachers -------------------- #

        index_teacher_list = []
        teacher_max_hours = 12  # maximum slot number for a teacher per week

        tutorial_list_per_teacher = []
        experiment_list_per_teacher = []
        planning_tutorials_per_teacher = []
        planning_experiments_per_teacher = []

        for teacher in teacher_list:
            tutorial_list_one_teacher = []
            experiment_list_one_teacher = []
            for course in teacher['course_list']:
                if course['tutorial_gp_nb'] > 0:
                    if course['course']['tutorial'] > 0:  # The current teacher has tutorials' current course with at least one group
                        tutorial_list_one_teacher += [[course['course']['name'], course['course']['tutorial']]]
                if course['experiment_gp_nb'] > 0:
                    if course['course']['experiment'] > 0:  # The current teacher has experiments' current course with at least one group
                        experiment_list_one_teacher += [[course['course']['name'], course['course']['experiment']]]

            index_teacher_list.append({'index_lecture_list': list_index_lesson(teacher, 'lecture', lecture_list),
                                       'index_tutorial_list': list_index_lesson(teacher, 'tutorial', tutorial_list_one_teacher),
                                       'index_experiment_list': list_index_lesson(teacher, 'experiment', experiment_list_one_teacher)})

            # Tutorials
            tutorial_list_per_teacher.append(tutorial_list_one_teacher)
            planning_tutorials_one_teacher = Matrix(len(tutorial_list_one_teacher), number_of_weeks, 0, limit_hours_course)
            planning_tutorials_per_teacher.append(planning_tutorials_one_teacher)

            # Experiments
            experiment_list_per_teacher.append(experiment_list_one_teacher)
            planning_experiments_one_teacher = Matrix(len(experiment_list_one_teacher), number_of_weeks, 0,limit_hours_course)
            planning_experiments_per_teacher.append(planning_experiments_one_teacher)

        # ----------------------------------- Additional group initialization -------------------------------------- #

        # ---------------------------------- Additional teacher initialization ------------------------------------- #

        # TODO : implement a function that gives the option of being absent only some days in a week, and
        #  the function computes the numbers of periods corresponding to these days of absence

        # ------------------------------------- Additional room initialization --------------------------------------- #
        # TODO : Take into account type room

        # ------------------------------------------------------------------------------------------------- #
        # ----------------------------------- Model : add all the constraints ----------------------------- #
        # ------------------------------------------------------------------------------------------------- #

        model = Model()

        # --------------------------------------- Course constraints -------------------------------------- #

        # Lectures
        # On the matrix, each row represents a lecture, and each column represent a week.
        # Constraint : The sum of a row should be equal to the corresponding lecture total hours.
        model += [Sum(row) == hours[1] for (row, hours) in zip(planning_lectures.row, lecture_list)]

        # Tutorials
        # Constraint : The sum of a row should be equal to the corresponding tutorial total hours,
        model += [Sum(row) == hours[1] for group in range(len(group_list)) for (row, hours) in zip(planning_tutorials_per_group[group].row, tutorial_list_per_group[group])]
        model += [Sum(row) == hours[1] for teacher in range(len(teacher_list)) for (row, hours) in zip(planning_tutorials_per_teacher[teacher].row, tutorial_list_per_teacher[teacher])]

        # Experiments
        # Constraint : The sum of a row should be equal to the corresponding experiment total hours,
        model += [Sum(row) == hours[1] for group in range(len(group_list)) for (row, hours) in zip(planning_experiments_per_group[group].row, experiment_list_per_group[group])]
        model += [Sum(row) == hours[1] for teacher in range(len(teacher_list)) for (row, hours) in zip(planning_experiments_per_teacher[teacher].row, experiment_list_per_teacher[teacher])]

        # Specific constraints #

        # Tutorials start after X lectures #
        for group in range(len(group_list)):
            (x, id_lec, id_exe, nb_lec) = exercises_only_after_x_lectures(course_list[1], lecture_list, tutorial_list_per_group[group], course_list[1]['lecture'], 6)
            middle = int(limit_hours_course*number_of_weeks*0.5)
            if len(planning_tutorials_per_group[group]) > 0:
                if (x < middle) and (x < nb_lec):
                    for i in range(int(number_of_weeks*0.5)):
                        model += (planning_tutorials_per_group[group][id_exe][i] == 0)
                    for i in range(int(number_of_weeks * 0.5), number_of_weeks):
                        model += (planning_lectures[id_lec][i] <= int((nb_lec-x)/(number_of_weeks*0.5)))

        # ---------------------------------------- Group constraints ------------------------------------------- #

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
        total_hours_group_list = []
        total_lecture_hours_group_list_undup = []
        total_tutorial_hours_group_list = []
        total_experiment_hours_group_list = []
        checked_promo_list = []
        group_index = 0
        for group_info in group_list:
            # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
            total_lecture_hours_one_group_undup = []
            total_tutorial_hours_one_group = []
            total_experiment_hours_one_group = []
            total_hours_one_group = []

            for week in range(number_of_weeks):
                hours_lectures, hours_tutorials_per_type_room, hours_experiments, hours_total, \
                unduplicated_lecture_hours = get_group_hours(group_info,
                                                             group_index,
                                                             index_group_list,
                                                             week,
                                                             planning_lectures,
                                                             planning_tutorials_per_group[group_index],
                                                             planning_experiments_per_group[group_index],
                                                             checked_promo_list)

                # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
                total_lecture_hours_one_group_undup.append(unduplicated_lecture_hours)
                total_tutorial_hours_one_group.append(hours_tutorials_per_type_room)
                total_experiment_hours_one_group.append(hours_experiments)
                total_hours_one_group.append(hours_total)

                model += (hours_total <= slots)

            # Add details of one group in the groups' lists
            total_lecture_hours_group_list_undup.append(total_lecture_hours_one_group_undup)
            total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
            total_experiment_hours_group_list.append(total_experiment_hours_one_group)
            total_hours_group_list.append(total_hours_one_group)

            checked_promo_list.append(index_group_list[group_index]['promo'])
            group_index += 1

        # -------------------------------------- Teacher constraints -------------------------------------- #

        for teacher_index in range(len(teacher_list)):
            for week in range(number_of_weeks):
                hours = get_teacher_hours(teacher_index,
                                          index_teacher_list,
                                          week,
                                          planning_lectures,
                                          planning_tutorials_per_teacher[teacher_index],
                                          planning_experiments_per_teacher[teacher_index])
                model += (hours <= teacher_max_hours)

        # Specific teacher constraints #

        # teacher_1 is not available the first week
        teacher_index = 0
        max_hours = 0
        hours = get_teacher_hours(teacher_index, index_teacher_list, 0, planning_lectures, planning_tutorials_per_teacher[teacher_index],
                                  planning_experiments_per_teacher[teacher_index])
        model += (hours <= max_hours)

        # teacher_6 is not available the fourth week
        teacher_index = 5
        max_hours = 0
        hours = get_teacher_hours(teacher_index, index_teacher_list, 3, planning_lectures, planning_tutorials_per_teacher[teacher_index],
                                  planning_experiments_per_teacher[teacher_index])
        model += (hours <= max_hours)

        teacher_index = 5
        max_hours = 0
        hours = get_teacher_hours(teacher_index, index_teacher_list, 8, planning_lectures, planning_tutorials_per_teacher[teacher_index],
                                  planning_experiments_per_teacher[teacher_index])
        model += (hours <= max_hours)

        # # ---------------------------------------- Room constraints --------------------------------------- #

        # Instantiate lists to know what rooms could be use for lecture/tutorial/experiment
        rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(rooms_list)

        # # Instantiate union lists
        # # union_lectures_tutorials : rooms that could be use for lectures or/and tutorials
        # # union_lectures_experiments : rooms that could be use for lectures or/and experiments
        # # union_tutorials_experiments : rooms that could be use for tutorials or/and experiments
        # union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments = \
        #     get_union_list_rooms_according_type_hours(rooms_list)

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week
        total_hours_lecture = get_total_hours_week(total_lecture_hours_group_list_undup)
        total_hours_tutorial = get_total_hours_week_per_type_room(total_tutorial_hours_group_list, number_of_weeks)
        total_hours_experiment = get_total_hours_week(total_experiment_hours_group_list)

        # Instantiate sum total of lectures/tutorials/experiments per week
        # total_hours_union_lecture_tutorial : sum total of lectures and tutorials
        # total_hours_union_lecture_experiment : sum total of lectures and experiments
        # total_hours_union_tutorial_experiment : sum total of tutorials and experiments
        # total_hours_union_lecture_tutorial = get_total_hours_week([total_hours_lecture, total_hours_tutorial])
        # total_hours_union_lecture_experiment = get_total_hours_week([total_hours_lecture, total_hours_experiment])
        # total_hours_union_tutorial_experiment = get_total_hours_week([total_hours_tutorial, total_hours_experiment])

        # Constraint : Lecture should be done in a room that is for lectures
        model += is_lesson_hours_lt_resources(total_hours_lecture, len(rooms_lectures), resource_per_room)

        # # Constraint : Tutorial should be done in a room that is for tutorials
        # model += is_lesson_hours_lt_resources(total_hours_tutorial, len(rooms_tutorials), resource_per_room)
        #
        # # Constraint : Experiment should be done in a room that is for experiments
        # model += is_lesson_hours_lt_resources(total_hours_experiment, len(rooms_experiments), resource_per_room)
        #
        # # Constraint : Lecture and tutorial should not be done in the same room at the same time
        # model += is_lesson_hours_lt_resources(total_hours_union_lecture_tutorial, len(union_lectures_tutorials), resource_per_room)
        #
        # # Constraint : Lecture and experiment should not be done in the same room at the same time
        # model += is_lesson_hours_lt_resources(total_hours_union_lecture_experiment, len(union_lectures_experiments), resource_per_room)
        #
        # # Constraint : Tutorial and experiment should not be done in the same room at the same time
        # model += is_lesson_hours_lt_resources(total_hours_union_tutorial_experiment, len(union_tutorials_experiments), resource_per_room)

        # Constraint : There should not be more lectures,tutorials and experiments than available rooms
        model += is_lesson_hours_lt_resources(get_total_hours_week(total_hours_group_list), len(rooms_list), resource_per_room)

        self.planning_lectures = planning_lectures
        self.planning_tutorials_group = planning_tutorials_per_group
        self.planning_experiments_group = planning_experiments_per_group
        self.planning_tutorials_teacher = planning_tutorials_per_teacher
        self.planning_experiments_teacher = planning_experiments_per_teacher
        self.index_teacher_list = index_teacher_list
        self.index_group_list = index_group_list
        self.rooms_list = rooms_list
        self.resource_per_room = resource_per_room

        # Printing needed data
        self.group_list = group_list
        self.lecture_list = lecture_list
        self.tutorial_list_per_group = tutorial_list_per_group
        self.experiment_list_per_group = experiment_list_per_group
        self.N = N

        return model

    def solve(self, param):
        model = self.get_model(param['N'])
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
            # out += ('\n\nNodes: ' + str(solver.getNodes()))

            # ------------------------- #
            # ----- Teacher Test ------ #
            # ------------------------- #

            out = "\n\n        # ------------------------- #"
            out += "\n\n        # ----- Teacher Test ------ #"
            out += "\n\n        # ------------------------- #"
            out += '\n\nLectures: \n' + str(self.planning_lectures)
            for teacher_index in range(len(self.planning_tutorials_teacher)):
                out += ('\n\n\nTeacher ' + str(teacher_index + 1) + ': \n')
                out += 'Tutorials' + str(Solution(self.planning_tutorials_teacher[teacher_index]))
                out += '\nClassroom Experiments' + str(Solution(self.planning_experiments_teacher[teacher_index]))
                total_teacher_hours = []
                for week in range(len(self.planning_lectures.col)):
                    hours = get_teacher_hours(teacher_index,
                                              self.index_teacher_list,
                                              week,
                                              Solution(self.planning_lectures),
                                              Solution(self.planning_tutorials_teacher[teacher_index]),
                                              Solution(self.planning_experiments_teacher[teacher_index]))
                    total_teacher_hours.append(hours)
                out += "\n\nTotal"
                # Sum lecture from planning_lectures
                # + tutorial from planning_tutorials_teacher
                # + experiment hours from planning_experiment_teacher
                out += str(total_teacher_hours)

            # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
            total_hours_group_list = []
            total_lecture_hours_group_list_undup = []
            total_tutorial_hours_group_list = []
            total_experiment_hours_group_list = []
            checked_promo_list = []

            # ----------------------- #
            # ----- Group Test ------ #
            # ----------------------- #

            out += "\n\n"
            out += "\n\n        # ----------------------- #"
            out += "\n\n        # ----- Group Test ------ #"
            out += "\n\n        # ----------------------- #"
            group_index = 0
            for group in self.group_list:
                out += ('\n\nGroup ' + str(group_index + 1) + ': \n')

                # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
                total_lecture_hours_one_group = []
                total_lecture_hours_one_group_undup = []
                total_tutorial_hours_one_group = []
                total_experiment_hours_one_group = []
                total_hours_one_group = []

                for week in range(len(self.planning_lectures.col)):
                    hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours = \
                        get_group_hours(group,
                                        group_index,
                                        self.index_group_list,
                                        week,
                                        Solution(self.planning_lectures),
                                        Solution(self.planning_tutorials_group[group_index]),
                                        Solution(self.planning_experiments_group[group_index]),
                                        checked_promo_list)

                    # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
                    total_lecture_hours_one_group_undup.append(unduplicated_lecture_hours)
                    total_lecture_hours_one_group.append(hours_lectures)
                    total_tutorial_hours_one_group.append(hours_tutorials)
                    total_experiment_hours_one_group .append(hours_experiments)
                    total_hours_one_group.append(hours_total)

                # Print details of the current group
                out += "Lecture" + str(total_lecture_hours_one_group)
                out += "\nTutorial" + str(total_tutorial_hours_one_group)
                out += "\nExperiments" + str(total_experiment_hours_one_group)
                out += "\n\nTotal" + str(total_hours_one_group)
                out += "\n\n"
                out += str(Solution(self.planning_tutorials_group[group_index]))
                out += "\n\n"

                # Add details of one group in the groups' lists
                total_lecture_hours_group_list_undup.append(total_lecture_hours_one_group_undup)
                total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
                total_experiment_hours_group_list.append(total_experiment_hours_one_group)
                total_hours_group_list.append(total_hours_one_group)

                checked_promo_list.append(self.index_group_list[group_index]['promo'])
                group_index += 1

            # ---------------------- #
            # ----- Room Test ------ #
            # ---------------------- #

            rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(self.rooms_list)
            # union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments =
            # get_union_list_rooms_according_type_hours(rooms_list)

            # Lists containing total of lectures/tutorials/experiments hours per week
            total_hours_lecture = Solution(get_total_hours_week(total_lecture_hours_group_list_undup))
            # total_hours_tutorial = Solution(get_total_hours_week(total_tutorial_hours_group_list, 'tutorial'))
            # total_hours_experiment = Solution(get_total_hours_week(total_experiment_hours_group_list, 'experiment'))

            # # Lists containing sum total of lectures/tutorials/experiments per week
            # total_hours_union_lecture_tutorial = Solution(get_total_hours_week([total_hours_lecture, total_hours_tutorial]))
            # total_hours_union_lecture_experiment = Solution(get_total_hours_week([total_hours_lecture, total_hours_experiment]))
            # total_hours_union_tutorial_experiment = Solution(get_total_hours_week([total_hours_tutorial, total_hours_experiment]))

            out += "\n\n"
            out += "\n\n        # ---------------------- #"
            out += "\n\n        # ----- Room Test ------ #"
            out += "\n\n        # ---------------------- #"
            out += "\n\nTotal hours lecture: " + str(total_hours_lecture)
            out += "\nTotal hours tutorial: " + str(get_total_hours_week_per_type_room(total_tutorial_hours_group_list, 10))
            # out += "\nTotal hours experiment: " + str(total_hours_experiment)
            out += "\n"
            # out += "\n\nTotal hours lecture+tutorial: " + str(total_hours_union_lecture_tutorial)
            # out += "\nTotal hours lecture+experiment: " + str(total_hours_union_lecture_experiment)
            # out += "\nTotal hours tutorial+experiment: " + str(total_hours_union_tutorial_experiment)
            out += "\n"
            out += "\nResources max for lectures per week: " + str(self.resource_per_room*len(rooms_lectures))
            out += "\nResources max for tutorials per week: " + str(self.resource_per_room*len(rooms_tutorials))
            out += "\nResources max for experiments per week: " + str(self.resource_per_room*len(rooms_experiments))

            self.print_csv("res.csv")

        else:
            out = "No solution has been found !"

        return out


default = {'solver': 'Mistral2', 'N': 10, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}

if __name__ == '__main__':
    params = input(default)
    planning = Planning()
    print(planning.solve(params))
