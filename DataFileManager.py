
import json
import group_functions
# Format
# course = {'name':'Sexage de poussin', 'lecture': 40, 'tutorial': 5, 'experiment': 5, 'type_room': value_type_room[0]}
# teacher_1 = {'name': "Michel Dumont", 'course_list': [
#       {'course': course_1, 'lecture_promo': [promo_1], 'tutorial_gp': [group_1, group_2], 'experiment_gp': [group_1]},
#       {'course': course_2, 'lecture_promo': [], 'tutorial_gp': [group_2], 'experiment_gp': []}]}
# Group : {'name': "4IR-A", 'course_list': [course_1, course_2], 'promo': "1"}
# room = {'name': "GEI 15", 'is_for_lecture': True, 'is_for_tutorial': True, 'is_for_experiment': True, 'type_room': 'Normal'}
# value_type_room = ['Automate', 'CS', 'IOT', 'Security', 'Normal']
# promo_list = {'1': [group_1, group_2], '2'::[]}
# absence = {'teacher': teacher_1, 'week': 0, 'absence_day_number': 5}

# Class : DataFileManager(filename)
# Attributes : courses, teachers, groups, filename
# Methods :   - load_file()                                ==> Load data from filename
#             - store_file()                               ==> Store data to filename
#             - get_data()
#             - add_course(name, lect, tut, exp)
#             - add_teacher(name)
#             - add_teacher_course(name, course_name, nb_lect, nb_tut, nb_exp)
#             - add_group(name)
#             - add_group_course(group, course)
#             - rem_course(course_name)
#             - rem_teacher(teacher_name)
#             - rem_teacher_course(teacher_name, course_name)
#             - rem_group(group_name)
#             - rem_group_course(group, course)

# Function : test_json() ==> Store default data to test.json

