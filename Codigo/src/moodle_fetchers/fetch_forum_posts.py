from moodle_fetchers.forum_fetcher import ForumFetcher

def fetch(course_id, user_id=None):
    fetcher = ForumFetcher()
    discussions = fetcher.getForumDiscussions(course_id)
    fetcher.saveData(f"forum_discussions_course_{course_id}.json", discussions)

if __name__ == "__main__":
    fetch(course_id=2)