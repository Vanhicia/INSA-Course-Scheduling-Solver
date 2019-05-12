from course_functions import *


def list_index_lesson_group(group, lesson_type, lesson_list):
    index_list = []
    for course in group['course_list']:
        if course[lesson_type] > 0:
            index_list.append({'name': course['name'], 'index': find_index_lesson_list(lesson_list, course), 'number_of': course[lesson_type]})

    return index_list

# TODO: implementer les "accounted classes" qui pourraient nous permettre d'avoir des groupes dans une meme promo
#  qui n'ont pas les mêmes cours


def get_group_hours(group_index, index_group_list, week, planning_lectures, planning_tutorials,
                    planning_experiments, checked_subject):
    hours_lectures = 0
    hours_tutorials = 0
    hours_experiments = 0
    unduplicated_lecture_hours = 0
    group = index_group_list[group_index]
    subject_treated = []

    for lecture in group['index_lecture_list']:
        hours_lectures += planning_lectures[lecture['index']][week]

        # in order to not count twice lectures that are followed by two groups at the same time,
        # we check if the current lesson was already accounted
        # (we assume that the checked subject list is reset for each promo)
        # if not, then we know the current lecture was never accounted before and we add it to "unduplicated_lectures"
        if lecture['name'] not in checked_subject:
            unduplicated_lecture_hours += planning_lectures[lecture['index']][week]
            subject_treated.append(lecture['name'])
    for tutorial in group['index_tutorial_list']:
        hours_tutorials += planning_tutorials[tutorial['index']][week]
    for experiment in group['index_experiment_list']:
        hours_experiments += 2 * planning_experiments[experiment['index']][week]

    hours_total = hours_lectures + hours_tutorials + hours_experiments
    return hours_lectures, hours_tutorials, hours_experiments, hours_total, unduplicated_lecture_hours, subject_treated
