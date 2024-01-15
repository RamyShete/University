import pyodbc
from variable import *
import random
import numpy as np
import pygad


def check_numb_student_and_rooms_conflicts(b_id, a_id): # Соответствие размера кабинета размеру учебного класса
    numOfConflict = 0
    cursor.execute(f'select * from [{table_dict["bloks_hs"][0]}] where [{table_dict["bloks_hs"][1]}] = {b_id}')
    value = cursor.fetchall()[0][3]
    cursor.execute(f'select [{table_dict["classes_table"][3]}] from [{table_dict["classes_table"][0]}] where [{table_dict["classes_table"][1]}] = {value}')
    numb_students = cursor.fetchall()[0][0]
    cursor.execute(f'select [{table_dict["rooms_table"][3]}] from [{table_dict["rooms_table"][0]}] where [{table_dict["rooms_table"][1]}] = {a_id}')
    numb_in_room = cursor.fetchall()[0][0]
    if numb_in_room < numb_students:
        numOfConflict += 1
    return numOfConflict


def check_work_time_teachers(b_id): # Учет рабочего графика учителей
    numOfConflict = 0
    cursor.execute(f'select * from [{table_dict["bloks_hs"][0]}] where [{table_dict["bloks_hs"][1]}] = {b_id}')
    value = cursor.fetchall()[0][1]
    cursor.execute(f'select * from [{table_dict["banTable"][0]}] where [{table_dict["banTable"][1]}] = {value}')
    ban = cursor.fetchall()

    if len(ban) == 0:
        pass
    else:
        if (value, b_id) in ban:
            numOfConflict += 1
    return numOfConflict


def check_smena(b_id, t_id): # Проверка временных интервалов для учебных классов
    numOfConflict = 0
    cursor.execute(f'select * from [{table_dict["bloks_hs"][0]}] where [{table_dict["bloks_hs"][1]}] = {b_id}')
    value = cursor.fetchall()[0][3]
    cursor.execute(f'select * from [{table_dict["smena_2"][0]}] where [{table_dict["smena_2"][1]}] = {value}')
    ban = cursor.fetchall()
    if len(ban) == 0:
        pass
    else:
        if value in ban:
            cursor.execute(f'select [{table_dict["lessons_table"][2]}] from [{table_dict["lessons_table"][0]}] join [{table_dict["allTime_table"][0]}] on [{table_dict["lessons_table"][1]}] = [{table_dict["allTime_table"][2]}] where [{table_dict["allTime_table"][1]}] = {t_id} order by [{table_dict["lessons_table"][1]}]')
            if '2 смена' not in cursor.fetchall()[0][0]:
                numOfConflict += 1
    return numOfConflict


def check_nakladki_time(b_id, t_id, b_list, t_list): # Время для блока всегда разное
    numOfConflict = 0
    for ch in range(len(b_list)):
        if b_list[ch] == b_id:
            pass
        else:
            if b_list[ch] == b_id and t_list[ch] == t_id:
                numOfConflict += 1
    return numOfConflict


def check_one_subject_in_day(b_id, b_list, t_list): # Отсутствие одного и того же предмета у одного класса в один день
    numOfConflict = 0
    check_list = []

    for i in range(len(b_list)):
        if b_list[i] == b_id:
            check_list.append([b_list[i], t_list[i]])

    for i in range(len(check_list)):
        for j in range(len(check_list)):
            if i == j:
                numOfConflict += 0
            else:
                if check_list[i][1] // 100 == check_list[j][1] // 100:
                    numOfConflict += 1
    return numOfConflict


def check_onetime_classes(b_id, t_id):
    return 1


def check_onetime_teachers(b_id, t_id):
    return 1


def check_onetime_rooms(t_id, a_id):
    return 1


def check_free_lessons_at_classes(b_id, t_id):
    return 1


def check_different_subject(b_id):
    return 1


def check_numb_subject_in_day(b_id, t_id):
    return 1


def check_sport_subj_to_two_days(b_id, t_id):
    return 1


def check_sport_subj(b_id, t_id):
    return 1


def check_six_subj(b_id, t_id):
    return 1


def check_work_subj_room(b_id, a_id):
    return 1


def check_sport_subj_room(b_id, a_id):
    return 1


def check_chzs(b_id, t_id):
    return 1


