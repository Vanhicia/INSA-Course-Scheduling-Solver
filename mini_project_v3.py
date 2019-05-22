import Test
from Numberjack import *
from group_functions import *
from room_functions import *
from teacher_functions import *
from course_functions import *


class Planning:

    def __init__(self):
        self.planning_lectures_per_promo = None
        self.planning_tutorials_group = None
        self.planning_experiments_group = None
        self.planning_tutorials_teacher = None
        self.planning_experiments_teacher = None
        self.index_teacher_list = None
        self.index_group_list = None

        self.rooms_list = None
        self.resource_per_room = None

        # Added for printing
        self.teacher_list = None
        self.group_list = None
        self.promo_list = None
        self.promo_list2 = None
        self.tutorial_list_per_group = None
        self.experiment_list_per_group = None
        self.lecture_list_per_promo2 = None
        self.tutorial_list_per_group2 = None
        self.experiment_list_per_group2 = None
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
                file.write("\n CM : "+cs['name'])
                for wk in range(self.N):
                    total[wk] += int(str(self.planning_lectures_per_promo[int(grp['promo'])-1][cs['index']][wk]))
                    file.write(";"+str(self.planning_lectures_per_promo[int(grp['promo'])-1][cs['index']][wk]))

            for cs in grp['index_tutorial_list']:
                file.write("\n TD : "+self.tutorial_list_per_group[cpt][cs['index']][0])
                for wk in range(self.N):
                    total[wk] += int(str(self.planning_tutorials_group[cpt][cs['index']][wk]))
                    file.write(";"+str(self.planning_tutorials_group[cpt][cs['index']][wk]))

            for cs in grp['index_experiment_list']:
                file.write("\n TP : "+self.experiment_list_per_group[cpt][cs['index']][0])
                for wk in range(self.N):
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
        resource_per_room = 7   # Number of slots per week a room could contained
        limit_hours_course_for_lectures = 5  # leveling factor
        limit_hours_course_for_tutorials = 5  # leveling factor
        limit_hours_course_for_experiments = 2  # leveling factor

        # Get a data set from Test.py
        course_list, teacher_list, group_list, promo_list, promo_list2, rooms_list, value_type_room, teacher_absence_list = Test.data_set(2)

        course_list, teacher_list, group_list, promo_list, promo_list2, rooms_list, value_type_room, teacher_absence_list, spe_cst_list = Test.data_set(3)

        # ----------------------------------- Course initialization ------------------------------------ #

        # Create lecture/tutorial/experiment list
        # One element contains the name of the subject + the number of lectures/tutorials/experiments
        lecture_list_per_promo = []
        tutorial_list_per_group = []
        experiment_list_per_group = []

        # These lists contain the course variables followed by the students
        # They are useful to define teacher constraints
        lecture_list_per_promo2 = []
        tutorial_list_per_group2 = []
        experiment_list_per_group2 = []

        # --------------------------- Initialize planning_lecture, tutorial and experiment --------------------------- #
        promo_list = get_promos(group_list)

        # Matrix representing planning for lecture lessons

        planning_lectures_per_promo = []

        # Lists containing matrix representing planning for tutorial/experiment per group
        planning_tutorials_per_group = []
        planning_experiments_per_group = []

        # a list is created, which contains for each group the promotion,
        # and a sublist for each type of class (lecture, tutorial, and experiment).
        # each sublist presents every course followed by the group,
        # and a number of hours for the present type of class for the present course
        index_group_list = []

        for promo in promo_list:
            lecture_list_one_promo = []
            lecture_list_one_promo2 = []
            for group in promo_list[promo]:
                tutorial_list_one_group = []
                experiment_list_one_group = []
                tutorial_list_one_group2 = []
                experiment_list_one_group2 = []
                for course in group['course_list']:
                    if course['lecture'] > 0 and ([[course['name'], course['lecture']]] not in lecture_list_one_promo):
                        lecture_list_one_promo += [[course['name'], course['lecture']]]
                        lecture_list_one_promo2 += [course]
                    if course['tutorial'] > 0:  # The current group has tutorials' current course
                        tutorial_list_one_group += [[course['name'], course['tutorial']]]
                        tutorial_list_one_group2 += [course]
                    if course['experiment'] > 0:  # The current group has experiments' current course
                        experiment_list_one_group += [[course['name'], course['experiment']]]
                        experiment_list_one_group2 += [course]

                index_group_list.append({'promo': group['promo'],
                                         'index_lecture_list': list_index_lesson_group(group, 'lecture',
                                                                                       lecture_list_one_promo),
                                         'index_tutorial_list': list_index_lesson_group(group, 'tutorial',
                                                                                        tutorial_list_one_group),
                                         'index_experiment_list': list_index_lesson_group(group, 'experiment',
                                                                                          experiment_list_one_group)})

                # Tutorials
                tutorial_list_per_group.append(tutorial_list_one_group)
                tutorial_list_per_group2.append(tutorial_list_one_group2)
                planning_tutorials_per_group.append(
                    Matrix(len(tutorial_list_one_group), number_of_weeks, 0, limit_hours_course_for_tutorials))

                # Experiments
                experiment_list_per_group.append(experiment_list_one_group)
                experiment_list_per_group2.append(experiment_list_one_group2)
                planning_experiments_per_group.append(
                    Matrix(len(experiment_list_one_group), number_of_weeks, 0, limit_hours_course_for_experiments))

            # Lectures
            lecture_list_per_promo.append(lecture_list_one_promo)
            lecture_list_per_promo2.append(lecture_list_one_promo2)
            planning_lectures_per_promo.append(
                Matrix(len(lecture_list_one_promo), number_of_weeks, 0, limit_hours_course_for_lectures))

        # ----------------------------------- Additional group initialization -------------------------------------- #

        # ---------------------------------- Additional teacher initialization ------------------------------------- #

        # ------------------------------------- Additional room initialization --------------------------------------- #

        # ------------------------------------------------------------------------------------------------- #
        # ----------------------------------- Model : add all the constraints ----------------------------- #
        # ------------------------------------------------------------------------------------------------- #

        model = Model()

        # --------------------------------------- Course constraints -------------------------------------- #

        # Lectures
        # On the matrix, each row represents a lecture, and each column represent a week.
        # Constraint : The sum of a row should be equal to the corresponding lecture total hours.
        model += [Sum(row) == hours[1] for promo in range(len(promo_list)) for (row, hours) in zip(planning_lectures_per_promo[promo].row, lecture_list_per_promo[promo])]

        # Tutorials
        # Constraint : The sum of a row should be equal to the corresponding tutorial total hours,
        model += [Sum(row) == hours[1] for group in range(len(group_list)) for (row, hours) in zip(planning_tutorials_per_group[group].row, tutorial_list_per_group[group])]

        # Experiments
        # Constraint : The sum of a row should be equal to the corresponding experiment total hours,
        model += [Sum(row) == hours[1] for group in range(len(group_list)) for (row, hours) in zip(planning_experiments_per_group[group].row, experiment_list_per_group[group])]

        # Specific constraints #
        # Tutorials start after X lectures #
        for spe_cst in spe_cst_list:
            cst_specific_tut(spe_cst,lecture_list_per_promo, tutorial_list_per_group, promo_list, group_list,
                         planning_tutorials_per_group,
                         planning_lectures_per_promo, limit_hours_course_for_lectures, number_of_weeks, model)

            # cst_specific_exp(spe_cst,lecture_list_per_promo, experiment_list_per_group, promo_list, group_list,
            #              planning_experiments_per_group,
            #              planning_lectures_per_promo, limit_hours_course_for_lectures, number_of_weeks, model)


        # ---------------------------------------- Group constraints ------------------------------------------- #

        # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
        total_hours_group_list = []
        total_lecture_hours_group_list_undup = []
        total_tutorial_hours_group_list = []
        total_tutorial_hours_group_list_per_room = []
        total_experiment_hours_group_list = []
        total_experiment_hours_group_list_per_room = []
        group_index = 0
        promo_index = 0

        for promo in promo_list:

            # resetting the checked subject list because the current promo was changed
            checked_subject = []

            for group_info in promo_list[promo]:

                # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
                total_lecture_hours_one_group_undup = []
                total_tutorial_hours_one_group = []
                total_tutorial_hours_one_group_per_room = []
                total_experiment_hours_one_group = []
                total_experiment_hours_one_group_per_room = []
                total_hours_one_group = []
                checked_subject_weekly = []  # we reset the weekly list for every group

                for week in range(number_of_weeks):
                    hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours, \
                        subject_treated, hours_tutorials_per_type_room, hours_experiments_per_type_room = \
                        get_group_hours(group_info,
                                        group_index,
                                        index_group_list,
                                        week,
                                        planning_lectures_per_promo[promo_index],
                                        planning_tutorials_per_group[group_index],
                                        planning_experiments_per_group[group_index],
                                        checked_subject)

                    # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
                    total_lecture_hours_one_group_undup.append(unduplicated_lecture_hours)
                    total_tutorial_hours_one_group_per_room.append(hours_tutorials_per_type_room)
                    total_experiment_hours_one_group_per_room.append(hours_experiments_per_type_room)
                    total_tutorial_hours_one_group.append(hours_tutorials)
                    total_experiment_hours_one_group.append(hours_experiments)
                    total_hours_one_group.append(hours_total)

                    # every week, for every treated subject, if they are not already in the temporary list, we add them
                    for subject in subject_treated:
                        if (subject not in checked_subject_weekly) and (subject != []):
                            checked_subject_weekly.append(subject)

                    model += (hours_total <= slots)

                # Add details of one group in the groups' lists
                total_lecture_hours_group_list_undup.append(total_lecture_hours_one_group_undup)
                total_tutorial_hours_group_list_per_room.append(total_tutorial_hours_one_group_per_room)
                total_experiment_hours_group_list_per_room.append(total_experiment_hours_one_group_per_room)
                total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
                total_experiment_hours_group_list.append(total_experiment_hours_one_group)
                total_hours_group_list.append(total_hours_one_group)

                # end of treatment for the group:

                # at this point, every week was treated for this group
                # for every subject found, we add them to the checked subject list
                for subject in checked_subject_weekly:
                    if subject not in checked_subject:
                        checked_subject.append(subject)
                group_index += 1

            promo_index += 1

        # -------------------------------------- Teacher constraints -------------------------------------- #
        #
        #         teacher_max_hours = 12  # maximum slot number for a teacher per week
        #
        #         for teacher in teacher_list:
        #             for week in range(number_of_weeks):
        #                 hours = get_teacher_hours(teacher,
        #                                           group_list,
        #                                           promo_list2,
        #                                           week,
        #                                           planning_lectures_per_promo,
        #                                           planning_tutorials_per_group,
        #                                           planning_experiments_per_group,
        #                                           lecture_list_per_promo2,
        #                                           tutorial_list_per_group2,
        #                                           experiment_list_per_group2)
        #                 if hours > 0:
        #                     model += (hours <= teacher_max_hours)
        #
        #         # Specific teacher constraints #
        #
        #         for absence in teacher_absence_list:
        #             max_hours = compute_slot_number(absence['absence_day_number'], teacher_max_hours)
        #             hours = get_teacher_hours(absence['teacher'],
        #                                       group_list,
        #                                       promo_list2,
        #                                       absence['week'],
        #                                       planning_lectures_per_promo,
        #                                       planning_tutorials_per_group,
        #                                       planning_experiments_per_group,
        #                                       lecture_list_per_promo2,
        #                                       tutorial_list_per_group2,
        #                                       experiment_list_per_group2)
        #
        # model += (hours <= max_hours)
        # ---------------------------------------- Room constraints --------------------------------------- #

        # Instantiate lists to know what rooms could be use for lecture/tutorial/experiment
        rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(rooms_list)
        # Instantiate lists containing total of lectures/tutorials/experiments hours per week
        total_hours_lecture = get_total_hours_week(total_lecture_hours_group_list_undup)
        total_hours_tutorial_per_room = get_total_hours_week_per_type_room(total_tutorial_hours_group_list_per_room, number_of_weeks)
        total_hours_experiment_per_room = get_total_hours_week_per_type_room(total_experiment_hours_group_list_per_room, number_of_weeks)
        total_hours_tutorial = get_total_hours_week(total_tutorial_hours_group_list)
        total_hours_experiment = get_total_hours_week(total_experiment_hours_group_list)

        # Constraint : Lecture should be done in a room that is for lectures
        model += is_lesson_hours_lt_resources(total_hours_lecture, len(rooms_lectures), resource_per_room)

        # Constraint : Tutorial should be done in a room that is for tutorials
        # Some tutorial are hold in special room, so we have to distinguish them.
        tutorial_rooms_per_type = get_list_rooms_per_type(rooms_tutorials, value_type_room)

        for week in total_hours_tutorial_per_room:
            for room_key, val in week.items():
                if room_key in tutorial_rooms_per_type:
                    model += is_lesson_hours_lt_resources_one_week(val, tutorial_rooms_per_type[room_key], resource_per_room)
                else:
                    raise Exception("DATA ERROR : there is not this type of room for tutorials : "+ str(room_key))

        # Constraint : Experiment should be done in a room that is for experiments
        # Some experiment are hold in special room, so we have to distinguish them.
        experiment_rooms_per_type = get_list_rooms_per_type(rooms_experiments, value_type_room)
        for week in total_hours_experiment_per_room:
            for room_key, val in week.items():
                if room_key in experiment_rooms_per_type:
                    model += is_lesson_hours_lt_resources_one_week(val, experiment_rooms_per_type[room_key], resource_per_room)
                else:
                    raise Exception("DATA ERROR : there is not this type of room for experiments : " + str(room_key))

        # Instantiate union lists
        # union_lectures_tutorials : rooms that could be use for lectures or/and tutorials
        # union_lectures_experiments : rooms that could be use for lectures or/and experiments
        # union_tutorials_experiments : rooms that could be use for tutorials or/and experiments
        union_lectures_tutorials, union_lectures_experiments = get_union_list_rooms_according_type_hours(rooms_list)
        union_tutorials_experiments = experiment_rooms_per_type
        for key, val in tutorial_rooms_per_type.items():
            if key not in union_tutorials_experiments:
                union_tutorials_experiments.update({key:val})
            else:
                if val > union_tutorials_experiments[key]:
                    union_tutorials_experiments[key] = tutorial_rooms_per_type[key]

        # Instantiate sum total of lectures/tutorials/experiments per week
        # total_hours_union_lecture_tutorial : sum total of lectures and tutorials
        # total_hours_union_lecture_experiment : sum total of lectures and experiments
        # total_hours_union_tutorial_experiment : sum total of tutorials and experiments
        total_hours_union_lecture_tutorial = get_total_hours_week([total_hours_lecture, total_hours_tutorial])
        total_hours_union_lecture_experiment = get_total_hours_week([total_hours_lecture, total_hours_experiment])
        total_hours_union_tutorial_experiment = get_total_hours_week_per_type_room([total_hours_tutorial_per_room, total_hours_experiment_per_room], number_of_weeks)

        # # Constraint : Lecture and tutorial should not be done in the same room at the same time
        model += is_lesson_hours_lt_resources(total_hours_union_lecture_tutorial, len(union_lectures_tutorials), resource_per_room)
        #
        # # Constraint : Lecture and experiment should not be done in the same room at the same time
        model += is_lesson_hours_lt_resources(total_hours_union_lecture_experiment, len(union_lectures_experiments), resource_per_room)

        # Constraint : Tutorial and experiment should not be done in the same room at the same time
        for week in total_hours_union_tutorial_experiment:
            for room_key, val in week.items():
                if room_key in union_tutorials_experiments:
                    model += is_lesson_hours_lt_resources_one_week(val, union_tutorials_experiments[room_key], resource_per_room)
                else:
                    raise Exception("DATA ERROR : there is not this type of room for tutorials/experiments : " + str(room_key))

        # Constraint : There should not be more lectures,tutorials and experiments than available rooms
        model += is_lesson_hours_lt_resources(get_total_hours_week(total_hours_group_list), len(rooms_list), resource_per_room)

        self.planning_lectures_per_promo = planning_lectures_per_promo
        self.planning_tutorials_group = planning_tutorials_per_group
        self.planning_experiments_group = planning_experiments_per_group
        self.index_group_list = index_group_list
        self.rooms_list = rooms_list
        self.resource_per_room = resource_per_room

        # Printing needed data
        self.teacher_list = teacher_list
        self.group_list = group_list
        self.promo_list = promo_list
        self.promo_list2 = promo_list2
        self.tutorial_list_per_group = tutorial_list_per_group
        self.experiment_list_per_group = experiment_list_per_group
        self.tutorial_list_per_group2 = tutorial_list_per_group2
        self.experiment_list_per_group2 = experiment_list_per_group2
        self.lecture_list_per_promo2 = lecture_list_per_promo2
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

            planning_lectures_per_promo2 = []
            for promo in self.promo_list2:
                promo_index = self.promo_list2.index(promo)
                planning_lectures_per_promo2.append(Solution(self.planning_lectures_per_promo[promo_index]))

            planning_tutorials_per_group2 = []
            planning_experiments_per_group2 = []
            for group in self.group_list:
                gp_index = self.group_list.index(group)
                planning_tutorials_per_group2.append(Solution(self.planning_tutorials_group[gp_index]))
                planning_experiments_per_group2.append(Solution(self.planning_experiments_group[gp_index]))


            for teacher in self.teacher_list:
                out += ('\n\n\n' + teacher['name'] + ': \n')
                total_teacher_hours = []
                for week in range(self.N):
                    hours = get_teacher_hours(teacher,
                                          self.group_list,
                                          self.promo_list2,
                                          week,
                                          planning_lectures_per_promo2,
                                          planning_tutorials_per_group2,
                                          planning_experiments_per_group2,
                                          self.lecture_list_per_promo2,
                                          self.tutorial_list_per_group2,
                                          self.experiment_list_per_group2)
                    total_teacher_hours.append(hours)
                out += "Total"

                # Sum lecture from planning_lectures
                # + tutorial from planning_tutorials_teacher
                # + experiment hours from planning_experiment_teacher
                out += str(total_teacher_hours)


            # Instantiate lists containing total of lectures/tutorials/experiments hours per week and per group
            total_hours_group_list = []
            total_lecture_hours_group_list_undup = []
            total_tutorial_hours_group_list = []
            total_experiment_hours_group_list = []
            total_tutorial_hours_group_list_per_room = []
            total_experiment_hours_group_list_per_room = []

            # ----------------------- #
            # ----- Group Test ------ #
            # ----------------------- #

            out += "\n\n"
            out += "\n\n        # ----------------------- #"
            out += "\n\n        # ----- Group Test ------ #"
            out += "\n\n        # ----------------------- #"
            group_index = 0
            promo_index = 0

            for promo in self.promo_list:

                checked_subject = []

                for group in self.promo_list[promo]:
                    out += ('\n\nGroup ' + str(group_index + 1) + ': \n')

                    # Instantiate lists containing total of lectures/tutorials/experiments hours per week for one group
                    total_lecture_hours_one_group = []
                    total_lecture_hours_one_group_undup = []
                    total_tutorial_hours_one_group = []
                    total_experiment_hours_one_group = []
                    total_tutorial_hours_one_group_per_room = []
                    total_experiment_hours_one_group_per_room = []
                    total_hours_one_group = []
                    checked_subject_weekly = []

                    for week in range(len(self.planning_lectures_per_promo[promo_index].col)):
                        hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours, \
                            subject_treated, hours_tutorials_per_type_room, hours_experiments_per_type_room = \
                            get_group_hours(group,
                                            group_index,
                                            self.index_group_list,
                                            week,
                                            Solution(self.planning_lectures_per_promo[promo_index]),
                                            Solution(self.planning_tutorials_group[group_index]),
                                            Solution(self.planning_experiments_group[group_index]),
                                            checked_subject)

                        # Add total of lectures/tutorials/experiments hours for one week in the current group' lists
                        total_lecture_hours_one_group_undup.append(unduplicated_lecture_hours)
                        total_lecture_hours_one_group.append(hours_lectures)
                        total_tutorial_hours_one_group.append(hours_tutorials)
                        total_experiment_hours_one_group .append(hours_experiments)
                        total_tutorial_hours_one_group_per_room.append(hours_tutorials_per_type_room)
                        total_experiment_hours_one_group_per_room .append(hours_experiments_per_type_room)
                        total_hours_one_group.append(hours_total)

                        for subject in subject_treated:
                            if (subject not in checked_subject_weekly) and (subject != []):
                                checked_subject_weekly.append(subject)

                    # Print details of the current group
                    out += "Lectures" + str(total_lecture_hours_one_group)
                    out += "\nTutorial" + str(total_tutorial_hours_one_group)
                    out += "\nExperiments" + str(total_experiment_hours_one_group)
                    out += "\n\nTotal" + str(total_hours_one_group)
                    out += "\n\n"

                    # Add details of one group in the groups' lists
                    total_lecture_hours_group_list_undup.append(total_lecture_hours_one_group_undup)
                    total_tutorial_hours_group_list.append(total_tutorial_hours_one_group)
                    total_experiment_hours_group_list.append(total_experiment_hours_one_group)
                    total_tutorial_hours_group_list_per_room.append(total_tutorial_hours_one_group_per_room)
                    total_experiment_hours_group_list_per_room.append(total_experiment_hours_one_group_per_room)
                    total_hours_group_list.append(total_hours_one_group)

                    for subject in checked_subject_weekly:
                        if subject not in checked_subject:
                            checked_subject.append(subject)
                    group_index += 1
                promo_index += 1

            # ---------------------- #
            # ----- Room Test ------ #
            # ---------------------- #

            rooms_lectures, rooms_tutorials, rooms_experiments = get_list_rooms_according_type_hours(self.rooms_list)
            # union_lectures_tutorials, union_lectures_experiments, union_tutorials_experiments =
            # get_union_list_rooms_according_type_hours(rooms_list)

            # Lists containing total of lectures/tutorials/experiments hours per week
            total_hours_lecture = get_total_hours_week(total_lecture_hours_group_list_undup)
            total_hours_tutorial = get_total_hours_week(total_tutorial_hours_group_list)
            total_hours_experiment = get_total_hours_week(total_experiment_hours_group_list)
            total_hours_tutorial_per_room = get_total_hours_week_per_type_room(total_tutorial_hours_group_list_per_room, self.N)
            total_hours_experiment_per_room = get_total_hours_week_per_type_room(total_experiment_hours_group_list_per_room, self.N)

            # # Lists containing sum total of lectures/tutorials/experiments per week
            total_hours_union_lecture_tutorial = get_total_hours_week([total_hours_lecture, total_hours_tutorial])
            total_hours_union_lecture_experiment = get_total_hours_week([total_hours_lecture, total_hours_experiment])
            total_hours_union_tutorial_experiment = get_total_hours_week_per_type_room([total_hours_tutorial_per_room, total_hours_experiment_per_room], self.N)
            out += "\n\n"
            out += "\n\n        # ---------------------- #"
            out += "\n\n        # ----- Room Test ------ #"
            out += "\n\n        # ---------------------- #"
            out += "\n\nTotal hours lecture: " + str(total_hours_lecture)
            out += "\nTotal hours tutorial: " + str(total_hours_tutorial)
            out += "\nDetail rooms for hours tutorial: " + str(total_hours_tutorial_per_room)
            out += "\nTotal hours experiment: " + str(total_hours_experiment)
            out += "\nDetail rooms for experiment: " + str(total_hours_experiment_per_room)
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


default = {'solver': 'Mistral2', 'N': 30, 'var': 'MinDomain',
           'val': 'RandomMinMax', 'restart': 'yes', 'rand': 2, 'verbose': 0, 'cutoff': 20}

if __name__ == '__main__':
    params = input(default)
    planning = Planning()
    print(planning.solve(params))
