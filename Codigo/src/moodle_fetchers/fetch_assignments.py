from moodle_fetchers.assignment_fetcher import AssignmentFetcher

def fetch(course_id, user_id=None):
    fetcher = AssignmentFetcher()
    assignments = fetcher.getAssignments(course_id)
    fetcher.saveData(f"assignments_course_{course_id}.json", assignments)

if __name__ == "__main__":
    fetch(course_id=2)