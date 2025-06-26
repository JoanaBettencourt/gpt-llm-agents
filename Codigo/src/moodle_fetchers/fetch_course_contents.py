from moodle_fetchers.course_content_fetcher import CourseContentFetcher

def fetch(course_id, user_id=None):
    fetcher = CourseContentFetcher()
    contents = fetcher.getCourseContents(course_id)
    fetcher.saveData(f"course_contents_{course_id}.json", contents)

if __name__ == "__main__":
    COURSE_ID = 2
    fetcher = CourseContentFetcher()
    contents = fetcher.getCourseContents(COURSE_ID)
    fetcher.saveData(f"course_contents_{COURSE_ID}.json", contents)
