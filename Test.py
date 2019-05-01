import DataFileManager


# Set of data that can accessed by their id n
def data_set(n):
    # Format
    # Course : {name:bla, lecture : 0, tutorial:0, experiment:0}
    # Group: {'name': "gpA", 'course_list': [course_1, course_2]}
    # Teacher: {'name':"Michel Dumont", 'course_list' : [
    #                              {course:course_n , lecture_gp_nb: 0, tutorial_gp_nb: 0, experiment_gp_nb: 0}]}

    if n == 1:
        fi = DataFileManager.DataFileManager("test.json")
        fi.load_file()

        return fi.get_data()

    elif n == 2:

        # Courses #
        course_1 = {'name': 'math', 'lecture': 40, 'tutorial': 0, 'experiment': 0}
        course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 15}
        course_3 = {'name': 'Chemistry', 'lecture': 10, 'tutorial': 0, 'experiment': 0}
        course_4 = {'name': 'English', 'lecture': 20, 'tutorial': 0, 'experiment': 0}
        course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial': 0, 'experiment': 0}
        course_list = [course_1, course_2, course_3, course_4, course_5]

        # Groups #
        group_1 = {'name': "4IR-A", 'course_list': [course_1, course_2]}
        group_2 = {'name': "4IR-B", 'course_list': [course_2, course_3]}
        group_3 = {'name': "4IR-C", 'course_list': [course_4, course_5]}
        group_list = [group_1, group_2, group_3]

        # Teachers #
        teacher_1 = {'name': "Michel Dumont", 'course_list': [
                         {'course': course_1, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0},
                         {'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 1}]}
        teacher_2 = {'name': "Hélène Michou", 'course_list': [
                         {'course': course_2, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 0}]}
        teacher_3 = {'name': "Benoit Jardin", 'course_list': [
                         {'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 2}]}
        teacher_4 = {'name': "Kate Stuart", 'course_list': [
                         {'course': course_3, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
        teacher_5 = {'name': "Hervé Vieux", 'course_list': [
                         {'course': course_4, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
        teacher_6 = {'name': "Christiane Colin", 'course_list': [
                         {'course': course_5, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
        teacher_list = [teacher_1, teacher_2, teacher_3, teacher_4, teacher_5, teacher_6]

        return course_list,teacher_list,group_list
    elif n == 3:
        pass

if __name__ == '__main__':
    cou,tea,gro = data_set(2)
    for i in cou:
        print(i)
    print()
    for i in tea:
        print(i)
    print()
    for i in gro:
        print(i)