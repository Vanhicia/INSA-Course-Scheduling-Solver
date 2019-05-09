

# parameters: lecture/tutorial/experiment list, course
# return the index of the course in the lecture/tutorial/experiment list
def find_index_lesson_list(lesson_list, course):
    k = 0
    for lesson in lesson_list:
        if lesson[0] == course['name']:
            return k
        k += 1

# for course_y, tutorials/experiments can start only after x lectures at least
def exercises_only_after_x_lectures(course, lecture_list, exercise_list, nb_lec, x):
     id_lec = find_index_lesson_list(lecture_list, course)
     id_exe = find_index_lesson_list(exercise_list, course)
     return x, id_lec, id_exe, nb_lec