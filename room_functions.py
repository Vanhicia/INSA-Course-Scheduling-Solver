
def sum_column(planning):
    return [sum(x) for x in zip(*planning)]


# def get_total_hours_week(planning_lectures, planning_tutorials, planning_experiments, nb_weeks):
#     res = [0]*nb_weeks
#     hours_lectures = sum_column(planning_lectures)
#     hours_tutorials = sum_column(planning_tutorials)
#     hours_experiments = sum_column(planning_experiments)
#
#     for i in range(nb_weeks):
#         res[i] = hours_lectures[i] + hours_tutorials[i] + hours_experiments[i]
#     return res

def get_total_hours_week(total_group):
    return sum_column(total_group)


def is_lesson_hours_lt_resources(total_hours, nb_rooms, nb_resources):
    return [week <= (nb_rooms*nb_resources) for week in total_hours]
