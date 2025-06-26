import os

from moodle_fetchers.moodle_connector import MoodleConnector
from datetime import datetime, timedelta


class EnrollmentsChecker(MoodleConnector):
    """Classe para verificar utilizadores inscritos e a sua atividade."""

    def getAllEnrolledUsers(self, course_id):
        """Obtém todos os utilizadores inscritos na disciplina."""
        return self.requestData("core_enrol_get_enrolled_users", {"courseid": course_id})

    def getUsersByRole(self, users, role_shortname):
        """Filtra utilizadores com base no nome curto do papel."""
        return [
            user for user in users
            if any(role.get("shortname", "") == role_shortname for role in user.get("roles", []))
        ]

    def saveAllUsers(self, course_id):
        """Guarda todos os utilizadores inscritos na disciplina num ficheiro JSON."""
        todos = self.getAllEnrolledUsers(course_id)
        self.saveData(f"participantes_course_{course_id}.json", todos)
        print(f"💾 {len(todos)} participantes guardados em 'participantes_course_{course_id}.json'")

    def getStudentData(self, course_id):
        """Atalho para obter apenas estudantes."""
        return self.getUsersByRole(self.getAllEnrolledUsers(course_id), "student")

    def checkNewAndRemovedStudents(self, course_id):
        """Compara a lista atual de estudantes com a lista anterior."""
        current = self.getStudentData(course_id)
        filename = f"enrollments_course_{course_id}.json"
        previous = self.loadData(filename)

        if previous is None:
            print("⚠️ Nenhuma lista anterior encontrada. A guardar a atual.")
            self.saveData(filename, current)
            return

        current_ids = {u["id"] for u in current}
        previous_ids = {u["id"] for u in previous}

        new_students = current_ids - previous_ids
        removed_students = previous_ids - current_ids

        if new_students:
            id_to_name = {user["id"]: user["fullname"] for user in current}
            print(f"📥 {len(new_students)} novo(s) aluno(s): {[id_to_name[uid] for uid in new_students]}")
        else:
            print("✅ Nenhum aluno novo.")

        if removed_students:
            previous_id_to_name = {user["id"]: user["fullname"] for user in previous}
            print(f"❌ {len(removed_students)} aluno(s) removido(s): {[previous_id_to_name[uid] for uid in removed_students]}")
        else:
            print("✅ Nenhum aluno saiu.")

        print(f"👥 Total de estudantes atualmente inscritos: {len(current)}")
        self.saveData(filename, current)

    def checkRolesSummary(self, course_id):
        """Mostra um resumo do número de utilizadores por papel (estudante, professor, tutor)."""
        all_users = self.getAllEnrolledUsers(course_id)
        students = self.getUsersByRole(all_users, "student")
        teachers = self.getUsersByRole(all_users, "editingteacher")
        tutors = self.getUsersByRole(all_users, "teacher")  # ou 'noneditingteacher', consoante o papel definido

        print("📊 Resumo por papel:")
        print(f"   👨‍🎓 Estudantes: {len(students)}")
        print(f"   👩‍🏫 Professores: {len(teachers)}")
        print(f"   🧑‍💼 Tutores: {len(tutors)}")

    def checkRecentAccesses(self, course_id, days=7):
        """Mostra os estudantes que acederam à disciplina nos últimos X dias."""
        enrolled = self.getStudentData(course_id)
        now = datetime.now()
        cutoff = now - timedelta(days=days)
        recent = []

        for user in enrolled:
            last_access_ts = user.get("lastcourseaccess")
            if last_access_ts:
                last_access = datetime.fromtimestamp(last_access_ts)
                if last_access >= cutoff:
                    recent.append((user["fullname"], last_access))

        print(f"📊 {len(recent)} de {len(enrolled)} estudantes acederam à disciplina nos últimos {days} dias.")
        for name, access_time in recent:
            print(f"✅ {name} — {access_time.strftime('%Y-%m-%d %H:%M')}")

