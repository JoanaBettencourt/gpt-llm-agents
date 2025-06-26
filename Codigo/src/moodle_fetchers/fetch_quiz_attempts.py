from moodle_fetchers.enrollments_checker import EnrollmentsChecker
from moodle_fetchers.quiz_finder import QuizFinder
from moodle_fetchers.quiz_fetcher import QuizFetcher

def fetch(course_id, user_id=None):
    checker = EnrollmentsChecker()
    students = checker.getStudentData(course_id)

    finder = QuizFinder()
    quizzes = finder.getQuizzesByCourse(course_id)

    if not quizzes:
        print("Não existem quizzes disponíveis neste curso.")
        return

    fetcher = QuizFetcher()
    all_attempts = []

    for quiz in quizzes:
        quiz_id = quiz["id"]
        quiz_name = quiz["name"]
        print(f"A verificar tentativas para o quiz: {quiz_name} (ID {quiz_id})")

        for student in students:
            uid = student["id"]
            fullname = student["fullname"]
            attempts = fetcher.getUserQuizAttempts(quiz_id, uid)
            all_attempts.append({
                "quiz": quiz_name,
                "student": fullname,
                "attempts": attempts
            })

    filename = f"quiz_attempts_course_{course_id}.json"
    fetcher.saveData(filename, all_attempts)

if __name__ == "__main__":
    fetch(course_id=2)
