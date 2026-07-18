from datetime import time

from app.db.sync_db import get_session_local
from app.models.institution import Institution
from app.models.role import Role
from app.models.subject import Subject
from app.models.course_offering import CourseOffering

SessionLocal = get_session_local()


def seed_academic():
    db = SessionLocal()

    # =========================
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
    db.commit()

    # =========================
    # ROLES
    # =========================
    role1 = Role(name="admin", description="Administrador del sistema")
    role2 = Role(name="student", description="Alumno inscrito")
    role3 = Role(name="teacher", description="Profesor que imparte cursos")
    role4 = Role(name="director", description="Director de la institucion")

    db.add_all([role1, role2, role3, role4])
    db.commit()

    # =========================
    # SUBJECTS
    # =========================
    subj1 = Subject(
        name="Matemáticas I",
        description="Álgebra básica",
        code="MAT101",
        credits=5,
        institution_id=inst1.id,
        is_active=True
    )

    subj2 = Subject(
        name="Fisica I",
        description="Mecánica básica",
        code="FIS101",
        credits=6,
        institution_id=inst1.id,
        is_active=True
    )

    subj3 = Subject(
        name="Programación Orientada a Objetos",
        description="Introducción a Python",
        code="CS101",
        credits=8,
        institution_id=inst1.id,
        is_active=True
    )

    subj4 = Subject(
        name="Base de Datos",
        description="Fundamentos de SQL",
        code="DB101",
        credits=7,
        institution_id=inst2.id,
        is_active=True
    )

    db.add_all([subj1, subj2, subj3, subj4])
    db.commit()

    # =========================
    # COURSE OFFERINGS
    # =========================
    offering1 = CourseOffering(
        subject_id=subj1.id,
        teacher_id=1,
        institution_id=inst1.id,
        group="A",
        capacity=30,
        start_time=time(8, 0),
        end_time=time(10, 0),
    )

    offering2 = CourseOffering(
        subject_id=subj2.id,
        teacher_id=2,
        institution_id=inst1.id,
        group="B",
        capacity=25,
        start_time=time(10, 0),
        end_time=time(12, 0),
    )

    offering3 = CourseOffering(
        subject_id=subj3.id,
        teacher_id=3,
        institution_id=inst2.id,
        group="C",
        capacity=20,
        start_time=time(12, 0),
        end_time=time(14, 0),
    )

    offering4 = CourseOffering(
        subject_id=subj4.id,
        teacher_id=3,
        institution_id=inst3.id,
        group="D",
        capacity=20,
        start_time=time(12, 0),
        end_time=time(14, 0),
    )

    db.add_all([offering1, offering2, offering3, offering4])
    db.commit()

    db.close()

    return {
        "institutions": [inst1, inst2, inst3],
        "roles": [role1, role2, role3, role4],
        "subjects": [subj1, subj2, subj3],
        "offerings": [offering1, offering2, offering3, offering4],
    }


if __name__ == "__main__":
    seed_academic()