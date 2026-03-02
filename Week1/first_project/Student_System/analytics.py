def get_top_student(classroom):
    if not classroom.students:
        return None
    return max(classroom.students, key=lambda s: s.calculate_average())

def get_lowest_student(classroom):
    if not classroom.students:
        return None
    return min(classroom.students, key=lambda s: s.calculate_average())

def rank_students(classroom):
    return sorted(classroom.students, key=lambda s: s.calculate_average(), reverse=True)

def get_grade_distribution(classroom):
    distribution = {
        "Excellent": 0,
        "Good": 0,
        "Needs Improvement": 0
    }
    
    for student in classroom.students:
        category = student.get_category() 
        if category in distribution:
            distribution[category] += 1
            
    return distribution