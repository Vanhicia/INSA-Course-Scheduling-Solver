from course_functions import *


# # parameters: teacher, 'lecture'/'tutorial'/'experiment', course list
# # return the index list of ?
# def list_index_lesson(teacher, lesson_type, lesson_list):
#     index_list = []
#
#     if lesson_type == 'lecture':
#         type_gp_nb = 'lecture_gp_nb'
#     elif lesson_type == 'tutorial':
#         type_gp_nb = 'tutorial_gp_nb'
#     elif lesson_type == 'experiment':
#         type_gp_nb = 'experiment_gp_nb'
#     else:
#         raise ValueError("'lesson_type' can only be either 'lecture','tutorial' or 'experiment'")
#
#     course_list = teacher['course_list']
#     for course in course_list:
#         if course[type_gp_nb] > 0:
#             index_list.append({'index': find_index_lesson_list(lesson_list, course['course']),
#                                'gp_nb': course[type_gp_nb]})
#
#     return index_list
#
#
# # get teacher hours for a specific week
# # Format : get_teacher_hours( teacher id, list of teachers by id, week, plannings * 3 )
# def get_teacher_hours(teacher_index, index_teacher_list, week, planning_lectures, planning_tutorials,
#                       planning_experiments):
#     hours = 0
#     teacher = index_teacher_list[teacher_index]
#
#     for lecture in teacher['index_lecture_list']:
#         hours += lecture['gp_nb'] * planning_lectures[lecture['index']][week]
#     for tutorial in teacher['index_tutorial_list']:
#         hours += tutorial['gp_nb'] * planning_tutorials[tutorial['index']][week]
#     for experiment in teacher['index_experiment_list']:
#         hours += experiment['gp_nb'] * 2 * planning_experiments[experiment['index']][week]
#
#     return hours

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
