from course_functions import *


def check_common_lectures(group_list, lecture_list, number_of_weeks):
    checked_course_list = []
    total_lecture_hours = []
    for group in group_list:
        for course in group['course_list']:
            if course not in checked_course_list:
                None


            #    course_lecture_hours.course += total_lecture_hours
            #    checked_course_list.append(course)

    return total_lecture_hours


def list_index_lesson_group(group, lesson_type, lesson_list):
    index_list = []
    for course in group['course_list']:
        if course[lesson_type] > 0:
            index_list.append({'index': find_index_lesson_list(lesson_list, course), 'number_of': course[lesson_type]})

    return index_list


def get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                    planning_experiments):
    hours_lectures = 0
    hours_tutorials = 0
    hours_experiments = 0
    group = index_group_list[group_index]

    for lecture in group['index_lecture_list']:
        hours_lectures += planning_lectures[lecture['index']][week]
    for tutorial in group['index_tutorial_list']:
        hours_tutorials += planning_tutorials[tutorial['index']][week]
    for experiment in group['index_experiment_list']:
        hours_experiments += 2 * planning_experiments[experiment['index']][week]

    hours_total = hours_lectures + hours_tutorials + hours_experiments
    return hours_lectures, hours_tutorials, hours_experiments, hours_total