class DataFileManager:

    courses = []
    teachers = []
    groups = []
    rooms = []
    room_types = []
    promos = []
    teacher_absence_list = []

    slots = 30
    number_of_weeks = 0
    resource_per_room = 7
    limit_hours_per_course = {}

    filename = ""

    def __init__(self, filename):
        self.filename = filename

    # Load data from a file
    def load_file(self):
        JSON_file = open(self.filename, "r")
        data = json.load(JSON_file)
        self.courses = data[0]
        self.teachers = data[1]
        self.groups = data[2]
        self.rooms = data[3]
        self.room_types = data[4]
        self.teacher_absence_list = data[5]
        self.slots = data[6]
        self.number_of_weeks = data[7]
        self.resource_per_room = data[8]
        self.limit_hours_per_course = data[9]

    # Generating file with object's data
    def store_file(self):
        py_object = [self.courses, self.teachers, self.groups,self.rooms, self.room_types, self.teacher_absence_list, self.slots, self.number_of_weeks, self.resource_per_room,self.limit_hours_per_course]
        JSON_file = open(self.filename, "w")
        JSON_file.write(json.dumps(py_object))

    def get_data(self):
        promos = group_functions.get_promos(self.groups)
        return self.courses, self.teachers, self.groups, promos, self.rooms, self.room_types, self.teacher_absence_list, self.slots, self.number_of_weeks, self.resource_per_room,self.limit_hours_per_course

    def set_slots(self, nb):
        self.slots = nb

    def set_nb_weeks(self, nb):
        self.number_of_weeks = nb

    def set_ressource_room(self, nb):
        self.resource_per_room = nb

    @staticmethod
    def check_teacher_group( teacher_list, group_list):
        grp_lec = {}
        grp_tut = {}
        grp_exp = {}

        # Make group lists of courses by groups
        for grp in group_list:
            for cs in grp['course_list']:
                #Lecture
                if cs["lecture"]!=0:
                    if cs['name'] not in grp_lec:
                        grp_lec[cs['name']]=[]
                    grp_lec[cs['name']].append(grp['name'])

                #Tutorial
                if cs["tutorial"]!=0:
                    if cs['name'] not in grp_tut:
                        grp_tut[cs['name']]=[]
                    grp_tut[cs['name']].append(grp['name'])

                #Experiments
                if cs["experiment"]!=0:
                    if cs['name'] not in grp_exp:
                        grp_exp[cs['name']]=[]
                    grp_exp[cs['name']].append(grp['name'])

        # Make group lists of courses by teachers
        tea_lec = {}
        tea_tut = {}
        tea_exp = {}
        promo_list = group_functions.get_promos(group_list)
        for tea in teacher_list:
            for cs in tea["course_list"]:

                if cs["lecture_promo"]:
                    if cs["course"]['name'] not in tea_lec:
                        tea_lec[cs["course"]['name']]=[]

                    for promo in cs['lecture_promo']:
                        for grp in promo_list[str(promo)]:
                            if cs['course'] in grp["course_list"]:
                                tea_lec[cs["course"]['name']].append(grp["name"])

                if cs["tutorial_gp"]:
                    if cs["course"]['name'] not in tea_tut:
                        tea_tut[cs["course"]['name']]=[]
                    for grp in cs['tutorial_gp']:
                        tea_tut[cs["course"]['name']].append(grp["name"])

                if cs["experiment_gp"]:
                    if cs["course"]['name'] not in tea_exp:
                        tea_exp[cs["course"]['name']]=[]
                    for grp in cs['experiment_gp']:
                        tea_exp[cs["course"]['name']].append(grp["name"])

        if grp_lec != tea_lec:
            return "Error in lectures",grp_lec,tea_lec
        if grp_tut != tea_tut:
            return "Error in tutorials",grp_tut, tea_tut
        if grp_exp != tea_exp:
            return "Error in experiments",grp_exp, tea_exp


    ##################
    # Course manager #
    ##################
    def add_course(self, name,room_type, lect, tut, exp, max_lec = 5, max_tut = 5, max_exp = 3):

        if any(i['name'].casefold() == name.casefold() for i in self.courses):
            return name+" already exists"

        if room_type not in self.room_types:
            return room_type+" doesn't exist"

        self.limit_hours_per_course[name]={"lec":max_lec,"tut":max_tut,"exp":max_exp}
        self.courses.append({'name': name, 'lecture': lect, 'tutorial': tut, 'experiment': exp, 'type_room': room_type})

    def rem_course(self, name):
        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == name.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + name + " does not exists"

        # Check if a teacher has this course
        for i in self.teachers:
            for j in i['course_list']:
                if j['course'] == cs:
                    return "Teacher " + i['name'] + " has the course " + name

        # Check if the group exists
        for grp in self.groups:
            for crs in grp['course_list']:
                if crs == cs:
                    return "Group " + grp['name'] + " has the course " + name

        del self.limit_hours_per_course[name]
        del self.courses[self.courses.index(cs)]

    ###################
    # Teacher manager #
    ###################

    def add_teacher(self, name):
        if any(i['name'].casefold() == name.casefold() for i in self.teachers):
            return name+" already exists"
        self.teachers.append({'name': name, 'course_list': []})

    def rem_teacher(self, name):
        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == name.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + name + " does not exist"

        del self.teachers[self.teachers.index(elem)]

    def add_teacher_course(self, name, course_name):
        # Check if the teacher exists
        i = 0
        elem ={}
        for tea in self.teachers:
            if tea['name'].casefold() == name.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher "+name+" does not exists"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course_name.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course "+course_name+" does not exists"

        # Check the teacher already has this course
        if any(i['course'] == cs for i in elem['course_list']):
            return "Teacher "+name+" already has "+course_name+" course"

        elem['course_list'].append({'course': cs, 'lecture_promo': [], 'tutorial_gp': [], 'experiment_gp': []})

    def rem_teacher_course(self, teacher, course):
        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == teacher.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + teacher + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exist"

        # Check the teacher has this course
        i = 0
        tea_cou = {}
        for tc in elem["course_list"]:
            if tc['course'] == cs:
                i = 1
                tea_cou = tc
        if i == 0:
            return "Teacher " + teacher + " does not have " + course + " course"

        del self.teachers[self.teachers.index(elem)]['course_list'][elem['course_list'].index(tea_cou)]

    def add_teacher_promo(self, teacher, course, promo):
        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == teacher.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + teacher + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exist"

        # Check the teacher has this course
        i = 0
        tea_cou = {}
        for tc in elem["course_list"]:
            if tc['course'] == cs:
                i = 1
                tea_cou = tc
        if i == 0:
            return "Teacher " + teacher + " does not have " + course + " course"

        tea_cou['lecture_promo'].append(str(promo))

    def rem_teacher_promo(self, teacher, course, promo):
        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == teacher.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + teacher + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exist"

        # Check the teacher has this course
        i = 0
        tea_cou = {}
        for tc in elem["course_list"]:
            if tc['course'] == cs:
                i = 1
                tea_cou = tc
        if i == 0:
            return "Teacher " + teacher + " does not have " + course + " course"

        # Check if the teacher has this promo in his course
        if str(promo) not in tea_cou['lecture_promo'] :
            return "Teacher " + teacher + " does not have the promo "+str(promo)+" in his course "+ course

        tea_cou['lecture_promo'].remove(str(promo))

    def add_teacher_group(self, teacher, group, course, course_type):
        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == teacher.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + teacher + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exist"

        # Check the teacher has this course
        i = 0
        tea_cou = {}
        for tc in elem["course_list"]:
            if tc['course'] == cs:
                i = 1
                tea_cou = tc
        if i == 0:
            return "Teacher " + teacher + " does not have " + course + " course"

        # Check if the group exists
        i = 0
        elem = {}
        for grp in self.groups:
            if grp['name'].casefold() == group.casefold():
                i = 1
                elem = grp

        if i == 0:
            return "Group " + group + " does not exist"

        # Check if the group has the course
        i=0
        for cs_grp in elem['course_list']:
            if cs_grp['name'] == course:
                i=1

        if i == 0:
            return "Group " + group + " does not have "+course

        # Check if the course_type exists
        if course_type != 'tutorial' and course_type!='experiment':
            return course_type + " is not a type of course"

        # Check if this teacher already has this group in this type_course in this course
        if elem in tea_cou[course_type+"_gp"]:
            return teacher + " already has "+group+" in "+course+" "+course_type

        tea_cou[course_type+"_gp"].append(elem)

    def rem_teacher_group(self, teacher, group, course, course_type):
        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == teacher.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + teacher + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exist"

        # Check the teacher has this course
        i = 0
        tea_cou = {}
        for tc in elem["course_list"]:
            if tc['course'] == cs:
                i = 1
                tea_cou = tc
        if i == 0:
            return "Teacher " + teacher + " does not have " + course + " course"

        # Check if the group exists
        i = 0
        elem = {}
        for grp in self.groups:
            if grp['name'].casefold() == group.casefold():
                i = 1
                elem = grp

        if i == 0:
            return "Group " + group + " does not exist"

        # Check if the group has the course
        i = 0
        for cs_grp in elem['course_list']:
            if cs_grp['name'] == course:
                i = 1

        if i == 0:
            return "Group " + group + " does not have " + course

        # Check if the course_type exists
        if course_type != 'tutorial' and course_type != 'experiment':
            return course_type + " is not a type of course"

        # Check if this teacher already has this group in this type_course in this course
        if elem not in tea_cou[course_type + "_gp"]:
            return teacher + " does not have the group " + group + " in " + course + " " + course_type

        tea_cou[course_type + "_gp"].remove(elem)

    def add_teacher_absence(self, name, week ,days):

        if  week > self.number_of_weeks:
            return "Week "+str(week)+ " is greater than number of weeks("+str(self.number_of_weeks)+")"

        # Check if the teacher exists
        i = 0
        elem = {}
        for tea in self.teachers:
            if tea['name'].casefold() == name.casefold():
                i = 1
                elem = tea

        if i == 0:
            return "Teacher " + name + " does not exists"

        self.teacher_absence_list.append({'teacher': elem, 'week': week, 'absence_day_number': days})

    def rem_teacher_absence(self, name, week):
        i = 0
        for tea in self.teachers:
            if tea['name'].casefold() == name.casefold():
                i = 1

        if i == 0:
            return "Teacher " + name + " does not exist"

        i=0
        elem = {}
        for absence in self.teacher_absence_list:
            if absence['teacher']['name'].casefold() == name.casefold() and absence['week']==week:
                elem = absence
                i=1

        if i==0:
            return name+" is not absent in week "+str(week)

        del self.teacher_absence_list[self.teacher_absence_list.index(elem)]

    #################
    # Group manager #
    #################

    def add_group(self, name, promo):
        if any(grp['name'].casefold() == name.casefold() for grp in self.groups):
            return name + " already exists"

        self.groups.append({'name': name,  'course_list': [], 'promo':promo})

    def rem_group(self, name):
        # Check if the group exists
        i = 0
        elem = {}
        for grp in self.groups:
            if grp['name'].casefold() == name.casefold():
                i = 1
                elem = grp

        if i == 0:
            return "Group " + name + " does not exist"

        del self.groups[self.groups.index(elem)]

    def add_group_course(self, group, course):
        # Check if the group exists
        i = 0
        grp = {}
        for gp in self.groups:
            if gp['name'].casefold() == group.casefold():
                i = 1
                grp = gp

        if i == 0:
            return "Group " + group + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exists"

        # Check the group already has this course
        if any(i == cs for i in grp['course_list']):
            return "Group " + group + " already has " + course + " course"

        self.groups[self.groups.index(grp)]['course_list'].append(cs)

    def rem_group_course(self, group, course):
        # Check if the grou exists
        i = 0
        grp = {}
        for gp in self.groups:
            if gp['name'].casefold() == group.casefold():
                i = 1
                grp = gp

        if i == 0:
            return "Group " + group + " does not exist"

        # Check if the course exists
        i = 0
        cs = {}
        for cou in self.courses:
            if cou['name'].casefold() == course.casefold():
                i = 1
                cs = cou
        if i == 0:
            return "Course " + course + " does not exist"

        # Check the group already has this course
        if not any(i == cs for i in grp['course_list']):
            return "Group " + group + " does not have " + course + " course"

        del self.groups[self.groups.index(grp)]['course_list'][grp['course_list'].index(cs)]

    ################
    # Room manager #
    ################

    def add_room_type(self, room_type):
        if room_type in self.room_types:
            return room_type+" already exists"

        self.room_types.append(room_type)

    def rem_room_type(self, room_type):
        if room_type not in self.room_types:
            return room_type+" doesn't exist"

        for cou in self.courses:
            if room_type == cou['value_type_room']:
                return room_type + " is still used in " + cou['name']

        del self.room_types[self.room_types.index(room_type)]

    def add_room(self, name, lect, tut, exp, room_type):
        if room_type not in self.room_types:
            return room_type+" doesn't exist"

        for room in self.rooms:
            if name.casefold() == room["name"].casefold():
                return name+" room already exists"

        self.rooms.append({'name': name, 'is_for_lecture': lect, 'is_for_tutorial': tut, 'is_for_experiment': exp,'type_room': room_type})

    def rem_room(self, name):
        c=0
        cpt = 0
        for room in self.rooms:
            if name.casefold() == room['name'].casefold():
                c = 1
                break
            cpt += 1
        if c==0:
            return name+" room doesn't exist"
        del self.rooms[cpt]


