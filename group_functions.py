from course_functions import *


def list_index_lesson_group(group, lesson_type, lesson_list):
    index_list = []
    for course in group['course_list']:
        if course[lesson_type] > 0:
            index_list.append({'index': find_index_lesson_list(lesson_list, course), 'number_of': course[lesson_type]})

    return index_list


def get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                    planning_experiments):
    hours = 0
    group = index_group_list[group_index]

    for lecture in group['index_lecture_list']:
        hours += planning_lectures[lecture['index']][week]
    for tutorial in group['index_tutorial_list']:
        hours += planning_tutorials[tutorial['index']][week]
    for experiment in group['index_experiment_list']:
        hours += 2 * planning_experiments[experiment['index']][week]

    return hours