from moodle_fetchers.enrollments_checker import EnrollmentsChecker

def fetch(course_id, user_id=None):
    checker = EnrollmentsChecker()
    checker.saveAllUsers(course_id)
    checker.checkNewAndRemovedStudents(course_id)
    checker.checkRecentAccesses(course_id, days=7)
    checker.checkRolesSummary(course_id)

if __name__ == "__main__":
    fetch(course_id=2)
