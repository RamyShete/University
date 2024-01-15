import pyodbc
from variable import *

try:
    conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=D:\4\diplom\school_helper\School_helper.accdb;'
    conn = pyodbc.connect(conn_string)
    print("Connected to database")

    cursor = conn.cursor()

    print("Processes create table")

    table_subjects = 'CREATE TABLE [' + table_dict['subject_table'][0] + '] ([' + table_dict['subject_table'][1] +\
                     '] INTEGER, [' + table_dict['subject_table'][2] + '] TEXT(255), [' +\
                     table_dict['subject_table'][3] + '] TEXT(255))'
    cursor.execute(table_subjects)
    cursor.commit()

    table_classes = 'CREATE TABLE [' + table_dict['classes_table'][0] + '] ([' + table_dict['classes_table'][1] +\
                    '] INTEGER, [' + table_dict['classes_table'][2] + '] TEXT(255), [' +\
                    table_dict['classes_table'][3] + '] INTEGER)'
    cursor.execute(table_classes)
    cursor.commit()

    table_rooms = 'CREATE TABLE [' + table_dict['rooms_table'][0] + '] ([' + table_dict['rooms_table'][1] +\
                  '] INTEGER, [' + table_dict['rooms_table'][2] + '] TEXT(255), [' + table_dict['rooms_table'][3] +\
                  '] INTEGER)'
    cursor.execute(table_rooms)
    cursor.commit()

    table_teachers = 'CREATE TABLE [' + table_dict['teachers_table'][0] + '] ([' + table_dict['teachers_table'][1] +\
                     '] INTEGER, [' + table_dict['teachers_table'][2] + '] TEXT(255), [' +\
                     table_dict['teachers_table'][3] + '] TEXT(255), [' + table_dict['teachers_table'][4] + '] TEXT(255))'
    cursor.execute(table_teachers)
    cursor.commit()

    table_lessons = 'CREATE TABLE [' + table_dict['lessons_table'][0] + '] ([' + table_dict['lessons_table'][1] + \
                    '] INTEGER, [' + table_dict['lessons_table'][2] + '] TEXT(255))'
    cursor.execute(table_lessons)
    cursor.commit()

    table_days = 'CREATE TABLE [' + table_dict['days_table'][0] + '] ([' + table_dict['days_table'][1] + \
                 '] INTEGER, [' + table_dict['days_table'][2] + '] TEXT(255))'
    cursor.execute(table_days)
    cursor.commit()

    table_allTime = 'CREATE TABLE [' + table_dict['allTime_table'][0] + '] ([' + table_dict['allTime_table'][1] +\
                  '] INTEGER, [' + table_dict['allTime_table'][2] + '] INTEGER, [' + table_dict['allTime_table'][3] +\
                  '] INTEGER)'
    cursor.execute(table_allTime)
    cursor.commit()

    print("Created tables")

    for i in range(len(subjects)):
        query = 'INSERT INTO [' + table_dict['subject_table'][0] + '] VALUES (?,?,?)'
        cursor.execute(query, subjects[i])
        cursor.commit()
    for i in range(1, len(week) + 1):
        query = 'insert into [' + table_dict['days_table'][0] + '] values (?,?)'
        inp = [i, week[i-1]]
        cursor.execute(query, inp)
        cursor.commit()
    print("Inserted table subjects")

    query_create_ban = 'CREATE TABLE [' + table_dict['banTable'][0] + '] ([' + table_dict['banTable'][1] + \
                       '] INTEGER, [' + table_dict['banTable'][2] + '] INTEGER)'
    cursor.execute(query_create_ban)
    cursor.commit()

    table_subjectPlans = 'CREATE TABLE [' + table_dict['sp_table'][0] + '] ([' +\
                         table_dict['sp_table'][1] + '] INTEGER, [' + table_dict['sp_table'][2] +\
                         '] INTEGER, [' + table_dict['sp_table'][3] + '] INTEGER)'
    cursor.execute(table_subjectPlans)
    cursor.commit()

    table_teachers_classes = 'CREATE TABLE [' + table_dict['thachers_to_classes'][0] + '] ([' +\
                         table_dict['thachers_to_classes'][1] + '] INTEGER, [' + table_dict['thachers_to_classes'][2] +\
                         '] INTEGER, [' + table_dict['thachers_to_classes'][3] + '] INTEGER)'
    cursor.execute(table_teachers_classes)
    cursor.commit()

    table_bloks_hs = 'CREATE TABLE [' + table_dict['bloks_hs'][0] + '] ([' + table_dict['bloks_hs'][1] +\
                     '] INTEGER, [' + table_dict['bloks_hs'][2] + '] INTEGER, [' + table_dict['bloks_hs'][3] +\
                     '] INTEGER, [' + table_dict['bloks_hs'][4] + '] INTEGER, [' + table_dict['bloks_hs'][5] +\
                     '] INTEGER, [' + table_dict['bloks_hs'][6] + '] INTEGER)'
    cursor.execute(table_bloks_hs)
    cursor.commit()

    table_smena = 'CREATE TABLE [' + table_dict['smena_2'][0] + '] ([' + table_dict['smena_2'][1] + '] INTEGER)'
    cursor.execute(table_smena)
    cursor.commit()

    schedulee = 'CREATE TABLE [' + schedule_itog['schedule'][0] + '] ([' + schedule_itog['schedule'][1] +\
                '] TEXT(255), [' + schedule_itog['schedule'][2] + '] TEXT(255), [' + schedule_itog['schedule'][3] + \
                '] TEXT(255))'
    cursor.execute(schedulee)
    cursor.commit()


except pyodbc.Error as e:
    print("Error: ", e)