from datetime import time

from app.auth.security import hash_password
from app.db.sync_db import get_session_local
from app.models.grade import Grade
from app.models.membership import Membership
from app.models.student import Student
from app.models.user import User
from app.models.institution import Institution
from app.models.role import Role
from app.models.subject import Subject
from app.models.course_offering import CourseOffering

SessionLocal = get_session_local()


def seed_academic():
    db = SessionLocal()
    try:
        with db.begin():
            # USERS
            # =========================
            user1 = User(name="Hector", email="hector@test.com", password_hash=hash_password("pass123"), is_admin=False)
            user2 = User(name="Juan", email="juan@test.com", password_hash=hash_password("pass123"), is_admin=False)
            user3 = User(name="Ricardo", email="ricardo@test.com", password_hash=hash_password("pass123"), is_admin=False)
            user4 = User(name="Mario", email="mario@test.com", password_hash=hash_password("pass123"), is_admin=False)

            db.add_all([user1, user2, user3, user4])
            db.flush()

            # INSTITUTIONS
            # =========================
            inst1 = Institution(
                name="Instituto Tecnológico Central",
                slug="itc",
                description="Institución enfocada en tecnología",
                email="contacto@itc.edu",
                phone="5551234567",
                website="https://itc.edu",
                country="México",
                state="CDMX",
                city="Ciudad de México",
                address="Av. Reforma 123",
                is_active=True
            )

            inst2 = Institution(
                name="Universidad del Norte",
                slug="unorte",
                description="Universidad privada",
                email="info@unorte.edu",
                phone="5559876543",
                website="https://unorte.edu",
                country="México",
                state="Nuevo León",
                city="Monterrey",
                address="Calle Norte 456",
                is_active=True
            )

            inst3 = Institution(
                name="Centro Educativo Sur",
                slug="cesur",
                description="Centro educativo general",
                email="admin@cesur.edu",
                phone="5551112233",
                website="https://cesur.edu",
                country="México",
                state="Jalisco",
                city="Guadalajara",
                address="Av. Sur 789",
                is_active=True
            )

            db.add_all([inst1, inst2, inst3])
            db.flush()

            # ROLES
            # =========================
            role_admin = Role(name="admin", description="Administrador del sistema")
            role_student = Role(name="student", description="Alumno inscrito")
            role_teacher = Role(name="teacher", description="Profesor que imparte cursos")
            role_director = Role(name="director", description="Director de la institucion")

            db.add_all([role_admin, role_student, role_teacher, role_director])
            db.flush()

            # MEMBERSHIPS
            # =========================
            m1 = Membership(user_id=user1.id, institution_id=inst1.id, role_id=role_student.id)
            m2 = Membership(user_id=user2.id, institution_id=inst1.id, role_id=role_teacher.id)
            m3 = Membership(user_id=user3.id, institution_id=inst1.id, role_id=role_teacher.id)
            m4 = Membership(user_id=user4.id, institution_id=inst1.id, role_id=role_director.id)
            m5 = Membership(user_id=user1.id, institution_id=inst2.id, role_id=role_teacher.id)
            m6 = Membership(user_id=user2.id, institution_id=inst2.id, role_id=role_student.id)
            db.add_all([m1, m2, m3, m4, m5, m6])
            db.flush()

            # GRADES
            # =========================
            g1 = Grade(name="1°", level=1, institution_id=inst1.id)
            g2 = Grade(name="2°", level=2, institution_id=inst1.id)
            g3 = Grade(name="1°", level=1, institution_id=inst2.id)
            g4 = Grade(name="3°", level=3, institution_id=inst3.id)

            db.add_all([g1, g2, g3, g4])
            db.flush()

            # SUBJECTS
            # =========================
            subj1 = Subject(
                name="Matemáticas I",
                description="Álgebra básica",
                code="MAT101",
                credits=5,
                grade_id=g1.id,
                institution_id=inst1.id,
                is_active=True
            )
            subj2 = Subject(
                name="Fisica I",
                description="Mecánica básica",
                code="FIS101",
                credits=6,
                grade_id=g1.id,
                institution_id=inst1.id,
                is_active=True
            )
            subj3 = Subject(
                name="Programación I",
                description="Programación básica",
                code="CS101",
                credits=6,
                grade_id=g2.id,
                institution_id=inst1.id,
                is_active=True
            )
            db.add_all([subj1, subj2, subj3])
            db.flush()

            # COURSE OFFERINGS
            # =========================
            offering1 = CourseOffering(
                subject_id=subj1.id,
                teacher_id=m2.id,
                institution_id=inst1.id,
                group_name="A",
                capacity=30,
                start_time=time(8, 0),
                end_time=time(10, 0),
            )

            offering2 = CourseOffering(
                subject_id=subj2.id,
                teacher_id=m2.id,
                institution_id=inst1.id,
                group_name="A",
                capacity=25,
                start_time=time(10, 0),
                end_time=time(12, 0),
            )

            offering3 = CourseOffering(
                subject_id=subj3.id,
                teacher_id=m3.id,
                institution_id=inst2.id,
                group_name="B",
                capacity=20,
                start_time=time(12, 0),
                end_time=time(14, 0),
            )

            offering4 = CourseOffering(
                subject_id=subj3.id,
                teacher_id=m3.id,
                institution_id=inst2.id,
                group_name="C",
                capacity=20,
                start_time=time(14, 0),
                end_time=time(16, 0),
            )
            db.add_all([offering1, offering2, offering3, offering4])
            db.flush()

            # STUDENTS
            # =========================
            student1 = Student(
                membership_id=m1.id,
                student_number="ITC2026001",
                institution_id=inst1.id,
                current_grade_id=g2.id,
                is_active=True
            )

            student2 = Student(
                membership_id=m6.id,
                institution_id=inst2.id,
                student_number="UDENO2026002",
                current_grade_id=g1.id,
                is_active=True
            )

            db.add_all([
                student1,
                student2
            ])

            db.flush()

        return {
            "institutions": [inst1, inst2, inst3],
            "roles": [role_admin, role_student, role_teacher, role_director],
            "memberships": [m1, m2, m3, m4],
            "grades": [g1, g2, g3, g4],
            "subjects": [subj1, subj2, subj3],
            "offerings": [offering1, offering2, offering3, offering4],
            "students": [student1, student2]
        }

    finally:
        db.close()

if __name__ == "__main__":
    seed_academic()
