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

        # Rooms #
        value_type_room = ['Automate', 'CS', 'IOT', 'Security', 'Normal']
        room_1 = {'name': "GEI 15", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'type_room': value_type_room[4]}
        room_2 = {'name': "GEI 13", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'type_room': value_type_room[4]}
        room_3 = {'name': "GEI 111", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True, 'type_room': value_type_room[1]}
        room_4 = {'name': "GEI 101", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True, 'type_room': value_type_room[3]}
        room_5 = {'name': "GEI 213", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'type_room': value_type_room[4]}
        rooms_list = [room_1, room_2, room_3, room_4, room_5]

        # Courses #
        course_1 = {'name': 'math', 'lecture': 40, 'tutorial': 5, 'experiment': 0, 'type_room': value_type_room[4]}
        course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 15, 'type_room': value_type_room[1]}
        course_3 = {'name': 'Security', 'lecture': 10, 'tutorial': 0, 'experiment': 5, 'type_room': value_type_room[3]}
        course_4 = {'name': 'English', 'lecture': 20, 'tutorial': 0, 'experiment': 0, 'type_room': value_type_room[4]}
        course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial': 0, 'experiment': 0, 'type_room': value_type_room[4]}
        course_list = [course_1, course_2, course_3, course_4, course_5]

        # Groups #
        group_1 = {'name': "4IR-A", 'course_list': [course_1, course_2], 'promo': "1"}
        group_2 = {'name': "4IR-B", 'course_list': [course_1, course_2], 'promo': "1"}
        group_3 = {'name': "4IR-C", 'course_list': [course_3, course_5], 'promo': "2"}
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

        return course_list, teacher_list, group_list, rooms_list, value_type_room
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
