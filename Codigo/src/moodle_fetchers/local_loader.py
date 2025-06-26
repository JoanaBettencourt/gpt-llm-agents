import json, os

def load_all_data(course_id, user_id):
    ficheiros = {
            "enrollments": f"dados/enrollments_course_{course_id}.json",
            "private_messages": f"dados/messages_user_{user_id}.json",
            "forum_posts": f"dados/forum_posts_course_{course_id}.json",
            "grades": f"dados/grades_course_{course_id}.json",
            "course_contents": f"dados/course_{course_id}_contents.json",
            "assignments": f"dados/assignments_course_{course_id}.json",
            "calendar_events": f"dados/calendar_events_course_{course_id}.json",
            "quiz_attempts": f"dados/quiz_attempts_course_{course_id}.json"
    }

    dados = {}
    for nome, ficheiro in ficheiros.items():
        if os.path.exists(ficheiro):
            with open(ficheiro, "r", encoding="utf-8") as f:
                dados[nome] = json.load(f)
        else:
            dados[nome] = f"[Ficheiro {ficheiro} não encontrado]"

    return dados
