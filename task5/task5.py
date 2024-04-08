from sqlalchemy import create_engine, MetaData, Table
from decouple import config
from collections import Counter

import urllib

from sqlalchemy import create_engine, MetaData, Table, select, desc, func

def url_encode(word):
    """
        Encode the given word in URL format.
    """
    new_word = urllib.parse.quote(word.encode('utf-8'), safe='')
    return new_word

def is_prime(n, i=2):
    """
        Check if integer n is a prime number.
    """
    if n <= 2:
        return n == 2
    if n % i == 0:
        return False
    if i * i > n:
        return True
    return is_prime(n, i + 1)


def max_instructors():
    """
        Connect the database using sqlalchemy and return name,id,num count of instructor(s) who has taught maximum number of classes onthe day 'W'.
        Return name of courses which have been taught in both Winter semester and Spring semester.
    """
    database = f"postgresql+psycopg2://{config('DB_USER')}:{url_encode(config('DB_PASSWORD'))}@{config('DB_HOST')}/{config('DB_NAME')}"

    engine = create_engine(database, pool_pre_ping=True)
    metadata = MetaData()

    instructor_table = Table('instructor', metadata, autoload_with=engine)
    timeslot_table = Table('time_slot', metadata, autoload_with=engine)
    section_table = Table('section', metadata, autoload_with=engine)
    course_table = Table('course', metadata, autoload_with=engine)

    #Winter sections
    winter_sections = select(section_table).where(
        section_table.c.semester == 'Winter'
    ).alias('winter_sections')

    #Summer Sections
    spring_sections = select(section_table).where(
        section_table.c.semester == 'Spring'
    ).alias('spring_sections')

    winter_courses = select(course_table).where(
        course_table.c.course_id == winter_sections.c.course_id
    )

    spring_courses = select(course_table).where(
        course_table.c.course_id == spring_sections.c.course_id
    )

    #Order of connecting the data together
    w_time_slots = select(timeslot_table).where(
        timeslot_table.c.day == 'W'
    ).alias('w_time_slots')

    w_sections = select(section_table).where(
        section_table.c.time_slot_id == w_time_slots.c.time_slot_id
    ).alias('w_sections')

    w_courses = select(course_table).where(
        course_table.c.course_id == w_sections.c.course_id
    ).alias('w_courses')

    instructor_query = select(
        instructor_table
    ).where(instructor_table.c.dept_name == w_courses.c.dept_name)

    with engine.connect() as connection:
        sorted_instructors = connection.execute(instructor_query).fetchall()
        winter = connection.execute(winter_courses).fetchall()
        spring = connection.execute(spring_courses).fetchall()

    winter_cour = [win.title for win in winter]
    spring_cour = [spr.title for spr in spring]

    count = 0
    instructor_counts = Counter([record.name for record in sorted_instructors])
    #To Get the max number of all instructors
    max_count = max(instructor_counts.values())

    instructors_with_max_count = []    
    for instructor_name, count in instructor_counts.items():
        if count == max_count:
            instructors_with_max_count.append(instructor_name)

    
    max_instructors_list = []
    added_names = []
    for instructor in sorted_instructors:
        for ins_name in instructors_with_max_count:
            if instructor.name == ins_name:
                if instructor.name not in added_names:
                    temp = {}
                    temp['name'] = instructor.name
                    temp['id'] = instructor.id
                    temp['num'] = max_count
                    max_instructors_list.append(temp)
                added_names.append(ins_name)

    return max_instructors_list, winter_cour, spring_cour

max_instructors, win_cour, spr_cour = max_instructors()

print("---------Task 5 output----------")
print("-----Winter Couses------")
for win_course in win_cour:
    print(win_course)
print("--------------------------------")
print("----Spring Couses----")
for spr_course in spr_cour:
    print(spr_course)
print("--------------------------------")
print("name,id,num count of instructor(s) who has taught maximum number of classes onthe day 'W'.")
for instru in max_instructors:
    print(f"{instru['name']}, {instru['id']}, {instru['num']}")

print("---------End 5 output----------")