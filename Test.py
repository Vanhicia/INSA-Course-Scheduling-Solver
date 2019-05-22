# coding=utf-8
import DataFileManager
import group_functions


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
        # value type room for lectures is 'Normal'
        # the following list and 'type_room' key are only for tutorials and experiments
        value_type_room = ['Automate', 'CS', 'IOT', 'Security', 'Normal']
        room_1 = {'name': "GEI 15", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': True, 'type_room': value_type_room[0]}
        room_2 = {'name': "GEI 13", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'type_room': value_type_room[0]}
        room_3 = {'name': "GEI 111", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True, 'type_room': value_type_room[1]}
        room_4 = {'name': "GEI 101", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True, 'type_room': value_type_room[3]}
        room_5 = {'name': "GEI 213", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False, 'type_room': value_type_room[0]}
        rooms_list = [room_1, room_2, room_3, room_4, room_5]

        # Courses #
        course_1 = {'name': 'math', 'lecture': 40, 'tutorial': 5, 'experiment': 5, 'type_room': value_type_room[0]}
        course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 0, 'type_room': value_type_room[1]}
        course_3 = {'name': 'Security', 'lecture': 10, 'tutorial': 0, 'experiment': 10, 'type_room': value_type_room[3]}
        course_4 = {'name': 'English', 'lecture': 20, 'tutorial': 0, 'experiment': 0, 'type_room': value_type_room[2]}
        course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial': 0, 'experiment': 0, 'type_room': value_type_room[2]}
        course_list = [course_1, course_2, course_3, course_4, course_5]

        # Groups #
        group_1 = {'name': "4IR-A", 'course_list': [course_1, course_2], 'promo': "1"}
        group_2 = {'name': "4IR-B", 'course_list': [course_1, course_2, course_5], 'promo': "1"}
        group_3 = {'name': "4IR-C", 'course_list': [course_3, course_4, course_5], 'promo': "2"}
        group_4 = {'name': "4IR-D", 'course_list': [course_1, course_4, course_5], 'promo': "2"}
        group_list = [group_1, group_2, group_3, group_4]

        # Promo #
        promo_1 = [group_1, group_2]
        promo_2 = [group_3, group_4]
        promo_list = group_functions.get_promos(group_list)
        promo_list2 = [ promo_1, promo_2]

        # Teachers #
        teacher_1 = {'name': "Michel Dumont", 'course_list': [
                        {'course': course_1, 'lecture_promo': [ promo_1], 'tutorial_gp': [group_1, group_2], 'experiment_gp': [group_1]},
                        {'course': course_2, 'lecture_promo': [], 'tutorial_gp': [group_2], 'experiment_gp': []}]}

        teacher_2 = {'name': "Hélène Michou", 'course_list': [
                        {'course': course_1, 'lecture_promo': [promo_2], 'tutorial_gp': [group_4], 'experiment_gp': [group_2, group_4]},
                        {'course': course_2, 'lecture_promo': [ promo_1], 'tutorial_gp': [group_1], 'experiment_gp': []}]}

        teacher_3 = {'name': "Benoit Jardin", 'course_list': [
                        {'course': course_2, 'lecture_promo': [], 'tutorial_gp': [group_2], 'experiment_gp': []}]}

        teacher_4 = {'name': "Kate Stuart", 'course_list': [
                        {'course': course_3, 'lecture_promo': [promo_2], 'tutorial_gp': [], 'experiment_gp': [group_3]}]}

        teacher_5 = {'name': "Hervé Vieux", 'course_list': [
                        {'course': course_4, 'lecture_promo': [promo_2], 'tutorial_gp': [], 'experiment_gp': []}]}

        teacher_6 = {'name': "Christiane Colin", 'course_list': [
                        {'course': course_1, 'lecture_promo': [promo_1, promo_2], 'tutorial_gp': [], 'experiment_gp': []}]}

        teacher_list = [teacher_1, teacher_2, teacher_3, teacher_4, teacher_5, teacher_6]

        # Teacher absences #

        # teacher_1 is not available the first week
        absence_1 = {'teacher': teacher_1, 'week': 0, 'absence_day_number': 5}

        # teacher_2 is not available the tenth week
        absence_2 = {'teacher': teacher_2, 'week': 9, 'absence_day_number': 5}

        # teacher_1 is not available 2 days during the fifth week
        absence_3 = {'teacher': teacher_1, 'week': 4, 'absence_day_number': 2}

        teacher_absence_list = [absence_1, absence_2, absence_3]

        return course_list, teacher_list, group_list, promo_list, promo_list2, rooms_list, value_type_room, teacher_absence_list

    elif n == 3:

        # Rooms #
        value_type_room = ['CM_GEI', 'CS', 'IOT', 'Security - Network', 'Automate', 'Electronic', 'CSH', 'Sport',
                           'Bib insa']
        room_1 = {'name': "GEI 15", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[0]}
        room_2 = {'name': "GEI 13", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False,
                  'type_room': value_type_room[0]}
        room_20 = {'name': "GEI 213", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False,
                   'type_room': value_type_room[0]}
        room_3 = {'name': "GEI 111A", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[1]}
        room_4 = {'name': "GEI 111B", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[1]}
        room_5 = {'name': "GEI 102A", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[1]}
        room_6 = {'name': "GEI 102B", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[1]}
        room_7 = {'name': "GEI 105", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[2]}
        room_8 = {'name': "GEI 101", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[3]}
        room_9 = {'name': "GEI 223", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                  'type_room': value_type_room[4]}
        room_10 = {'name': "GEI 224", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                   'type_room': value_type_room[4]}
        room_11 = {'name': "GEI 226", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': True,
                   'type_room': value_type_room[4]}
        room_12 = {'name': "GEI 002", 'is_for_lecture': False, 'is_for_tutorial': False, 'is_for_experiment': True,
                   'type_room': value_type_room[5]}
        room_13 = {'name': "GEI 005", 'is_for_lecture': False, 'is_for_tutorial': False, 'is_for_experiment': True,
                   'type_room': value_type_room[5]}
        room_14 = {'name': "GEI 113", 'is_for_lecture': False, 'is_for_tutorial': False, 'is_for_experiment': True,
                   'type_room': value_type_room[5]}
        room_15 = {'name': "CSH 004", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False,
                   'type_room': value_type_room[6]}
        room_16 = {'name': "CSH 006", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False,
                   'type_room': value_type_room[6]}
        room_17 = {'name': "CSH 104", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': False,
                   'type_room': value_type_room[6]}
        room_18 = {'name': "Gymnase", 'is_for_lecture': False, 'is_for_tutorial': True, 'is_for_experiment': False,
                   'type_room': value_type_room[7]}
        room_19 = {'name': "Bib - salle formation", 'is_for_lecture': False, 'is_for_tutorial': True,
                   'is_for_experiment': False,
                   'type_room': value_type_room[8]}

        rooms_list = [room_1, room_2, room_3, room_4, room_5, room_6, room_7, room_8, room_9, room_10,
                      room_11, room_12, room_13, room_14, room_15, room_16, room_17, room_18, room_19, room_20]

        # Sequencement s7 4IR 2018-2019 #
        # Tronc commun #
        course_1 = {'name': 'Conception Orientee Objets', 'lecture': 8, 'tutorial': 13, 'experiment': 0,
                    'type_room': value_type_room[1]}
        course_2 = {'name': 'Programmation Orientee Objets', 'lecture': 16, 'tutorial': 7, 'experiment': 12,
                    'type_room': value_type_room[1]}
        course_3 = {'name': 'Interconnexion de réseaux', 'lecture': 12, 'tutorial': 1, 'experiment': 3,
                    'type_room': value_type_room[3]}
        course_4 = {'name': 'Algorithmique Repartie', 'lecture': 8, 'tutorial': 0, 'experiment': 0,
                    'type_room': value_type_room[0]}
        course_5 = {'name': 'Securite informatique et dans l internet', 'lecture': 14, 'tutorial': 2, 'experiment': 3,
                    'type_room': value_type_room[3]}
        course_6 = {'name': 'Activite physique et sportive', 'lecture': 0, 'tutorial': 13, 'experiment': 0,
                    'type_room': value_type_room[7]}

        course_7 = {'name': 'Développer ses aptitudes manageriales (finance, marketing, droit)', 'lecture': 36,
                    'tutorial': 0,
                    'experiment': 0, 'type_room': value_type_room[6]}
        course_8 = {'name': 'Formation à la recherche documentaire', 'lecture': 0, 'tutorial': 2, 'experiment': 0,
                    'type_room': value_type_room[8]}
        course_9 = {'name': 'LV2/ Anglais renforce', 'lecture': 0, 'tutorial': 20, 'experiment': 0,
                    'type_room': value_type_room[6]}

        # Orientation SI #
        course_10 = {'name': 'Programmation fonctionnelle', 'lecture': 5, 'tutorial': 8, 'experiment': 4,
                     'type_room': value_type_room[1]}
        course_11 = {'name': 'Logique et programmation logique', 'lecture': 13, 'tutorial': 6, 'experiment': 4,
                     'type_room': value_type_room[1]}
        course_12 = {'name': 'Algorithmique avancee', 'lecture': 5, 'tutorial': 3, 'experiment': 0,
                     'type_room': value_type_room[1]}
        course_13 = {'name': 'Direction des systemes d information', 'lecture': 8, 'tutorial': 0, 'experiment': 0,
                     'type_room': value_type_room[0]}
        course_14 = {'name': 'Modeles de Donnees et Systemes d information', 'lecture': 11, 'tutorial': 17,
                     'experiment': 0,
                     'type_room': value_type_room[1]}
        course_15 = {'name': 'Informatique materielle: microcontroleurs', 'lecture': 1, 'tutorial': 4, 'experiment': 11,
                     'type_room': value_type_room[4]}

        # Orientation SC #
        course_16 = {'name': 'Reseaux sans fil', 'lecture': 6, 'tutorial': 2, 'experiment': 4,
                     'type_room': value_type_room[0]}
        course_17 = {'name': 'Reseaux de mobiles', 'lecture': 16, 'tutorial': 3, 'experiment': 4,
                     'type_room': value_type_room[2]}
        course_18 = {'name': 'Energie pour les systemes mobiles', 'lecture': 4, 'tutorial': 0, 'experiment': 1,
                     'type_room': value_type_room[2]}
        course_19 = {'name': 'Codage voix et image pour réseaux mobiles', 'lecture': 2, 'tutorial': 0, 'experiment': 2,
                     'type_room': value_type_room[2]}
        course_20 = {'name': 'Canaux bruites et codes correcteurs', 'lecture': 11, 'tutorial': 4, 'experiment': 0,
                     'type_room': value_type_room[2]}
        course_21 = {'name': 'BE Transmission', 'lecture': 2, 'tutorial': 0, 'experiment': 10,
                     'type_room': value_type_room[2]}
        course_22 = {'name': 'Antennes et modeles pour la transmission', 'lecture': 10, 'tutorial': 1, 'experiment': 2,
                     'type_room': value_type_room[2]}

        course_list = [course_1
                       , course_2
                       , course_3
                       , course_4
                       , course_5
                       , course_6
                       , course_7
                       , course_8
                       , course_9
                       , course_10
                       , course_11
                       , course_12
                       , course_13
                       , course_14
                       , course_15,course_16, course_17,
                       course_18, course_19, course_20, course_21, course_22
                        ]

        group_1 = {'name': '4IR-A', 'course_list': [course_1, course_2, course_3, course_4, course_5,
                                                    course_6, course_7, course_8, course_9, course_10,
                                                    course_11, course_12, course_13, course_14, course_15], 'promo': "1"}

        group_2 = {'name': '4IR-B', 'course_list': [course_1, course_2, course_3, course_4, course_5,
                                                    course_6, course_7, course_8, course_9, course_10,
                                                    course_11, course_12, course_13, course_14, course_15], 'promo': "1"}

        group_3 = {'name': '4IR-C', 'course_list': [course_1, course_2, course_3, course_4, course_5,
                                                    course_6, course_7, course_8, course_9, course_10,
                                                    course_11, course_12, course_13, course_14, course_15], 'promo': "1"}

        group_4 = {'name': '4IR-SC', 'course_list': [course_1, course_2, course_3, course_4, course_5,
                                                     course_6, course_7, course_8, course_9,
                                                     course_16, course_17, course_18, course_19, course_20,
                                                     course_21, course_22 ], 'promo': "2"}

        group_list = [group_1, group_2, group_3, group_4]

        # Promo #
        promo_1 = [group_1, group_2, group_3]  # Promo SI
        promo_2 = [group_4]                    # Promo SC
        promo_list = group_functions.get_promos(group_list)
        promo_list2 = [promo_1, promo_2]

        # Teachers #
        teacher_1 = {'name': "Nicolas Van Wambeke", 'course_list': [
            {'course': course_1, 'lecture_promo': [promo_1, promo_2], 'tutorial_gp': [group_1], 'experiment_gp': []}]}
        teacher_2 = {'name': "Sami Yangui", 'course_list': [
            {'course': course_2, 'lecture_promo': [promo_1], 'tutorial_gp': promo_1,
             'experiment_gp': [group_1, group_2]}]}
        teacher_3 = {'name': "Christophe Chassot", 'course_list': [
            {'course': course_3, 'lecture_promo': [promo_1], 'tutorial_gp': promo_1, 'experiment_gp': [group_1, group_2]}]}
        teacher_4 = {'name': "Francois Vernadat", 'course_list': [
            {'course': course_4, 'lecture_promo': [promo_1], 'tutorial_gp': [], 'experiment_gp': []}]}
        teacher_5 = {'name': "Vincent Nicomette", 'course_list': [
            {'course': course_5, 'lecture_promo': [promo_1], 'tutorial_gp': [], 'experiment_gp': []}]}
        teacher_6 = {'name': "Sylvie Rossard", 'course_list': [
            {'course': course_6, 'lecture_promo': [], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_7 = {'name': "Lucie Leclert", 'course_list': [
            {'course': course_7, 'lecture_promo': [promo_1], 'tutorial_gp': [], 'experiment_gp': []}]}
        teacher_8 = {'name': "Anne-Laure Aymard", 'course_list': [
            {'course': course_8, 'lecture_promo': [], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_9 = {'name': "Anouk Abadie", 'course_list': [
            {'course': course_9, 'lecture_promo': [], 'tutorial_gp': [group_2, group_1], 'experiment_gp': []}]}
        teacher_10 = {'name': "Joseph Shea", 'course_list': [
            {'course': course_9, 'lecture_promo': [], 'tutorial_gp': [group_3, group_4], 'experiment_gp': []}]}
        teacher_11 = {'name': "Didier Le Botlan", 'course_list': [
            {'course': course_10, 'lecture_promo': [promo_1], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_12 = {'name': "Yannick Pencolé", 'course_list': [
            {'course': course_11, 'lecture_promo': [promo_1], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_13 = {'name': "Mohamed Siala", 'course_list': [
            {'course': course_12, 'lecture_promo': [promo_1], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_14 = {'name': "Laurent Dairaine", 'course_list': [
            {'course': course_13, 'lecture_promo': [promo_1], 'tutorial_gp': [], 'experiment_gp': []}]}
        teacher_15 = {'name': "Nawal Guermouche", 'course_list': [
            {'course': course_14, 'lecture_promo': [promo_1], 'tutorial_gp': [], 'experiment_gp': []}]}
        teacher_16 = {'name': "Vincent Mahout", 'course_list': [
            {'course': course_15, 'lecture_promo': [promo_1], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_17 = {'name': "Slim Abdelatif", 'course_list': [
            {'course': course_16, 'lecture_promo': [promo_2], 'tutorial_gp': promo_2, 'experiment_gp': promo_2},
            {'course': course_3, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': [group_3, group_4]},
            {'course': course_1, 'lecture_promo': [], 'tutorial_gp': [group_3], 'experiment_gp': []}]}
        teacher_18 = {'name': "Daniela Dragomirescu", 'course_list': [
            {'course': course_17, 'lecture_promo': [promo_2], 'tutorial_gp': promo_2, 'experiment_gp': promo_2}]}
        teacher_19 = {'name': "Anne Nicolas", 'course_list': [
            {'course': course_18, 'lecture_promo': [promo_2], 'tutorial_gp': [], 'experiment_gp': promo_2}]}
        teacher_20 = {'name': "Jean-Louis Noullet", 'course_list': [
            {'course': course_19, 'lecture_promo': [promo_2], 'tutorial_gp': [], 'experiment_gp': promo_2}]}
        teacher_21 = {'name': "Alexandre Boyer", 'course_list': [
            {'course': course_20, 'lecture_promo': [promo_2], 'tutorial_gp': promo_2, 'experiment_gp': []},
            {'course': course_22, 'lecture_promo': [promo_2], 'tutorial_gp': promo_2, 'experiment_gp': promo_2}]}
        teacher_22 = {'name': "Pierre Pinel", 'course_list': [
            {'course': course_20, 'lecture_promo': [promo_2], 'tutorial_gp': promo_2, 'experiment_gp': []},
            {'course': course_1, 'lecture_promo': [], 'tutorial_gp': [group_2], 'experiment_gp': []},
            {'course': course_2, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': [group_3, group_4]}]}
        teacher_23 = {'name': "Pascal Acco", 'course_list': [
            {'course': course_21, 'lecture_promo': [promo_2], 'tutorial_gp': [], 'experiment_gp': promo_2}]}
        teacher_24 = {'name': "Eric Alata", 'course_list': [
            {'course': course_5, 'lecture_promo': [], 'tutorial_gp': promo_1, 'experiment_gp': promo_1}]}
        teacher_assistant_1 = {'name': "Doctorant 1", 'course_list': [
            {'course': course_10, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': promo_1},
            {'course': course_11, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': promo_1}]}
        teacher_assistant_2 = {'name': "Doctorant 2", 'course_list': [
            {'course': course_1, 'lecture_promo': [], 'tutorial_gp': [group_4], 'experiment_gp': []},
            {'course': course_14, 'lecture_promo': [], 'tutorial_gp': promo_1, 'experiment_gp': []}]}
        teacher_assistant_3 = {'name': "Doctorant 3", 'course_list': [
            {'course': course_15, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': [group_1, group_3]}]}
        teacher_assistant_4 = {'name': "Doctorant 4", 'course_list': [
            {'course': course_15, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': [group_2]}]}

        teacher_list = [teacher_1, teacher_2, teacher_3, teacher_4, teacher_5,
                        teacher_6, teacher_7, teacher_8, teacher_9, teacher_10,
                        teacher_11, teacher_12, teacher_13, teacher_14, teacher_15,
                        teacher_16, teacher_17, teacher_18, teacher_19, teacher_20,
                        teacher_21, teacher_22, teacher_23, teacher_24,
                        teacher_assistant_1, teacher_assistant_2, teacher_assistant_3, teacher_assistant_4
        ]

        # Teacher absences #

        # teacher_1 is not available the first week
        absence_1 = {'teacher': teacher_1, 'week': 0, 'absence_day_number': 5}

        # teacher_2 is not available the tenth week
        absence_2 = {'teacher': teacher_2, 'week': 9, 'absence_day_number': 5}

        # teacher_1 is not available 2 days during the fifth week
        absence_3 = {'teacher': teacher_1, 'week': 4, 'absence_day_number': 2}

        teacher_absence_list = [absence_1, absence_2, absence_3]

        # spe_cst_1 = {'course': course_1, 'nb_min': 8}
        # spe_cst_2 = {'course': course_2, 'nb_min': 8}
        # spe_cst_3 = {'course': course_3, 'nb_min': 6}
        # spe_cst_4 = {'course': course_4, 'nb_min': 8}
        # spe_cst_5 = {'course': course_5, 'nb_min': 8}

        # spe_cst_10 = {'course': course_10, 'nb_min': 5}
        # spe_cst_11 = {'course': course_11, 'nb_min': 5}
        # spe_cst_12 = {'course': course_12, 'nb_min': 5}
        # spe_cst_13 = {'course': course_13, 'nb_min': 5}
        # spe_cst_14 = {'course': course_14, 'nb_min': 5}
        #
        # spe_cst_16 = {'course': course_16, 'nb_min': 5}
        # spe_cst_17 = {'course': course_17, 'nb_min': 5}
        # spe_cst_18 = {'course': course_18, 'nb_min': 4}
        # spe_cst_19 = {'course': course_19, 'nb_min': 2}
        # spe_cst_20 = {'course': course_20, 'nb_min': 5}
        # spe_cst_21 = {'course': course_21, 'nb_min': 2}
        # spe_cst_22 = {'course': course_22, 'nb_min': 5}
        #
        # spe_cst_list = [spe_cst_1,spe_cst_2,spe_cst_3,spe_cst_4,spe_cst_5
        #                 ,spe_cst_10,spe_cst_12, spe_cst_13
        #                 # ,spe_cst_11
        #                 # ,spe_cst_14
        #                 # ,spe_cst_16
        #                 # ,spe_cst_17
        #                 ,spe_cst_18
        #                 ,spe_cst_19
        #                 # ,spe_cst_20
        #                 ,spe_cst_21
        #                 # ,spe_cst_22
        #                 ]

        return course_list, teacher_list, group_list, promo_list, promo_list2, rooms_list, value_type_room,\
               teacher_absence_list #, spe_cst_list


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

