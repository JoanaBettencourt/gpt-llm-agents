from moodle_fetchers.grades_fetcher import GradesFetcher
from moodle_fetchers.enrollments_checker import EnrollmentsChecker

def fetch(course_id, user_id=None):
    checker = EnrollmentsChecker()
    students = checker.getStudentData(course_id)
    fetcher = GradesFetcher()
    all_grades = []

    for student in students:
        grade_info = fetcher.getStudentGrades(course_id, student["id"])
        all_grades.append(grade_info)

    fetcher.saveData(f"grades_course_{course_id}.json", all_grades)


if __name__ == "__main__":
    fetch(course_id=2)
