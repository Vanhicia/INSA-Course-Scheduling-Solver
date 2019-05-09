from Numberjack import *


# Sum column of a matrix
def sum_column(matrix):
    return [Sum(x) for x in zip(*matrix)]


# Return a list containing total of hours per week
def get_total_hours_week(total_group):
    return sum_column(total_group)


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


# Check if hours are less than resources of a room and per week
def is_lesson_hours_lt_resources(total_hours, nb_rooms, nb_resources):
    return [week <= (nb_rooms*nb_resources) for week in total_hours]