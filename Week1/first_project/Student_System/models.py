class Student:
    def __init__(self, name, student_id, grades=None):
        self.__name = name
        self.__student_id = student_id
        # ممارسة من Effective Python: نستخدم نسخة من القائمة لضمان عدم تأثر الكائن بتعديلات خارجية
        self.__grades = list(grades) if grades else []

    @property
    def name(self):
        return self.__name

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grades(self):
        return self.__grades

    def calculate_average(self):
        if not self.__grades:
            return 0
        return sum(self.__grades) / len(self.__grades)

    def get_category(self):
        avg = self.calculate_average()
        if avg >= 90: return "Excellent"
        if avg >= 75: return "Good"
        return "Needs Improvement"


class Classroom:
    def __init__(self):
        # قائمة لتخزين كائنات الطلاب التي سنقوم بإنشائها
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student_id):
        student = self.search_student(student_id)
        if student:
            self.students = [s for s in self.students if s.student_id != student_id]
            return True
        return False

    def search_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def calculate_class_average(self):
        if not self.students:
            return 0
        total_avg = sum(s.calculate_average() for s in self.students)
        return total_avg / len(self.students)