import json
# Format
# Course : {'name':'Sexage de poussin', 'lecture' : 0, 'tutorial':0, 'experiment':0}
# Teacher : 'name':'Michael Jackson', 'course_list':[{'course': course_1, 'lecture_gp_nb': 1, 'tutorial_gp_nb': 0, 'experiment_gp_nb': 0},
# {'course': course_2, 'lecture_gp_nb': 0, 'tutorial_gp_nb': 1, 'experiment_gp_nb': 1}]}
# Group : {'name':'Group1', 'course_list':[coure1,course2]}

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

    filename = ""

    def __init__(self, filename):
        self.filename = filename

    # Load data from a file
    def load_file(self):
        f = open(self.filename, "r")
        data = json.load(f)
        self.courses = data[0]
        self.teachers = data[1]
        self.groups = data[2]

    # Generating file with object's data
    def store_file(self):
        py_object = [self.courses, self.teachers, self.groups]
        f = open(self.filename, "w")
        f.write(json.dumps(py_object))

    def get_data(self):
        return self.courses, self.teachers, self.groups

    def add_course(self, name, lect, tut, exp):

        if any(i['name'].casefold() == name.casefold() for i in self.courses):
            return name+" already exists"

        self.courses.append({'name': name, 'lecture': lect, 'tutorial': tut, 'experiment': exp})

    def add_teacher(self, name):
        if any(i['name'].casefold() == name.casefold() for i in self.teachers):
            return name+" already exists"
        self.teachers.append({'name': name, 'course_list': []})

    def add_teacher_course(self, name, course_name, nb_lect, nb_tut, nb_exp):
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

        elem['course_list'].append({'course': cs, 'lecture_gp_nb': nb_lect, 'tutorial_gp_nb': nb_tut, 'experiment_gp_nb': nb_exp})

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
                    return "Teacher "+i['name']+" has the course "+name

        # Check if the group exists
        for grp in self.groups:
            for crs in grp['course_list']:
                if crs == cs:
                    return "Group " + grp['name'] + " has the course "+name

        del self.courses[self.courses.index(cs)]

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

        # Check the teacher already has this course
        i = 0
        tea_cou = {}
        for tc in elem["course_list"]:
            if tc['course'] == cs:
                i = 1
                tea_cou = tc
        if i == 0:
            return "Teacher " + teacher + " does not have " + course + " course"

        del self.teachers[self.teachers.index(elem)]['course_list'][elem['course_list'].index(tea_cou)]

    def add_group(self, name):
        if any(grp['name'].casefold() == name.casefold() for grp in self.groups):
            return name + " already exists"

        self.groups.append({'name': name,  'course_list': []})

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


def test_json():
    course_1 = {'name': 'Math', 'lecture': 40, 'tutorial': 0, 'experiment': 0}
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

