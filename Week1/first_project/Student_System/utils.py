import csv
import os

class DataHandler:
    
    @staticmethod
    def validate_grades(grades_string):
        if not grades_string.strip():
            return None
        try:
            # Using list comprehension for Pythonic efficiency (Effective Python tip)
            return [float(g.strip()) for g in grades_string.split(',')]
        except ValueError:
            return None

    @classmethod
    def save_to_csv(cls, classroom, filename="data.csv"):
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for s in classroom.students:
                    grades_str = ",".join(map(str, s.grades))
                    writer.writerow([s.name, s.student_id, grades_str])
            return True
        except IOError as e:
            print(f"File Error: {e}")
            return False

    @classmethod
    def load_from_csv(cls, classroom, filename="data.csv"):
        from models import Student  
        if not os.path.exists(filename):
            return False
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        name, sid, g_str = row
                        grades = [float(g) for g in g_str.split(',') if g]
                        classroom.add_student(Student(name, sid, grades))
            return True
        except Exception as e:
            print(f"Loading Error: {e}")
            return False

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def display_header(title):
        print("\n" + "="*50)
        print(f"{title.center(50)}")
        print("="*50)