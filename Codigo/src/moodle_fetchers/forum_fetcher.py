import json

from datetime import datetime
from moodle_fetchers.moodle_connector import MoodleConnector


class ForumFetcher(MoodleConnector):
    """Classe para obter publicações dos fóruns."""

    def getForumDiscussions(self, course_id):
        forums = self.requestData("mod_forum_get_forums_by_courses", {"courseids[0]": course_id})
        all_discussions = []

        for forum in forums:
            forum_id = forum["id"]
            discussions = self.requestData("mod_forum_get_forum_discussions", {"forumid": forum_id})
            for discussion in discussions.get("discussions", []):
                all_discussions.append({
                    "forum": forum["name"],
                    "discussion": discussion["name"],
                    "author": discussion["userfullname"],
                    "created": datetime.fromtimestamp(discussion["created"]).strftime("%Y-%m-%d %H:%M"),
                    "message": discussion["message"]
                })

        return all_discussions

