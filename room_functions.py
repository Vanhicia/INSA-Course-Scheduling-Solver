from Numberjack import *
import collections, functools, operator

# Sum column of a matrix
def sum_column(matrix):
    return [sum(x) for x in zip(*matrix)]


# Return a list containing total of hours per week
def get_total_hours_week(total_group):
        return sum_column(total_group)


def get_total_hours_week_per_type_room(total_group, number_of_week):
    res = []

    for week in range(number_of_week):
        column = []
        for group in total_group:
            column.append(group[week])
        res.append(dict(functools.reduce(operator.add, map(collections.Counter, column))))
    return res


# Return 3 lists
# lectures: list containing rooms that are for lectures
# tutorials: list containing rooms that are for tutorials
# experiments: list containing rooms that are for experiments
def get_list_rooms_according_type_hours(all_rooms_list):
    lectures = []
    tutorials = []
    experiments = []

    for room in all_rooms_list:
        if room['is_for_lecture']:
            lectures.append(room)
        if room['is_for_tutorial']:
            tutorials.append(room)
        if room['is_for_experiment']:
            experiments.append(room)

    return lectures, tutorials, experiments


# Return 3 lists
# lectures_tutorials: list containing rooms that are for lectures/tutorials
# lectures_experiments: list containing rooms that are for lectures/experiments
# tutorials_experiments: list containing rooms that are for tutorials/experiments
def get_union_list_rooms_according_type_hours(all_rooms_list):

    lectures_tutorials = []
    tutorials_experiments = []
    lectures_experiments = []

    for room in all_rooms_list:
        if room['is_for_lecture']:
            if room not in lectures_experiments:
                lectures_experiments.append(room)
            if room not in lectures_tutorials:
                lectures_tutorials.append(room)
        if room['is_for_tutorial']:
            if room not in lectures_tutorials:
                lectures_tutorials.append(room)
            if room not in tutorials_experiments:
                tutorials_experiments.append(room)
        if room['is_for_experiment']:
            if room not in lectures_experiments:
                lectures_experiments.append(room)
            if room not in tutorials_experiments:
                tutorials_experiments.append(room)

    return lectures_tutorials, lectures_experiments, tutorials_experiments


def get_list_rooms_per_type(room_list, value_type_room):
    res = {}
    for room in room_list:
        for type_room in value_type_room:
            if type_room == room['type_room']:
                if type_room in res:
                    res[type_room] +=1
                else:
                    res.update({type_room: 1})
    return res


# Check if hours are less than resources of a room and per week
def is_lesson_hours_lt_resources(total_hours, nb_rooms, nb_resources):
    return [week <= (nb_rooms*nb_resources) for week in total_hours]


def is_lesson_hours_lt_resources_one_week(week, nb_rooms, nb_resources):
    return [week <= (nb_rooms*nb_resources)]
