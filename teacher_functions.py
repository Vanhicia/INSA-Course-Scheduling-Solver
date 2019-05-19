

# get teacher hours for a specific week
# Format : get_teacher_hours( teacher id, list of teachers by id, week, plannings * 3 )
# TODO : add parameters for planning lecture
def get_teacher_hours(teacher, group_list, promo_list, week, list_planning_tutorials_per_group, list_planning_experiments_per_group,
                      tutorial_list_per_group2, experiment_list_per_group2):
    hours = 0
    for course in teacher['course_list']:

        # for promo in course['lecture_promo']:
        #     promo_index = promo_list.index(promo)
        #     lect_index = lecture_list_per_promo2[promo_index].index(course)
        #     hours += (list_planning_lectures_per_promo[promo_index])[lect_index][week]

        for group in course['tutorial_gp']:
            gp_index = group_list.index(group)
            tuto_index = tutorial_list_per_group2[gp_index].index(course['course'])
            hours += (list_planning_tutorials_per_group[gp_index])[tuto_index][week]

        for group in course['experiment_gp']:
            gp_index = group_list.index(group)
            exp_index = experiment_list_per_group2[gp_index].index(course['course'])
            hours += 2 * (list_planning_experiments_per_group[gp_index])[exp_index][week]

    return hours


# compute the available slot number when a teacher is partially absent during a week,
# from the absence day number and the maximum of slots per week
def compute_slot_number(absence_day_number, max_hours):
    total_day_number = 5
    slots = 0
    if absence_day_number < total_day_number:
        slots = int(max_hours*((total_day_number-absence_day_number)/total_day_number))
    return slots
