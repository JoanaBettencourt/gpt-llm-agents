from moodle_fetchers.completion_fetcher import CompletionFetcher
from moodle_fetchers.enrollments_checker import EnrollmentsChecker

def fetch(course_id, user_id=None):
    checker = EnrollmentsChecker()
    students = checker.getStudentData(course_id)
    fetcher = CompletionFetcher()
    results = []

    for student in students:
        status = fetcher.getActivityCompletionStatus(course_id, student["id"])
        results.append({
            "student": student["fullname"],
            "completion": status
        })

    fetcher.saveData(f"completion_status_{course_id}.json", results)

if __name__ == "__main__":
    COURSE_ID = 2
    checker = EnrollmentsChecker()
    students = checker.getStudentData(COURSE_ID)
    fetcher = CompletionFetcher()
    results = []

    for student in students:
        status = fetcher.getActivityCompletionStatus(COURSE_ID, student["id"])
        results.append({"student": student["fullname"], "completion": status})

    fetcher.saveData(f"completion_status_{COURSE_ID}.json", results)
