#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):

    # Class Attributes
    __tablename__ = 'students'

    # Constraints are stores within __table_args__
    __table_args__ = (
        PrimaryKeyConstraint(
            'id', # the column that makes the primary key
            name='id_pk'),
        UniqueConstraint(
            'email', # the column email for which uniqueness is enforced
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12', # ensures grade column falls between a range of 1 to 12
            name='grade_between_1_and_12')
    )
    Index('index_name', 'name') # name is the column to be indexed; Can help improve query performance

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    # making output human readable

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # Working with sessions to interact with our db

    Session = sessionmaker(bind=engine) # session configuration using the session maker class

    # An instance of Session class is created for interacting with the db. This session instance is what you use to add,query or modify data in a db

    session = Session()

    # Populating our database with data. Syntax is same as instantaiating any python class

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # After creating the student object sesseion.add generates statement and commit execute it and saves it to db
    #session.add(albert_einstein) # this is if we are adding only one record

    session.bulk_save_objects([albert_einstein, alan_turing]) # use bulk_save_objects for multiple objects
    session.commit()

    # Reading Records

    students = session.query(Student).all()

    print(students)

    # reading specific columns. Query method returns complete records from data model passed as argument

    names = [name for name in session.query(Student.name)]

    print(names)

    # ordering: use order by method to sort it out

    students_by_name = [student for student in session.query(
        Student.name).order_by(
        Student.name)]

    print(students_by_name)

    # to sort by descending order we use desc function

    students_by_grade_desc = [student for student in session.query(
        Student.name, Student.grade).order_by(
        desc(Student.grade))]

    print(students_by_grade_desc)

    # Limiting works too

    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).first()

    print(oldest_student)

    # using func to handle count

    student_count = session.query(func.count(Student.id)).first()

    print(student_count)

    # Filtering

    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11)

    for record in query:
        print(record.name)
    
    # Updating Data

    for student in session.query(Student):
        student.grade += 1

    session.commit()

    print([(student.name,
        student.grade) for student in session.query(Student)])
    
    # Deleting Data

    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")        

    # retrieve first matching record as object
    albert_einstein = query.first()

    # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()

    print(albert_einstein)
    
    

    print(f"New student ID is {albert_einstein.name}.")