def fitness_function(ga_instance, solution, solution_idx):
    numbOfConflicts = 0
    b_list = solution[:len(solution) // 3] # Список bi
    a_list = solution[len(solution)//3:2*len(solution)//3]  # Список ai
    t_list = solution[2*len(solution)//3:]  # Список ti

    for check in range(N):
        numbOfConflicts += check_numb_student_and_rooms_conflicts(b_list[check], a_list[check])
        numbOfConflicts += check_work_time_teachers(b_list[check])
        numbOfConflicts += check_smena(b_list[check], t_list[check])
        numbOfConflicts += check_nakladki_time(b_list[check], t_list[check], b_list, t_list)
        numbOfConflicts += check_one_subject_in_day(b_list[check], b_list, t_list)
        numbOfConflicts += check_onetime_classes(b_list[check], t_list[check])
        numbOfConflicts += check_onetime_teachers(b_list[check], t_list[check])
        numbOfConflicts += check_onetime_rooms(t_list[check], a_list[check])
        numbOfConflicts += check_free_lessons_at_classes(b_list[check], t_list[check])
        numbOfConflicts += check_different_subject(b_list)
        numbOfConflicts += check_numb_subject_in_day(b_list[check], t_list[check])
        numbOfConflicts += check_sport_subj_to_two_days(b_list[check], t_list[check])
        numbOfConflicts += check_sport_subj(b_list[check], t_list[check])
        numbOfConflicts += check_six_subj(b_list[check], t_list[check])
        numbOfConflicts += check_work_subj_room(b_list[check], t_list[check])
        numbOfConflicts += check_sport_subj_room(b_list[check], a_list[check])
        numbOfConflicts += check_chzs(b_list[check], t_list[check])

    return 1 / ((1.0 * numbOfConflicts) + 1)


def on_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])


# Получение количества блоков занятий из БД
conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=D:\4\diplom\school_helper\School_helper.accdb;'
conn = pyodbc.connect(conn_string)
print("Connected to database")

cursor = conn.cursor()

block_data, cabinet_data, time_data, time_data1, time_data2, smena = [], [], [], [], [], []
cursor.execute('select * from [' + table_dict['bloks_hs'][0] + ']')
for i in cursor.fetchall():
    # block_data.append(i[0])
# block_data = np.array(block_data)
    block_data.append(list([i[0], i[1], i[2], i[3], i[4], i[5]]))
cursor.execute('select * from [' + table_dict['rooms_table'][0] + ']')
for i in cursor.fetchall():
    if i[0] in [3, 4, 5]:
        pass
    else:
        cabinet_data.append(list([i[0], i[1], i[2]]))

# cursor.execute('select * from [' + table_dict['allTime_table'][0] + ']')
# for i in cursor.fetchall():
#     time_data.append([i[0], i[1], i[2]])

cursor.execute('select * from [' + table_dict['allTime_table'][0] + ']')
time_curs = cursor.fetchall()
for i in time_curs:
    cursor.execute(f'select [{table_dict["lessons_table"][2]}] from [{table_dict["lessons_table"][0]}] where [{table_dict["lessons_table"][1]}] = {i[2]}')
    if '1 смена' in cursor.fetchall()[0][0]:
        time_data1.append(list([i[0], i[1], i[2]]))
    else:
        time_data2.append(list([i[0], i[1], i[2]]))

cursor.execute('select * from [' + table_dict['smena_2'][0] + ']')
for i in cursor.fetchall():
    for j in i:
        smena.append(j)

# Создать пустой список для хранения особей
population = []

# Создать пустые списки для хромосом
individual = []

N = len(block_data)

# Формирование популяции
for n in range(N): # количество особей
    for chrom in range(3): # количество хромосом
        for n in range(N): # начальное количество генов
            for intens in range(block_data[n][5]): # интенсивность
                if chrom == 0:
                    individual.append(block_data[n][0])
                elif chrom == 1:
                    individual.append(random.choice(cabinet_data)[0])
                else:
                    if len(smena) == 0:
                        individual.append(random.choice(time_data1)[0])
                    else:
                        if block_data[n][3] in smena:
                            individual.append(random.choice(time_data2)[0])
                        else:
                            individual.append(random.choice(time_data1)[0])
    # Добавить особь в популяцию
    population.append(individual.copy())
    individual.clear()

# Преобразовать популяцию в массив NumPy
population = np.array(population)

# Вывести популяцию
# for i, individual in enumerate(population):
#     print(f"Особь {i + 1}:")
#     print(individual)

ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=10,
                       fitness_func=fitness_function,
                       init_range_low=-4,
                       init_range_high=4,
                       parent_selection_type="tournament",
                       keep_elitism=1,
                       K_tournament=3,
                       crossover_type="uniform",
                       crossover_probability=0.5,
                       mutation_type=None,
                       initial_population=population,
                       on_generation=on_gen,
                       gene_type=int,
                       )

ga_instance.run()

block, all_schedule = [], []
# schedule_list = [ga_instance.best_solution()[0][i:i + 3].tolist() for i in range(0, len(ga_instance.best_solution()[0]), 3)]
b_list = ga_instance.best_solution()[0][:len(ga_instance.best_solution()[0]) // 3] # Список bi
a_list = ga_instance.best_solution()[0][len(ga_instance.best_solution()[0])//3:2*len(ga_instance.best_solution()[0])//3]  # Список ai
t_list = ga_instance.best_solution()[0][2*len(ga_instance.best_solution()[0])//3:]  # Список ti

cursor.execute(f'delete from [{schedule_itog["schedule"][0]}]')
for b in range(len(b_list)):
    block.clear()
    cursor.execute(f'select * from [{table_dict["bloks_hs"][0]}] where [{table_dict["bloks_hs"][1]}] = {b_list[b]}')
    for i in cursor.fetchall():
        for j in i:
            block.append(j)
    # cursor.execute(
    #     f'select [{table_dict["classes_table"][2]}] from [{table_dict["classes_table"][0]}] where [{table_dict["classes_table"][1]}] = {block[3]}')
    name_class = block[3]
    cursor.execute(
        f'select [{table_dict["subject_table"][3]}] from [{table_dict["subject_table"][0]}] where [{table_dict["subject_table"][1]}] = {block[2]}')
    name_subject = cursor.fetchall()[0][0]
    cursor.execute(
        f'select [{table_dict["teachers_table"][2]}] from [{table_dict["teachers_table"][0]}] where [{table_dict["teachers_table"][1]}] = {block[1]}')
    name_teacher = cursor.fetchall()[0][0]
    all_schedule.append(
        [name_class, t_list[b], name_subject + '\n' + name_teacher[:name_teacher.index('\n')] + '\n' + str(a_list[b])])
all_schedule = sorted(all_schedule, key=lambda sched: (sched[0], sched[1]))
query_ins = f'insert into [{schedule_itog["schedule"][0]}] values (?,?,?)'
for al in all_schedule:
    cursor.execute(query_ins, al)
    cursor.commit()
#
#
# print('Best solution : ', ga_instance.best_solution()[0])










