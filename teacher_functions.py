from course_functions import *


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

    course_list = teacher['course_list']
    for course in course_list:
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
