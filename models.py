from sqlalchemy import Column, Integer, String, Table, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

student_courses = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

teacher_courses = Table(
    "teacher_courses",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)

    courses = relationship(
        "Course",
        secondary=student_courses,
        back_populates="students"
    )

    parents = relationship(
        "Parent",
        secondary="parent_students",
        back_populates="students"
    )



class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration = Column(String, nullable=False)

    students = relationship(
        "Student",
        secondary=student_courses,
        back_populates="courses"
    )
    teachers = relationship(
    "Teacher",
    secondary=teacher_courses,
    back_populates="courses"
    )


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    class_id = Column(Integer,
    ForeignKey("classes.id"),nullable=False)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    courses = relationship(
    "Course",
    secondary=teacher_courses,
    back_populates="teachers"
)

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    students = relationship(
        "Student",
        secondary="parent_students",
        back_populates="parents"
    )

parent_students = Table(
    "parent_students",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("parents.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
)


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    paid_amount = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False)
    student_id = Column(Integer,ForeignKey("students.id"), nullable= False)
    student = relationship("Student")
    

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    date = Column(Date, nullable=False)

    status = Column(String, nullable=False)
    student = relationship("Student")

class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    exam_name = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)

    student = relationship("Student")
    course = relationship("Course")

class ParentMeeting(Base):
    __tablename__ = "parent_meetings"

    id = Column(Integer, primary_key=True, index=True)

    parent_id = Column(
        Integer,
        ForeignKey("parents.id"),
        nullable=False
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    meeting_date = Column(Date, nullable=False)
    purpose = Column(String, nullable=False)

    parent = relationship("Parent")
    student = relationship("Student")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")