from moodle_fetchers.calendar_fetcher import CalendarFetcher

def fetch(course_id, user_id=None):
    fetcher = CalendarFetcher()
    events = fetcher.getUpcomingEvents(course_id)
    fetcher.saveData(f"calendar_events_{course_id}.json", events)

if __name__ == "__main__":
    COURSE_ID = 2
    fetcher = CalendarFetcher()
    events = fetcher.getUpcomingEvents(COURSE_ID)
    fetcher.saveData(f"calendar_events_{COURSE_ID}.json", events)
