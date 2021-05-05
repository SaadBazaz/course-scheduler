import random
import prettytable

POPULATION_SIZE = 9
NO_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Data:
    ROOMS = [
        ["R1", 45],  # room id, seating cap
        ["R2", 45],
        ["R3", 35]
    ]
    MEETING_TIMES = [
        ["MT1", "MWF 09:00 - 10:00"],
        ["MT2", "MWF 10:00 - 11:00"],
        ["MT3", "TTH 09:00 - 10:30"],
        ["MT4", "TTH 10:30 - 12:00"]
    ]
    INSTRUCTORS = [
        ["I1", "Dr James Web"],
        ["I2", "Mr Mike Brown"],
        ["I3", "Dr Steve Day"],
        ["I4", "Mrs Jane Doe"]
    ]

    def __init__(self):
        self._rooms = []
        self._meeting_times = []
        self._instructors = []
        for i in range(0, len(self.ROOMS)):
            self._rooms.append(Room(number=self.ROOMS[i][0], seating_capacity=self.ROOMS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
            self._meeting_times.append(MeetingTime(id=self.MEETING_TIMES[i][0], time=self.MEETING_TIMES[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
            self._instructors.append(Instructor(id=self.INSTRUCTORS[i][0], name=self.INSTRUCTORS[i][1]))

        course1 = Course(
            number="C1",
            name="325K",
            instructors=[self._instructors[0], self._instructors[1]],
            max_no_of_students=25
        )
        course2 = Course(
            number="C2",
            name="319K",
            instructors=[self._instructors[0], self._instructors[1], self._instructors[2]],
            max_no_of_students=35
        )
        course3 = Course(
            number="C3",
            name="462K",
            instructors=[self._instructors[0], self._instructors[1]],
            max_no_of_students=25
        )
        course4 = Course(
            number="C4",
            name="464K",
            instructors=[self._instructors[2], self._instructors[3]],
            max_no_of_students=30
        )
        course5 = Course(
            number="C5",
            name="360C",
            instructors=[self._instructors[3]],
            max_no_of_students=35
        )
        course6 = Course(
            number="C6",
            name="303K",
            instructors=[self._instructors[0], self._instructors[2]],
            max_no_of_students=45
        )
        course7 = Course(
            number="C7",
            name="303L",
            instructors=[self._instructors[1], self._instructors[3]],
            max_no_of_students=45
        )
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        dept1 = Department(
            name="MATH",
            courses=[course1, course3]
        )
        dept2 = Department(
            name="EE",
            courses=[course2, course4, course5]
        )
        dept3 = Department(
            name="PHY",
            courses=[course6, course7]
        )
        self._depts = [dept1, dept2, dept3]
        self._no_of_classes = 0
        for i in range(0, len(self._depts)):
            self._no_of_classes += len(self._depts[i].get_courses())
        print("No of classes: {}".format(self._no_of_classes))

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meeting_times(self):
        return self._meeting_times

    def get_no_of_classes(self):
        return self._no_of_classes


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._no_of_conflicts = 0
        self._fitness = -1
        self._class_no = 0
        self._is_fitness_changed = True

    def get_classes(self):
        self._is_fitness_changed = True
        return self._classes

    def get_no_of_conflicts(self):
        return self._no_of_conflicts

    def get_fitness(self):
        if self._is_fitness_changed:
            self._fitness = self.calculate_fitness()
            self._is_fitness_changed = False
        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                new_class = Class(id=self._class_no, dept=depts[i], course=courses[j])
                self._class_no += 1
                new_class.set_meeting_time(data.get_meeting_times()[random.randrange(0, len(data.get_meeting_times()))])
                new_class.set_room(data.get_rooms()[random.randrange(0, len(data.get_rooms()))])
                new_class.set_instructor(
                    courses[j].get_instructors()[random.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(new_class)
        return self

    def calculate_fitness(self):
        self._no_of_conflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if classes[i].get_room().get_seating_capacity() < classes[i].get_course().get_max_no_of_students():
                self._no_of_conflicts += 1
            for j in range(0, len(classes)):
                if j >= i:
                    if classes[i].get_meeting_time() == classes[j].get_meeting_time() and classes[i].get_id() != \
                            classes[j].get_id():
                        if classes[i].get_room() == classes[j].get_room():
                            self._no_of_conflicts += 1
                        if classes[i].get_instructor() == classes[j].get_instructor():
                            self._no_of_conflicts += 1
        return 1 / (1.0 * self._no_of_conflicts + 1)

    def __str__(self):
        return_value = ""
        for i in range(0, len(self._classes) - 1):
            return_value += str(self._classes[i]) + ", "
        return_value += str(self._classes[len(self._classes) - 1])


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(size=0)
        for i in range(NO_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NO_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NO_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossover_schedule = Schedule().initialize()
        for i in range(0, len(crossover_schedule.get_classes())):
            if random.random() > 0.5:
                crossover_schedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossover_schedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossover_schedule

    def _mutate_schedule(self, schedule_to_mutate):
        schedule = Schedule().initialize()
        for i in range(0, len(schedule_to_mutate.get_classes())):
            if MUTATION_RATE > random.random():
                schedule_to_mutate.get_classes()[i] = schedule.get_classes()[i]
        return schedule_to_mutate

    def _select_tournament_population(self, pop):
        tournament_pop = Population(size=0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[random.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Course:
    def __init__(self, number, name, instructors, max_no_of_students):
        self._number = number
        self._name = name
        self._instructors = instructors
        self._max_no_of_students = max_no_of_students

    def __str__(self):
        return self._name

    def get_instructors(self):
        return self._instructors

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_max_no_of_students(self):
        return self._max_no_of_students


class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name


class Room:
    def __init__(self, number, seating_capacity):
        self._number = number
        self._seating_capacity = seating_capacity

    def get_number(self):
        return self._number

    def get_seating_capacity(self):
        return self._seating_capacity


class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self):
        return self._id

    def get_time(self):
        return self._time


class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self):
        return self._name

    def get_courses(self):
        return self._courses


class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meeting_time = None
        self._room = None

    def get_id(self):
        return self._id

    def get_dept(self):
        return self._dept

    def get_course(self):
        return self._course

    def get_instructor(self):
        return self._instructor

    def get_meeting_time(self):
        return self._meeting_time

    def get_room(self):
        return self._room

    def set_instructor(self, instructor):
        self._instructor = instructor

    def set_meeting_time(self, meeting_time):
        self._meeting_time = meeting_time

    def set_room(self, room):
        self._room = room

    def __str__(self):
        return str(self._dept.get_name()) + ", " + str(self._course.get_number()) + ", " + str(
            self._room.get_number()) + ", " + str(self._instructor.get_id()) + ", " + str(self._meeting_time.get_id())


def print_dept():
    depts = data.get_depts()
    available_depts_table = prettytable.PrettyTable(['dept', 'courses'])
    for i in range(0, len(depts)):
        courses = depts.__getitem__(i).get_courses()
        temp_str = "["
        for j in range(0, len(courses) - 1):
            temp_str += courses[j].__str__() + ", "
        temp_str += courses[len(courses) - 1].__str__() + "]"
        available_depts_table.add_row([depts.__getitem__(i).get_name(), temp_str])
    print(available_depts_table)


def print_courses():
    available_courses_table = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructions'])
    courses = data.get_courses()
    for i in range(0, len(courses)):
        instructors = courses[i].get_instructors()
        temp_str = ""
        for j in range(0, len(instructors) - 1):
            temp_str += instructors[j].__str__() + ", "
        temp_str += instructors[len(instructors) - 1].__str__()
        available_courses_table.add_row(
            [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_max_no_of_students()), temp_str]
        )
    print(available_courses_table)


def print_rooms():
    available_rooms_table = prettytable.PrettyTable(['room #', 'max seating capacity'])
    rooms = data.get_rooms()
    for i in range(0, len(rooms)):
        available_rooms_table.add_row(
            [str(rooms[i].get_number()), str(rooms[i].get_seating_capacity())]
        )
    print(available_rooms_table)


def print_instructors():
    available_instructors_table = prettytable.PrettyTable(['id', 'instructor'])
    instructors = data.get_instructors()
    for i in range(0, len(instructors)):
        available_instructors_table.add_row([instructors[i].get_id(), instructors[i].get_name()])
    print(available_instructors_table)


def print_meeting_times():
    available_meeting_times_table = prettytable.PrettyTable(['id', 'Meeting Time'])
    meeting_times = data.get_meeting_times()
    for i in range(0, len(meeting_times)):
        available_meeting_times_table.add_row(
            [meeting_times[i].get_id(), meeting_times[i].get_time()]
        )
    print(available_meeting_times_table)


def print_generation(population):
    table = prettytable.PrettyTable(
        ["schedule #", "fitness", "# of conflicts", "classes [dept, class, room, instructor, meeting time]"]
    )
    schedules = population.get_schedules()
    for i in range(0, len(schedules)):
        temp_str = "- "
        for _class in schedules[i].get_classes():
            temp_str += str(_class) + " - "
        table.add_row([
            str(i),
            round(schedules[i].get_fitness(), 3),
            schedules[i].get_no_of_conflicts(),
            temp_str
        ])
    print(table)


def print_schedule_as_table(schedule):
    classes = schedule.get_classes()
    table = prettytable.PrettyTable(
        ["Class #", "Dept", "Course (number, max # of students)", "Room (capacity)", "Instructor (id)",
         "Meeting  Time (id)"]
    )
    for i in range(0, len(classes)):
        table.add_row([
            str(i),
            classes[i].get_dept().get_name(),
            classes[i].get_course().get_name() + " (" + str(classes[i].get_course().get_number()) + ", "
            + str(classes[i].get_course().get_max_no_of_students()) + " )",
            classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seating_capacity()) + " )",
            classes[i].get_instructor().get_name() + " (" + str(classes[i].get_instructor().get_id()) + " )",
            classes[i].get_meeting_time().get_time() + " (" + str(classes[i].get_meeting_time().get_id()) + " )"
        ])
    print(table)


def print_available_data():
    print("> All Available Data")
    print_dept()
    print_courses()
    print_rooms()
    print_instructors()
    print_meeting_times()


data = Data()
generation_number = 0


def print_generation_number():
    print("\n> Generation # {}".format(generation_number))


if __name__ == '__main__':
    print_available_data()
    print_generation_number()
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    print_generation(population)
    print_schedule_as_table(population.get_schedules()[0])
    genetic_algorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_number += 1
        print_generation_number()
        population = genetic_algorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        print_generation(population)
        print_schedule_as_table(population.get_schedules()[0])
    print("\n\n\n")
