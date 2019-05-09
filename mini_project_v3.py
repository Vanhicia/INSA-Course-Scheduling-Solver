import Test
from Numberjack import *
from group_functions import *
from room_functions import *
from teacher_functions import *
from course_functions import *


class Planning:

    def __init__(self):
        self.planning_lectures = None
        self.planning_tutorials = None
        self.planning_experiments = None

        self.index_teacher_list = None
        self.index_group_list = None

        self.rooms_list = None
        self.resource_per_room = None

        # Added for printing
        self.group_list = None
        self.lecture_list = None
        self.tutorial_list = None
        self.experiment_list = None

        self.N = None

    def print_csv(self, filename):
        file = open(filename, "w")
        cpt = 0
        for grp in self.index_group_list:
            file.write(self.group_list[cpt]['name']+"\n")
            cpt+=1

            total = [0]*self.N

            for wk in range(1, self.N+1):
                file.write(";Semaine "+str(wk))

            for cs in grp['index_lecture_list']:
                file.write("\n CM : "+self.lecture_list[cs['index']][0])
                for wk in range(self.N): #TODO Change to use parameter
                    total[wk] += int(str(self.planning_lectures[cs['index']][wk]))
                    file.write(";"+str(self.planning_lectures[cs['index']][wk]))

            for cs in grp['index_tutorial_list']:
                file.write("\n TD : "+self.tutorial_list[cs['index']][0])
                for wk in range(self.N): #TODO Change to use parameter
                    total[wk] += int(str(self.planning_tutorials[cs['index']][wk]))
                    file.write(";"+str(self.planning_tutorials[cs['index']][wk]))

            for cs in grp['index_experiment_list']:
                file.write("\n TP : "+self.experiment_list[cs['index']][0])
                for wk in range(self.N): #TODO Change to use parameter
                    total[wk] += (int(str(self.planning_experiments[cs['index']][wk]))*2)
                    file.write(";"+str(int(str(self.planning_experiments[cs['index']][wk]))*2))

            file.write("\n Total ")
            for tot in total:
                file.write(";"+str(tot))
            file.write("\n\n")
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
        # ----------------------------------- Additional course initialization ------------------------------------ #

        # Create lecture/tutorial/experiment list
        # One element contains the name of the subject + the number of lectures/tutorials/experiments
        lecture_list = []
        tutorial_list = []
        experiment_list = []

        for course in course_list:
            # some courses have only lectures, only tutorials or only experiments,
            # so we need to check which type of lesson is contained in the current course
            if course['lecture'] > 0:
                lecture_list += [[course['name'], course['lecture']]]
            if course['tutorial'] > 0:
                tutorial_list += [[course['name'], course['tutorial']]]
            if course['experiment'] > 0:
                experiment_list += [[course['name'], course['experiment']]]

        # Matrix representing planning for each lesson type
        planning_lectures = Matrix(len(lecture_list), number_of_weeks, 0, limit_hours_course)
        planning_tutorials = Matrix(len(tutorial_list), number_of_weeks, 0, limit_hours_course)
        planning_experiments = Matrix(len(experiment_list), number_of_weeks, 0, limit_hours_course)

        # ----------------------------------- Additional group initialization -------------------------------------- #

        # a list is created, which contains for each group the promotion,
        # and a sublist for each type of class (lecture, tutorial, and experiment).
        # each sublist presents every course followed by the group,
        # and a number of hours for the present type of class for the present course
        index_group_list = []
        for group in group_list:
            index_group_list.append({'promo':group['promo'],
                                     'index_lecture_list': list_index_lesson_group(group, 'lecture', lecture_list),
                                     'index_tutorial_list': list_index_lesson_group(group, 'tutorial', tutorial_list),
                                     'index_experiment_list': list_index_lesson_group(group, 'experiment', experiment_list)})
        print(index_group_list)
        # ---------------------------------- Additional teacher initialization ------------------------------------- #

        # TODO : implement a function that gives the option of being absent only some days in a week, and
        #  the function computes the numbers of periods corresponding to these days of absence

        teacher_max_hours = 12  # maximum slot number for a teacher per week

        index_teacher_list = []
        for teacher in teacher_list:
            index_teacher_list.append({'index_lecture_list': list_index_lesson(teacher, 'lecture', lecture_list),
                                       'index_tutorial_list': list_index_lesson(teacher, 'tutorial', tutorial_list),
                                       'index_experiment_list': list_index_lesson(teacher, 'experiment', experiment_list)})

        # ------------------------------------- Room initialization --------------------------------------- #
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
        model += [Sum(row) == hours[1] for (row, hours) in zip(planning_tutorials.row, tutorial_list)]

        # Experiments
        # Constraint : The sum of a row should be equal to the corresponding experiment total hours,
        model += [Sum(row) == hours[1] for (row, hours) in zip(planning_experiments.row, experiment_list)]

        # Specific constraints #

        # exercises start after X lectures #

        (x, id_lec, id_exe, nb_lec) = exercises_only_after_x_lectures(course_list[1], lecture_list, tutorial_list,course_list[1]['lecture'], 6)
        middle = int(limit_hours_course*number_of_weeks*0.5)
        if (x < middle) and (x<nb_lec):
            for i in range(int(number_of_weeks*0.5)):
                model += (planning_tutorials[id_exe][i] == 0)
            for i in range(int(number_of_weeks * 0.5), number_of_weeks):
                model += (planning_lectures[id_lec][i] <= int((nb_lec-x)/(number_of_weeks*0.5)))

        # ---------------------------------------- Group constraints ------------------------------------------- #

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
        total_hours_group_list = []
        total_lecture_hours_group_list_undup = []
        total_tutorial_hours_group_list = []
        total_experiment_hours_group_list = []
        checked_promo_list = []

        for group_index in range(len(group_list)):

            # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
            total_lecture_hours_one_group_undup = []
            total_tutorial_hours_one_group = []
            total_experiment_hours_one_group = []
            total_hours_one_group = []

            for week in range(number_of_weeks):
                hours_lectures, hours_tutorials, hours_experiments, hours_total, \
                    unduplicated_lecture_hours = get_group_hours(group_index,
                                                                 index_group_list,
                                                                 week,
                                                                 planning_lectures,
                                                                 planning_tutorials,
                                                                 planning_experiments,
                                                                 checked_promo_list)

                # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
                total_lecture_hours_one_group_undup.append(unduplicated_lecture_hours)
                total_tutorial_hours_one_group.append(hours_tutorials)
                total_experiment_hours_one_group.append(hours_experiments)
                total_hours_one_group.append(hours_total)

                model += (hours_total <= slots)

            # Add details of one group in the groups' lists
            total_lecture_hours_group_list_undup.append(total_lecture_hours_one_group_undup)
            total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
            total_experiment_hours_group_list.append(total_experiment_hours_one_group)
            total_hours_group_list.append(total_hours_one_group)

            checked_promo_list.append(index_group_list[group_index]['promo'])

        # -------------------------------------- Teacher constraints -------------------------------------- #

        for teacher_index in range(len(teacher_list)):
            for week in range(number_of_weeks):
                hours = get_teacher_hours(teacher_index,
                                          index_teacher_list,
                                          week,
                                          planning_lectures,
                                          planning_tutorials,
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

        # ---------------------------------------- Room constraints --------------------------------------- #

        # Instantiate lists to know what rooms could be use for lecture/tutorial/experiment
        rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(rooms_list)

        # Instantiate union lists
        # union_lectures_tutorials : rooms that could be use for lectures or/and tutorials
        # union_lectures_experiments : rooms that could be use for lectures or/and experiments
        # union_tutorials_experiments : rooms that could be use for tutorials or/and experiments
        union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments = \
            get_union_list_rooms_according_type_hours(rooms_list)

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week
        total_hours_lecture = get_total_hours_week(total_lecture_hours_group_list_undup)
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

        # Constraint : There should not be more lectures,tutorials and experiments than available rooms
        model += is_lesson_hours_lt_resources(get_total_hours_week(total_hours_group_list), len(rooms_list), resource_per_room)

        self.planning_lectures = planning_lectures
        self.planning_tutorials = planning_tutorials
        self.planning_experiments = planning_experiments
        self.index_teacher_list = index_teacher_list
        self.index_group_list = index_group_list
        self.rooms_list = rooms_list
        self.resource_per_room = resource_per_room

        #Printing needed data
        self.group_list = group_list
        self.lecture_list = lecture_list
        self.tutorial_list = tutorial_list
        self.experiment_list = experiment_list
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

            # print plannings
            out = '\nLectures: \n' + str(self.planning_lectures)
            out += '\n\nTutorials: \n' + str(self.planning_tutorials)
            out += '\n\nClassroom Experiments: \n' + str(self.planning_experiments)

            # out += ('\n\nNodes: ' + str(solver.getNodes()))

            # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
            total_hours_group_list = []
            total_lecture_hours_group_list_undup = []
            total_tutorial_hours_group_list = []
            total_experiment_hours_group_list = []
            checked_promo_list = []

            # print groups' hours
            for group_index in range(len(self.index_group_list)):
                out += ('\n\nGroup ' + str(group_index + 1) + ': \n')

                # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
                total_lecture_hours_one_group = []
                total_lecture_hours_one_group_undup = []
                total_tutorial_hours_one_group = []
                total_experiment_hours_one_group = []
                total_hours_one_group = []

                for week in range(len(self.planning_lectures.col)):
                    hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours = \
                        get_group_hours(group_index,
                                        self.index_group_list,
                                        week,
                                        Solution(self.planning_lectures),
                                        Solution(self.planning_tutorials),
                                        Solution(self.planning_experiments),
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

                # Add details of one group in the groups' lists
                total_lecture_hours_group_list_undup.append(total_lecture_hours_one_group_undup)
                total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
                total_experiment_hours_group_list.append(total_experiment_hours_one_group)
                total_hours_group_list.append(total_hours_one_group)

                checked_promo_list.append(self.index_group_list[group_index]['promo'])

            # print teachers' hours
            for teacher_index in range(len(self.index_teacher_list)):
                out += ('\n\nTeacher ' + str(teacher_index + 1) + ': \n')
                total_teacher_hours = []
                for week in range(len(self.planning_lectures.col)):
                    hours = get_teacher_hours(teacher_index,
                                              self.index_teacher_list,
                                              week,
                                              Solution(self.planning_lectures),
                                              Solution(self.planning_tutorials),
                                              Solution(self.planning_experiments))
                    total_teacher_hours.append(hours)
                out += str(total_teacher_hours)




            # ---------------------- #
            # ----- Room Test ------ #
            # ---------------------- #

            rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(self.rooms_list)
            # union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments =
            # get_union_list_rooms_according_type_hours(rooms_list)

            # Lists containing total of lectures/tutorials/experiments hours per week
            total_hours_lecture = Solution(get_total_hours_week(total_lecture_hours_group_list_undup))
            total_hours_tutorial = Solution(get_total_hours_week(total_tutorial_hours_group_list))
            total_hours_experiment = Solution(get_total_hours_week(total_experiment_hours_group_list))

            # Lists containing sum total of lectures/tutorials/experiments per week
            total_hours_union_lecture_tutorial = Solution(get_total_hours_week([total_hours_lecture, total_hours_tutorial]))
            total_hours_union_lecture_experiment = Solution(get_total_hours_week([total_hours_lecture, total_hours_experiment]))
            total_hours_union_tutorial_experiment = Solution(get_total_hours_week([total_hours_tutorial, total_hours_experiment]))

            out += "\n\n"
            out += "\n\n        # ---------------------- #"
            out += "\n\n        # ----- Room Test ------ #"
            out += "\n\n        # ---------------------- #"
            out += "\n\nTotal hours lecture: " + str(total_hours_lecture)
            out += "\nTotal hours tutorial: " + str(total_hours_tutorial)
            out += "\nTotal hours experiment: " + str(total_hours_experiment)
            out += "\n"
            out += "\n\nTotal hours lecture+tutorial: " + str(total_hours_union_lecture_tutorial)
            out += "\nTotal hours lecture+experiment: " + str(total_hours_union_lecture_experiment)
            out += "\nTotal hours tutorial+experiment: " + str(total_hours_union_tutorial_experiment)
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
