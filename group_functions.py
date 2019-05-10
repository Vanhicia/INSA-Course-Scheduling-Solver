from course_functions import *
from collections import ChainMap

def list_index_lesson_group(group, lesson_type, lesson_list):
    index_list = []
    for course in group['course_list']:
        if course[lesson_type] > 0:
            index_list.append({'index': find_index_lesson_list(lesson_list, course), 'number_of': course[lesson_type]})

    return index_list

# TODO: implementer les "accounted classes" qui pourraient nous permettre d'avoir des groupes dans une meme promo
#  qui n'ont pas les mêmes cours


def get_group_hours(group_info, group_index, index_group_list, week, planning_lectures, planning_tutorials,
                    planning_experiments, checked_promo_list):
    hours_lectures = 0
    hours_tutorials = 0
    hours_tutorials_per_type_room = {}
    hours_experiments = 0
    hours_experiments_per_type_room = {}
    unduplicated_lecture_hours = 0
    group = index_group_list[group_index]
    for lecture in group['index_lecture_list']:
        hours_lectures += planning_lectures[lecture['index']][week]

        # in order to not count twice lectures that are followed by two groups at the same time,
        # we check if the current group belongs to a promotion that was already accounted
        # if not, then we know the current lecture was never accounted before and we add it to "unduplicated_lectures"
        if group['promo'] not in checked_promo_list:
            unduplicated_lecture_hours += planning_lectures[lecture['index']][week]
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
            hours_experiments_per_type_room.update({course['type_room']: planning_experiments[experiment['index']][week]})
    hours_total = hours_lectures + hours_tutorials + hours_experiments
    return hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours, hours_tutorials_per_type_room, hours_experiments_per_type_room

