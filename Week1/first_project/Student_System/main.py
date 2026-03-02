from models import Student, Classroom
from utils import DataHandler
import analytics
import sys

def main():
    my_class = Classroom()
    DataHandler.load_from_csv(my_class)
    
    while True:
        DataHandler.display_header("STUDENT PERFORMANCE ANALYZER")
        print(" 1. [Add] New Student")
        print(" 2. [Remove] Student by ID")
        print(" 3. [Search] for Student")
        print(" 4. [Class Average] View Overall Mean")
        print(" 5. [Top] Performing Student")
        print(" 6. [Lowest] Performing Student")
        print(" 7. [Distribution] Grade Categories Count")
        print(" 8. [Rankings] Show All Students Sorted")
        print(" 9. [Save & Exit] System Shutdown")
        print("-" * 50)

        choice = input(">>> Select an option (1-9): ").strip()

        try:
            if choice == '1':
                name = input("Enter Student Name: ")
                sid = input("Enter Student ID: ")
                g_raw = input("Enter Grades (e.g., 90, 85, 70): ")
                
                grades = DataHandler.validate_grades(g_raw)
                if grades is not None:
                    new_student = Student(name, sid, grades)
                    my_class.add_student(new_student)
                    print(f"SUCCESS: Student '{name}' added.")
                else:
                    print("ERROR: Invalid grades. Please use numbers and commas.")

            elif choice == '2':
                sid = input("Enter Student ID to remove: ")
                if my_class.remove_student(sid):
                    print(f"SUCCESS: Student with ID {sid} has been removed.")
                else:
                    print(f"FAILED: No student found with ID {sid}. Check the number and try again.")

            elif choice == '3':
                sid = input("Enter ID to search: ")
                s = my_class.search_student(sid)
                if s:
                    print(f"\n[FOUND] Name: {s.name} | Average: {s.calculate_average():.2f}")
                    print(f"Status: {s.get_category()}")
                else:
                    print("NOT FOUND: No student matches that ID.")

            elif choice == '4':
                avg = my_class.calculate_class_average()
                print(f"CLASS METRIC: The overall average is {avg:.2f}")

            elif choice == '5':
                top = analytics.get_top_student(my_class)
                if top:
                    print(f"TOP PERFORMER: {top.name} | Score: {top.calculate_average():.2f}")
                else:
                    print("DATA EMPTY: Add students first.")

            elif choice == '6':
                low = analytics.get_lowest_student(my_class)
                if low:
                    print(f"LOWEST PERFORMER: {low.name} | Score: {low.calculate_average():.2f}")
                else:
                    print("DATA EMPTY: Add students first.")

            elif choice == '7':
                dist = analytics.get_grade_distribution(my_class)
                print("\n[GRADE DISTRIBUTION]")
                for category, count in dist.items():
                    print(f" - {category.ljust(18)}: {count} student(s)")

            elif choice == '8':
                print("\n" + "RANK".ljust(5) + "NAME".ljust(20) + "AVERAGE".ljust(10) + "CATEGORY")
                print("-" * 50)
                ranked = analytics.rank_students(my_class)
                for i, s in enumerate(ranked, 1):
                    print(f"{str(i).ljust(5)}{s.name.ljust(20)}{format(s.calculate_average(), '.2f').ljust(10)}{s.get_category()}")

            elif choice == '9':
                if DataHandler.save_to_csv(my_class):
                    print("SYSTEM: Database updated successfully (data.csv).")
                print("EXIT: Goodbye!")
                sys.exit()

            else:
                print("INVALID: Please enter a number between 1 and 9.")

        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()