def test_json():
    course_1 = {'name': 'math', 'lecture': 40, 'tutorial': 0, 'experiment': 0}
    course_2 = {'name': 'Computer Science', 'lecture': 30, 'tutorial': 10, 'experiment': 15}
    course_3 = {'name': 'Chemistry', 'lecture': 10, 'tutorial': 0, 'experiment': 0}
    course_4 = {'name': 'English', 'lecture': 20, 'tutorial': 0, 'experiment': 0}
    course_5 = {'name': 'PPI', 'lecture': 10, 'tutorial': 0, 'experiment': 0}

    course_list = [course_1, course_2, course_3, course_4, course_5]

    teacher_1 = {'name': "Bob Dylan", 'course_list': [{'course': course_1, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0},
                 {'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 1}]}
    teacher_2 = {'name': "Miley Cyrus", 'course_list': [{'course': course_2, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 0}]}
    teacher_3 = {'name': "Axl Rose", 'course_list': [{'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 2}]}
    teacher_4 = {'name': "Brian Johnson", 'course_list': [{'course': course_3, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
    teacher_5 = {'name': "Mick Jagger", 'course_list': [{'course': course_4, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}
    teacher_6 = {'name': "Rick Astley", 'course_list': [{'course': course_5, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0}]}

    teacher_list = [teacher_1, teacher_2, teacher_3, teacher_4, teacher_5, teacher_6]

    group_1 = {'name': '4IR-A', 'course_list': [course_1, course_2]}
    group_2 = {'name': '4IR-B', 'course_list': [course_1, course_3, course_5]}
    group_3 = {'name': '4IR-C', 'course_list': [course_3, course_5, course_4]}
    group_list = [group_1, group_2, group_3]

    jfile = [course_list, teacher_list, group_list]
    f = open("test.json", "w")
    f.write(json.dumps(jfile))


if __name__ == '__main__':
    f = DataFileManager("plop.txt")
    # Rooms #
    print(f.add_room_type("Automate"))
    print(f.add_room_type("CS"))
    print(f.add_room_type("IOT"))
    print(f.add_room_type("Security"))
    print(f.add_room_type("Normal"))

    print(f.add_room("GEI 15", True, True, True, "Automate"))
    print(f.add_room("GEI 13", True, True, False, "Automate"))
    print(f.add_room("GEI 111", False, True, True, "CS"))
    print(f.add_room("GEI 101", False, True, True, "Security"))
    print(f.add_room("GEI 213", True, True, False, "Automate"))

    print(f.add_course('math',"Automate", 40,5,5))
    print(f.add_course('Computer Science', "CS", 30, 10, 0))
    print(f.add_course('Security', "Security", 10, 0, 10))
    print(f.add_course('English', "IOT", 20, 0, 0))
    print(f.add_course('PPI', "IOT", 10, 0, 0))

    print(f.add_group("4IR-A", 1))
    print(f.add_group("4IR-B", 1))
    print(f.add_group("4IR-C", 2))
    print(f.add_group("4IR-D", 2))

    print(f.add_group_course("4IR-A","math"))
    print(f.add_group_course("4IR-A", "Computer Science"))
    print(f.add_group_course("4IR-B", "math"))
    print(f.add_group_course("4IR-B", "Computer Science"))
    print(f.add_group_course("4IR-B", "PPI"))
    print(f.add_group_course("4IR-C", "Security"))
    print(f.add_group_course("4IR-C", "English"))
    print(f.add_group_course("4IR-C", "PPI"))
    print(f.add_group_course("4IR-D", "math"))
    print(f.add_group_course("4IR-D", "English"))
    print(f.add_group_course("4IR-D", "PPI"))

    # Prof 1
    print(f.add_teacher("Michel Dumont"))
    print(f.add_teacher_course("Michel Dumont","math"))
    print(f.add_teacher_promo("Michel Dumont","math","1"))
    print(f.add_teacher_group("Michel Dumont","4IR-A", "math", "tutorial"))
    print(f.add_teacher_group("Michel Dumont", "4IR-B", "math", "tutorial"))
    print(f.add_teacher_group("Michel Dumont", "4IR-A", "math", "experiment"))
    print(f.add_teacher_course("Michel Dumont", "Computer Science"))
    print(f.add_teacher_group("Michel Dumont", "4IR-B", "Computer Science", "tutorial"))

    #Prof 2
    print(f.add_teacher("Hélène Michou"))
    print(f.add_teacher_course("Hélène Michou", "math"))
    print(f.add_teacher_promo("Hélène Michou", "math", "2"))
    print(f.add_teacher_group("Hélène Michou", "4IR-D", "math", "tutorial"))
    print(f.add_teacher_group("Hélène Michou", "4IR-B", "math", "experiment"))
    print(f.add_teacher_group("Hélène Michou", "4IR-D", "math", "experiment"))
    print(f.add_teacher_course("Hélène Michou", "Computer Science"))
    print(f.add_teacher_promo("Hélène Michou", "Computer Science", "1"))
    print(f.add_teacher_group("Hélène Michou", "4IR-A", "Computer Science", "tutorial"))

    #Prof 3
    print(f.add_teacher("Benoit Jardin"))
    print(f.add_teacher_course("Benoit Jardin", "Computer Science"))
    print(f.add_teacher_promo("Benoit Jardin", "Computer Science", "2"))
    print(f.add_teacher_group("Benoit Jardin", "4IR-B", "Computer Science", "tutorial"))

    #Prof 4
    print(f.add_teacher("Kate Stuart"))
    print(f.add_teacher_course("Kate Stuart", "Security"))
    print(f.add_teacher_promo("Kate Stuart", "Security", "2"))
    print(f.add_teacher_group("Kate Stuart", "4IR-C", "Security", "experiment"))

    #Prof 5
    print(f.add_teacher("Hervé Vieux"))
    print(f.add_teacher_course("Hervé Vieux", "English"))
    print(f.add_teacher_promo("Hervé Vieux", "English", "2"))

    #Prof 6
    print(f.add_teacher("Christiane Colin"))
    print(f.add_teacher_course("Christiane Colin", "math"))
    print(f.add_teacher_promo("Christiane Colin", "math", "1"))
    print(f.add_teacher_promo("Christiane Colin", "math", "2"))

    # Teacher absences #
    f.set_nb_weeks(10)
    print(f.add_teacher_absence("Michel Dumont", 0,5))
    print(f.add_teacher_absence("Hélène Michou", 9, 5))
    print(f.add_teacher_absence("Michel Dumont", 4, 2))

    #print(f.limit_hours_per_course)

    print(DataFileManager.check_teacher_group(f.teachers,f.groups))
    f.store_file()