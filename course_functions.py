

# parameters: lecture/tutorial/experiment list, course
# return the index of the course in the lecture/tutorial/experiment list
def find_index_lesson_list(lesson_list, course):
    k = 0
    for lesson in lesson_list:
        if lesson[0] == course['name']:
            return k
        k += 1

# for course_y, tutorials/experiments can start only after x lectures at least
def exercises_only_after_x_lectures(course, lecture_list, exercise_list):
     id_lec = find_index_lesson_list(lecture_list, course)
     id_exe = find_index_lesson_list(exercise_list, course)
     return id_lec, id_exe

def cst_specific_tut(spe_cst, lecture_list, exercise_list, promo_list, group_list, planning_tutorials_per_group,
                 planning_lectures_per_promo,limit_hours_course_for_lectures, number_of_weeks, model):
    promo_index = 0
    for promo in promo_list:
        for group in promo_list[promo]:
            if spe_cst['course']['tutorial'] > 0:
                nbr_group = group_list.index(group)
                nb_lec = spe_cst['course']['lecture']
                (id_lec, id_exe) = exercises_only_after_x_lectures(spe_cst['course'], lecture_list[promo_index],
                                                                              exercise_list[nbr_group])
                if len(planning_tutorials_per_group[nbr_group]) > 0:
                    x = spe_cst['nb_min']
                    if (x < nb_lec):
                        limit_lesson = (int(x / limit_hours_course_for_lectures)+1,
                                        int(x / limit_hours_course_for_lectures))[float(
                            int(x /limit_hours_course_for_lectures)) == x / limit_hours_course_for_lectures]

                        nb = (int(x/limit_lesson)+1,int(x/limit_lesson))[float(
                            int(x /limit_lesson)) == x / limit_lesson]

                        for i in range(limit_lesson):
                            model += (planning_tutorials_per_group[nbr_group][id_exe][i] == 0)
                            model += (planning_lectures_per_promo[promo_index][id_lec][i] >= nb)

                    elif (nb_lec < limit_hours_course_for_lectures):
                        model += (planning_tutorials_per_group[nbr_group][id_exe][0] == 0)
                        model += (planning_lectures_per_promo[promo_index][id_lec][0] == nb_lec)

        promo_index += 1


def cst_specific_exp(spe_cst, lecture_list, exercise_list, promo_list, group_list, planning_experiments_per_group,
                     planning_lectures_per_promo, limit_hours_course_for_lectures, number_of_weeks, model):
    promo_index = 0
    for promo in promo_list:
        for group in promo_list[promo]:
            if spe_cst['course']['experiment'] > 0:
                nbr_group = group_list.index(group)
                nb_lec = spe_cst['course']['lecture']
                (id_lec, id_exe) = exercises_only_after_x_lectures(spe_cst['course'], lecture_list[promo_index],
                                                                   exercise_list[nbr_group])
                if len(planning_experiments_per_group[nbr_group]) > 0:
                    x = spe_cst['nb_min']
                    if (x < nb_lec):
                        limit_lesson = (int(x / limit_hours_course_for_lectures) + 1,
                                        int(x / limit_hours_course_for_lectures))[float(
                            int(x / limit_hours_course_for_lectures)) == x / limit_hours_course_for_lectures]

                        nb = (int(x / limit_lesson) + 1, int(x / limit_lesson))[float(
                            int(x / limit_lesson)) == x / limit_lesson]

                        for i in range(limit_lesson):
                            model += (planning_experiments_per_group[nbr_group][id_exe][i] == 0)
                            model += (planning_lectures_per_promo[promo_index][id_lec][i] >= nb)

                    elif (nb_lec < limit_hours_course_for_lectures):
                        model += (planning_experiments_per_group[nbr_group][id_exe][0] == 0)
                        model += (planning_lectures_per_promo[promo_index][id_lec][0] == nb_lec)

        promo_index += 1


