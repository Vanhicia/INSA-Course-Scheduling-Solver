from course_functions import *


def get_promos(group_list):  # takes a group list, returns a promo list
    promo_list = {}
    checked_promo = []
    for group in group_list:
        promo_index = str(group['promo'])
        if promo_index not in checked_promo:
            checked_promo.append(promo_index)
            current_promo = []
            current_promo.append(group)
            promo_list[promo_index] = current_promo
        else:
            promo_list[promo_index].append(group)
    return promo_list


def list_index_lesson_group(group, lesson_type, lesson_list):
    index_list = []
    for course in group['course_list']:
        if course[lesson_type] > 0:
            index_list.append({'name': course['name'], 'index': find_index_lesson_list(lesson_list, course),
                               'number_of': course[lesson_type]})

    return index_list


def get_group_hours(group_info, group_index, index_group_list, week,
                    planning_lectures_per_promo, planning_tutorials,
                    planning_experiments, checked_subject):
    hours_lectures = 0
    hours_tutorials = 0
    hours_tutorials_per_type_room = {}
    hours_experiments = 0
    hours_experiments_per_type_room = {}
    unduplicated_lecture_hours = 0
    group = index_group_list[group_index]
    subject_treated = []

    for lecture in group['index_lecture_list']:

        # in order to not count twice lectures that are followed by two groups at the same time,
        # we check if the current lesson was already accounted
        # (we assume that the checked subject list is reset for each promo)
        # if not, then we know the current lecture was never accounted before and we add it to "unduplicated_lectures"
        if lecture['name'] not in checked_subject:
            unduplicated_lecture_hours += planning_lectures_per_promo[lecture['index']][week]
            subject_treated.append(lecture['name'])

    for tutorial in group['index_tutorial_list']:
        hours_tutorials += planning_tutorials[tutorial['index']][week]
        course = group_info['course_list'][tutorial['index']]
        if course['type_room'] in hours_tutorials_per_type_room.keys():
            hours_tutorials_per_type_room[course['type_room']] += planning_tutorials[tutorial['index']][week]
        else:
            hours_tutorials_per_type_room.update({course['type_room']: planning_tutorials[tutorial['index']][week]})

    for experiment in group['index_experiment_list']:
        hours_experiments += 2 * planning_experiments[experiment['index']][week]
        course = group_info['course_list'][experiment['index']]
        if course['type_room'] in hours_experiments_per_type_room.keys():
            hours_experiments_per_type_room[course['type_room']] += planning_experiments[experiment['index']][week]
        else:
            hours_experiments_per_type_room.update({course['type_room']: planning_experiments[experiment['index']]
                                                    [week]})
    hours_total = hours_lectures + hours_tutorials + hours_experiments

    return hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours, \
        subject_treated, hours_tutorials_per_type_room, hours_experiments_per_type_room

