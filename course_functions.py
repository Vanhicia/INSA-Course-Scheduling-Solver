

# parameters: lecture/tutorial/experiment list, course
# return the index of the course in the lecture/tutorial/experiment list
def find_index_lesson_list(lesson_list, course):
    k = 0
    for lesson in lesson_list:
        if lesson[0] == course['name']:
            return k
        k += 1