import dearpygui.dearpygui as dpg
from variable import *
import pyodbc

dpg.create_context()

conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=D:\4\diplom\school_helper\School_helper.accdb;'
conn = pyodbc.connect(conn_string)
print("Connected to database")
tag_list = []

cursor = conn.cursor()

with dpg.font_registry():
    with dpg.font("georgia.ttf", 16, default_font=True, id="Default font") as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        biglet = remap_big_let

        for i1 in range(big_let_start, big_let_end + 1):
            dpg.add_char_remap(i1, biglet)
            dpg.add_char_remap(i1 + alph_len, biglet + alph_len)
            biglet += 1


def to_cyr(instr):
    out = []
    for i in range(0, len(instr)):
        if ord(instr[i]) in range(big_let_start, small_let_end + 1):
            out.append(chr(ord(instr[i]) + alph_shift))
        else:
            out.append(instr[i])
    return ''.join(out)


def _log(sender, app_data):
    return app_data


def add_subject(value):
    for i in range(int(value)):
        dpg.delete_item(combo_tags[i])
        dpg.add_combo(combo_subj, tag=combo_tags[i], before='add_val_subj', callback=_log)


def list_subject(st):
    stroke = []
    for i in range(len(st)):
        if st[i].isupper() and i > 0:
            stroke.append(st[:i])
            stroke.append(st[i:])
    return stroke


def insert_table_allTime():
    query_del = 'delete from [' + table_dict['allTime_table'][0] + ']'
    cursor.execute(query_del)
    cursor.commit()

    query_ins = 'insert into [' + table_dict['allTime_table'][0] + '] values ' + '(?,?,?)'
    data = []
    cursor.execute('select * from [' + table_dict['days_table'][0] + ']')
    day_id = cursor.fetchall()
    cursor.execute('select * from [' + table_dict['lessons_table'][0] + ']')
    les_id = cursor.fetchall()

    for i in range(len(day_id)):
        for j in range(len(les_id)):
            new_id = str(day_id[i][0]) + str(les_id[j][0])
            data.append(list([int(new_id), day_id[i][0], les_id[j][0]]))

    for i in range(len(data)):
        cursor.execute(query_ins, data[i])
        cursor.commit()
    print('insert table allTime')


def query_update_lessons(val, printed_tag, value):
    query_del = 'delete from [' + table_dict[printed_tag][0] + ']'
    cursor.execute(query_del)
    cursor.commit()

    query_ins = 'insert into [' + table_dict[printed_tag][0] + '] values ' + val
    data = []
    sm1 = dpg.get_value('kol_les_1_sm')
    sm2 = dpg.get_value('kol_les_2_sm')
    if value is None:
        for i in range(1, int(sm1) + 1):
            data.append(list([f'1{i}', f'{i} урок (1 смена)']))
    else:
        for i in range(1, int(sm2) + int(value)):
            if i < int(value):
                data.append(list([f'1{i}', f'{i} урок (1 смена)']))
            elif i >= int(value) and i < int(sm1) + 1:
                data.append(list([f'1{i}', f'{i}/{(i - int(value) + 1)} урок (1/2 смена)']))
            else:
                data.append((list([f'2{(i - int(value) + 1)}', f'{(i - int(value) + 1)} урок (2 смена)'])))
    for i in range(len(data)):
        cursor.execute(query_ins, data[i])
        cursor.commit()

    insert_table_allTime()
    print('added')


def query_insert(val, printed_tag, value):
    query = 'insert into ['
    data = []
    combo_data = ''

    if printed_tag == 'teachers_table':
        for combo_i in range(int(value)):
            combo_data += dpg.get_value(combo_tags[combo_i]) + '\n'
        for tag in range(len(rows_tags[printed_tag])):
            if rows_tags[printed_tag][tag] == 'teachers_subjects':
                data.append(combo_data)
            elif rows_tags[printed_tag][tag] == 'teacher_flf':
                st = to_cyr(dpg.get_value(rows_tags[printed_tag][tag]))
                st = st.replace(" ", '\n', 1)
                data.append(st)
            elif rows_tags[printed_tag][tag] == 'job_title':
                st = to_cyr(dpg.get_value(rows_tags[printed_tag][tag]))
                st = st.replace(' и ', '\nи ')
                data.append(st)
            else:
                data.append(to_cyr(dpg.get_value(rows_tags[printed_tag][tag])))
    elif printed_tag == 'lessons_table':
        pass
    else:
        for tag in range(len(rows_tags[printed_tag])):
            data.append(to_cyr(dpg.get_value(rows_tags[printed_tag][tag])))

    query += table_dict[printed_tag][0] + '] values ' + val

    cursor.execute(query, data)
    cursor.commit()
    wind_success()


def query_update(printed_tag, value, num_row):
    query = 'update ['
    data = []
    combo_data = ''

    if printed_tag == 'teachers_table':
        for combo_i in range(int(value)):
            combo_data += dpg.get_value(combo_tags[combo_i]) + '\n'
        for tag in range(len(rows_tags[printed_tag])):
            if rows_tags[printed_tag][tag] == 'teachers_subjects':
                data.append(combo_data)
            elif rows_tags[printed_tag][tag] == 'teacher_flf':
                st = to_cyr(dpg.get_value(rows_tags[printed_tag][tag]))
                st = st.replace(" ", '\n', 1)
                data.append(st)
            elif rows_tags[printed_tag][tag] == 'job_title':
                st = to_cyr(dpg.get_value(rows_tags[printed_tag][tag]))
                st = st.replace(' и ', '\nи ')
                data.append(st)
            else:
                data.append(to_cyr(dpg.get_value(rows_tags[printed_tag][tag])))
    else:
        for tag in range(len(rows_tags[printed_tag])):
            data.append(to_cyr(dpg.get_value(rows_tags[printed_tag][tag])))

    query += table_dict[printed_tag][0] + '] set '
    for i in range(len(table_dict[printed_tag]) - 1):
        stroke = '[' + table_dict[printed_tag][i+1] + ']=\'' + data[i] + '\', '
        query += stroke

    cursor.execute(query[:-2] + ' where [' + table_dict[printed_tag][1] + '] = ' + str(num_row))
    cursor.commit()
    wind_success()


def query_delete(printed_tag, num_row):
    query = 'delete from [' + table_dict[printed_tag][0] + ']'
    cursor.execute(query + ' where ['
                       + table_dict[printed_tag][1] + '] = ' + str(num_row))

    cursor.commit()
    wind_success()


def limit_teacherToClasses(tt, clt):
    tag = 'thachers_to_classes'
    ttcl = cursor_select(tag)

    query_ins = f'insert into [{table_dict[tag][0]}] values (?,?,?)'

    if len(ttcl) == 0:
        for teach in range(len(tt)):
            for clas in range(len(clt)):
                tg = str(teach) + str(clas)
                print(tg)
                if dpg.get_value(tg) is True:
                    cursor.execute(query_ins, list([tt[teach][0], tt[teach][1], clt[clas][0]]))
                    cursor.commit()
                    print('saved')
    else:
        for teach in range(len(tt)):
            for clas in range(len(clt)):
                tg = str(teach) + str(clas)
                value, inp = check_condition(tag, clt[clas][0], tt[teach][0], tt[teach][1])
                if value is True and dpg.get_value(tg) is True:
                    pass
                elif value is False and dpg.get_value(tg) is True:
                    cursor.execute(query_ins, list([tt[teach][0], tt[teach][1], clt[clas][0]]))
                    cursor.commit()
                    print('saved')
                elif value is True and dpg.get_value(tg) is False:
                    cursor.execute(f'delete from [{table_dict[tag][0]}] where [{table_dict[tag][1]}] = {tt[teach][0]} and [{table_dict[tag][2]}] = {tt[teach][1]} and [{table_dict[tag][2]}] = {clt[clas][0]}')
                    cursor.commit()
                    print('deleted')



def limit_teachers_setWorkTime(sender, dt, lt):
    tag = 'banTable'
    query_ins = 'insert into [' + table_dict[tag][0] + '] values (?,?)'
    cursor.execute('select * from [' + table_dict[tag][0] + '] where [' + table_dict[tag][1] + '] =' + str(sender))
    data_from_table = cursor.fetchall()

    list_alltime = []
    list_tg = []
    for val in range(len(data_from_table)):
        list_alltime.append(list([data_from_table[val][0], data_from_table[val][1]]))
    for day in range(len(dt)):
        for lesson in range(len(lt)):
            tg = str(dt[day][0]) + str(lt[lesson][0])
            list_tg.append(tg)

    if len(data_from_table) == 0:
        for day in range(len(dt)):
            for lesson in range(len(lt)):
                tg = str(dt[day][0]) + str(lt[lesson][0])
                if dpg.get_value(tg) is False:
                    cursor.execute(query_ins, list([sender, int(tg)]))
                    cursor.commit()
    else:
        for tgs in list_tg:
            if dpg.get_value(tgs) is False:
                if list([int(sender), int(tgs)]) in list_alltime:
                    pass
                else:
                    cursor.execute(query_ins, list([int(sender), int(tgs)]))
                    cursor.commit()
            if dpg.get_value(tgs) is True:
                if list([int(sender), int(tgs)]) in list_alltime:
                    query_del = 'delete from [' + table_dict[tag][0] + '] where [' + table_dict[tag][1] +\
                                '] = ' + str(sender) + ' and [' + table_dict[tag][2] + '] = ' + tgs
                    cursor.execute(query_del)
                    cursor.commit()


def cursor_select(tag):
    cursor.execute('select * from [' + table_dict[tag][0] + ']')
    return cursor.fetchall()


def chWind_setWorkTime(sender, app_data, user_data):
    dt = cursor_select('days_table')
    lt = cursor_select('lessons_table')
    tt = cursor_select('teachers_table')
    bt = cursor_select('banTable')

    list_alltime = []
    for val in range(len(bt)):
        list_alltime.append(list([bt[val][0], bt[val][1]]))
    ind = '\n'
    with dpg.window(label=f'Рабочее время {tt[sender - 1][1][:tt[sender - 1][1].index(ind)]}',
                    pos=(100, 100), width=900, height=300):
        with dpg.table(header_row=True, scrollX=True,
                       borders_innerH=False, borders_outerH=False, borders_innerV=False,
                       borders_outerV=False, policy=dpg.mvTable_SizingFixedFit):
            dpg.add_table_column(label='')
            for i in range(len(lt)):
                dpg.add_table_column(label=lt[i][1].replace(' (', '\n('))

            for i in range(len(dt)):
                with dpg.table_row():
                    for j in range(len(lt) + 1):
                        if j == 0:
                            dpg.add_text(dt[i][1])
                        else:
                            tg = str(dt[i][0]) + str(lt[j - 1][0])
                            dpg.delete_item(tg)
                            if list([int(sender), int(tg)]) in list_alltime:
                                dpg.add_checkbox(tag=tg, default_value=False)
                            else:
                                dpg.add_checkbox(tag=tg, default_value=True)
        dpg.add_button(label='Сохранить', callback=lambda: limit_teachers_setWorkTime(sender, dt, lt))


def check_condition(tag, val_1, val_2, val_3):
    cursor.execute('select * from [' + table_dict[tag][0] + ']')
    sp = cursor.fetchall()
    sp_list = []
    if len(sp) == 0:
        pass
    else:
        for i in sp:
            sp_list.append(list([i[0], i[1], i[2]]))
    value = False
    input_value = 0
    if val_3 is None:
        for i in range(len(sp_list)):
            if sp_list[i][0] == val_2 and sp_list[i][1] == val_1:
                value = True
                input_value = sp_list[i][2]
        return value, input_value
    else:
        for i in range(len(sp_list)):
            if sp_list[i][0] == val_2 and sp_list[i][1] == val_3 and sp_list[i][2] == val_1:
                value = True
                input_value = sp_list[i][2]
        return value, input_value


def wind_limitation():
    dpg.delete_item('wind_limit')
    with dpg.window(label='Условия', tag='wind_limit', width=1100, height=480, pos=(50, 50)):
        tt = cursor_select('teachers_table')
        tag_tt = 'teachers_table'
        st = cursor_select('subject_table')
        tag_st = 'subject_table'
        tt_list = []
        for i in tt:
            subject = find_subject_id(i[3], st)
            for j in subject:
                if j != '':
                    tt_list.append(list([i[0], j]))
        ttcl = cursor_select('thachers_to_classes')

        with dpg.tree_node(label='1. Нагрузка учителей'):
            clt = cursor_select('classes_table')
            with dpg.table(header_row=True, scrollX=True, borders_innerH=True, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True, policy=dpg.mvTable_SizingFixedFit):
                dpg.add_table_column(label=table_dict['teachers_table'][2])
                dpg.add_table_column(label=table_dict['teachers_table'][4])
                for i in range(len(clt)):
                    dpg.add_table_column(label=clt[i][1])

                for i in range(len(tt_list)):
                    with dpg.table_row():
                        for j in range(len(clt) + 2):
                            if j == 0:
                                cursor.execute(f'select [{table_dict[tag_tt][2]}] from [{table_dict[tag_tt][0]}] where [{table_dict[tag_tt][1]}] = {tt_list[i][0]}')
                                stroke = cursor.fetchall()
                                dpg.add_text(stroke[0][0])
                            elif j == 1:
                                cursor.execute(f'select [{table_dict[tag_st][2]}] from [{table_dict[tag_st][0]}] where [{table_dict[tag_st][1]}] = {tt_list[i][1]}')
                                stroke = cursor.fetchall()
                                dpg.add_text(stroke[0][0])
                            else:
                                tg1 = str(i) + str(j - 2)
                                if len(ttcl) != 0:
                                    value, input_value = check_condition('thachers_to_classes', clt[j - 2][0], tt_list[i][0], tt_list[i][1])
                                    if value is True:
                                        dpg.delete_item(tg1)
                                        dpg.add_checkbox(tag=tg1, default_value=True)
                                    else:
                                        dpg.delete_item(tg1)
                                        dpg.add_checkbox(tag=tg1)
                                else:
                                    dpg.delete_item(tg1)
                                    dpg.add_checkbox(tag=tg1)
            dpg.add_button(label='Сохранить', callback=lambda: limit_teacherToClasses(tt_list, clt))

        with dpg.tree_node(label='2. Рабочее время учителей'):
            with dpg.table(header_row=False, scrollX=True, borders_innerH=False, borders_outerH=False,
                           borders_innerV=False, borders_outerV=False, policy=dpg.mvTable_SizingFixedFit):
                dpg.add_table_column()
                dpg.add_table_column()
                for name in range(len(tt)):
                    with dpg.table_row():
                        for i in range(2):
                            if i == 0:
                                dpg.delete_item(tt[name][1][:tt[name][1].index('\n')])
                                dpg.add_text(tt[name][1], tag=tt[name][1][:tt[name][1].index('\n')])
                            else:
                                dpg.add_button(label='Настроить', tag=tt[name][0])
                                dpg.configure_item(tt[name][0], user_data=dpg.last_item(), callback=chWind_setWorkTime)
                                tag_list.append(str(tt[name][0]))


def wind_adding():
    dpg.delete_item('add_row')
    with dpg.window(label="Добавление записи", tag='add_row', width=400, height=300, pos=(500, 200)):
        for i in range(len(rows_tags[printed_tag])):
            dpg.delete_item(rows_tags[printed_tag][i])

        val = '(?,?'

        if printed_tag != 'teachers_table':
            if printed_tag == 'lessons_table':
                val += ')'
                dpg.add_text('Выберите количество учебных смен')

                def _selection(sender, app_data, user_data):
                    dpg.delete_item('kol_les_1_sm')
                    dpg.delete_item('les_1_sm')
                    dpg.delete_item('kol_les_2_sm')
                    dpg.delete_item('les_2_sm')
                    dpg.delete_item('what_sm2')
                    dpg.delete_item('sm1_sm2')
                    for item in user_data:
                        if item != sender:
                            dpg.set_value(item, False)
                    if sender == user_data[0]:
                        dpg.add_text(f'Введите количество уроков в 1 смену:', tag='les_1_sm', before='add_val_les')
                        dpg.add_input_text(tag='kol_les_1_sm', before='add_val_les')
                    else:
                        dpg.add_text(f'Введите количество уроков в 1 смену:', tag='les_1_sm', before='add_val_les')
                        dpg.add_input_text(tag='kol_les_1_sm', before='add_val_les')
                        dpg.add_text(f'Введите количество уроков в 2 смену:', tag='les_2_sm', before='add_val_les')
                        dpg.add_input_text(tag='kol_les_2_sm', before='add_val_les')
                        dpg.add_text('С какого урока начинается вторая смена?', tag='what_sm2', before='add_val_les')
                        dpg.add_input_text(tag='sm1_sm2', before='add_val_les')

                items = (
                    dpg.add_selectable(label="1 смена"),
                    dpg.add_selectable(label="2 смены"),
                )
                for item in items:
                    dpg.configure_item(item, callback=_selection, user_data=items)

            else:
                val += ',?)'
                for column in range((len(table_dict[printed_tag])) - 1):
                    dpg.add_text(table_dict[printed_tag][column + 1])
                    dpg.add_input_text(tag=rows_tags[printed_tag][column])
        else:
            val += ',?,?)'
            for column in range((len(table_dict[printed_tag])) - 1):
                dpg.add_text(table_dict[printed_tag][column + 1])
                if table_dict[printed_tag][column + 1] == 'Предметы':
                    with dpg.group(horizontal=True):
                        dpg.add_text("Выберите количество предметов: ")
                        widget = dpg.add_text("0")
                        dpg.add_button(arrow=True, direction=dpg.mvDir_Left, user_data=widget,
                                       callback=lambda s, a, u: dpg.set_value(u, int(dpg.get_value(u)) - 1))
                        dpg.add_button(arrow=True, direction=dpg.mvDir_Right, user_data=widget,
                                       callback=lambda s, a, u: dpg.set_value(u, int(dpg.get_value(u)) + 1))
                    dpg.add_button(label='Добавить предметы', tag="add_subject",
                                   callback=lambda f: add_subject(dpg.get_value(widget)))
                else:
                    dpg.add_input_text(tag=rows_tags[printed_tag][column])

        if printed_tag == 'teachers_table':
            dpg.delete_item('add_val_subj')
            dpg.add_button(label="Добавить", tag='add_val_subj',
                           callback=lambda: query_insert(val, printed_tag, dpg.get_value(widget)))
        elif printed_tag == 'lessons_table':
            dpg.delete_item('add_val_les')
            dpg.add_button(label="Добавить", tag='add_val_les',
                           callback=lambda: query_update_lessons(val, printed_tag, dpg.get_value('sm1_sm2')))
        else:
            dpg.delete_item('add_avl_all')
            dpg.add_button(label="Добавить", tag='add_avl_all', callback=lambda: query_insert(val, printed_tag, 1))


def wind_edit(sender, app_data, user_data):
    with dpg.window(label="Редактирование записи", width=400, height=300, pos=(500, 200)):
        for i in range(len(rows_tags[printed_tag])):
            dpg.delete_item(rows_tags[printed_tag][i])

        cursor.execute('select * from [' + table_dict[printed_tag][0] + '] where [' +
                       table_dict[printed_tag][1] + '] = ' + str(sender))

        data = cursor.fetchall()
        for i in range(len(data)):
            for j in range(len(data[i])):
                if isinstance(data[i][j], str):
                    data[i][j] = data[i][j].replace('\n', ' ')

        if printed_tag != 'teachers_table':
            for column in range((len(table_dict[printed_tag])) - 1):
                dpg.add_text(table_dict[printed_tag][column + 1])
                dpg.add_input_text(tag=rows_tags[printed_tag][column], default_value=data[0][column])
        else:
            for column in range((len(table_dict[printed_tag])) - 1):
                dpg.add_text(table_dict[printed_tag][column + 1])
                if table_dict[printed_tag][column + 1] == 'Предметы':
                    st = data[0][column]
                    st = list_subject(st)
                    for i in range(len(st)):
                        dpg.delete_item(combo_tags[i])
                        dpg.add_combo(combo_subj, tag=combo_tags[i], default_value=st[i], callback=_log)
                else:
                    dpg.add_input_text(tag=rows_tags[printed_tag][column], default_value=data[0][column])
        with dpg.group(horizontal=True):
            if printed_tag != 'teachers_table':
                dpg.add_button(label="Сохранить изменения", callback=lambda: query_update(printed_tag, 1, sender))
            else:
                dpg.delete_item('save_val_subj')
                dpg.add_button(label="Сохранить изменения", tag='save_val_subj',
                               callback=lambda: query_update(printed_tag, len(st), sender))

            dpg.add_button(label='Удалить запись', callback=lambda f: query_delete(printed_tag, sender))


def select_table(sender, app_data, user_data):
    dpg.delete_item("staged_container")
    dpg.push_container_stack(dpg.add_stage(tag="staged_container"))

    for tl in tag_list:
        dpg.delete_item(tl[0])
    tag_list.clear()

    with dpg.table(header_row=True, scrollX=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True, delay_search=True, policy=dpg.mvTable_SizingFixedFit, no_host_extendX=True):

        for column in range((len(table_dict[sender])) - 1):
            dpg.add_table_column(label=table_dict[sender][column + 1])
        dpg.add_table_column()

        cursor.execute('select * from [' + table_dict[sender][0] + ']')
        global printed_tag
        printed_tag = sender

        for i in cursor.fetchall():
            with dpg.table_row():
                for j in range((len(table_dict[sender]))):
                    if j == (len(table_dict[sender]) - 1):
                        if printed_tag == 'lessons_table':
                            pass
                        else:
                            dpg.add_button(label='Редактировать', tag=i[0])
                            dpg.configure_item(i[0], user_data=dpg.last_item(), callback=wind_edit)
                            tag_list.append(str(i[0]))
                    else:
                        dpg.add_text(i[j])

    dpg.pop_container_stack()
    dpg.set_item_children(user_data, 'staged_container', 1)


def wind_input_data():
    with dpg.window(label='Вводные данные', width=1000, height=340, pos=(150, 150), delay_search=False):

        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                for btn in range(len(table_dict) - 7):
                    dpg.delete_item(tables_tags[btn])
                    dpg.add_button(label=table_dict[tables_tags[btn]][0], tag=tables_tags[btn])

            dpg.add_child_window(width=800, height=300)

            dpg.configure_item(tables_tags[0], user_data=dpg.last_item(), callback=select_table)
            dpg.configure_item(tables_tags[1], user_data=dpg.last_item(), callback=select_table)
            dpg.configure_item(tables_tags[2], user_data=dpg.last_item(), callback=select_table)
            dpg.configure_item(tables_tags[3], user_data=dpg.last_item(), callback=select_table)
            dpg.configure_item(tables_tags[4], user_data=dpg.last_item(), callback=select_table)

            with dpg.group(horizontal=False):
                dpg.add_button(label="Добавить", callback=wind_adding)
                dpg.add_button(label='Условия', callback=wind_limitation)

        dpg.bind_font("Default font")


def get_class_id(value, class_lst):
    class_id = 0
    for c in range(len(class_lst)):
        if value == class_lst[c][1]:
            class_id = class_lst[c][0]
    return class_id


def check_row(sp_list, clas, subj, input_value):
    tag = 'sp_table'
    for i in range(len(sp_list)):
        if input_value is None or input_value == '':
            if sp_list[i][0] == int(clas) and sp_list[i][1] == int(subj):
                return f'delete from [{table_dict[tag][0]}] where [{table_dict[tag][1]}] = {int(clas)} and' \
                       f' [{table_dict[tag][2]}] = {int(subj)}'
        else:
            if sp_list[i][0] == int(clas) and sp_list[i][1] == int(subj) and sp_list[i][2] == int(input_value):
                pass
            elif sp_list[i][0] == int(clas) and sp_list[i][1] == int(subj) and sp_list[i][2] != int(input_value):
                return f'update [{table_dict[tag][0]}] set [{table_dict[tag][3]}] = {int(input_value)} where' \
                       f' [{table_dict[tag][1]}] = {int(clas)} and [{table_dict[tag][2]}] = {int(subj)}'
            elif sp_list[i][0] != int(clas) and sp_list[i][1] != int(subj) and sp_list[i][2] != int(input_value):
                return f'insert into [{table_dict[tag][0]}] values (?,?,?)'


def save_subjplan(tag_list):
    cursor.execute('select * from [' + table_dict['sp_table'][0] + ']')
    sp = cursor.fetchall()
    sp_list = []
    if len(sp) == 0:
        pass
    else:
        for i in sp:
            sp_list.append(list([i[0], i[1], i[2]]))

    query_ins = 'insert into [' + table_dict['sp_table'][0] + '] values (?,?,?)'

    for i in range(len(tag_list)):
        if dpg.get_value(tag_list[i]) is None or dpg.get_value(tag_list[i]) == "":
            stroke = check_row(sp_list, tag_list[i][tag_list[i].index('_') + 1:],
                               tag_list[i][:tag_list[i].index('_')], dpg.get_value(tag_list[i]))
            if stroke is not None:
                cursor.execute(stroke)
                cursor.commit()
                wind_success()
        else:
            if len(sp) == 0:
                cursor.execute(query_ins, list([int(tag_list[i][tag_list[i].index('_') + 1:]),
                                                int(tag_list[i][:tag_list[i].index('_')]),
                                                int(dpg.get_value(tag_list[i]))]))
                cursor.commit()
                wind_success()
            else:
                stroke = check_row(sp_list, tag_list[i][tag_list[i].index('_') + 1:],
                                   tag_list[i][:tag_list[i].index('_')], dpg.get_value(tag_list[i]))
                if stroke is not None:
                    if 'insert' in stroke:
                        cursor.execute(stroke, list([int(tag_list[i][tag_list[i].index('_') + 1:]),
                                                     int(tag_list[i][:tag_list[i].index('_')]),
                                                     int(dpg.get_value(tag_list[i]))]))
                    else:
                        cursor.execute(stroke)
                cursor.commit()
                wind_success()


def select_to_list(printed_tag):
    lst = []
    cursor.execute(
        f'select {table_dict[printed_tag][0]}.[{table_dict[printed_tag][1]}],{table_dict[printed_tag][0]}.[{table_dict[printed_tag][2]}] from [{table_dict[printed_tag][0]}]')
    for row in cursor.fetchall():
        lst.append(list([row[0], row[1]]))
    return lst


def wind_study_plans():
    with dpg.window(label='Учебные планы', width=1500, height=800, pos=(30, 30), delay_search=False):
        cl_lst = select_to_list('classes_table')
        sub_lst = select_to_list('subject_table')
        tag_list = []
        tag_list.clear()

        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(width=150)
            for cl in cl_lst:
                dpg.add_table_column(label=cl[1])
            for subj in sub_lst:
                with dpg.table_row():
                    for c in range(len(cl_lst) + 1):
                        if c == 0:
                            dpg.add_text(subj[1], wrap=100)
                        else:
                            tg = str(subj[0]) + '_' + str(cl_lst[c - 1][0])
                            tag_list.append(tg)
                            value, input_value = check_condition('sp_table', subj[0], cl_lst[c - 1][0], None)
                            if value is True:
                                dpg.delete_item(tg)
                                dpg.add_input_text(default_value=input_value, tag=tg)
                            else:
                                dpg.delete_item(tg)
                                dpg.add_input_text(tag=tg)
        dpg.add_button(label='Сохранить', callback=lambda: save_subjplan(tag_list))


def find_subject_id(subject, st_list):
    subj_list = []
    subject = subject.split('\n')
    for i in subject:
        for j in st_list:
            if i == j[1]:
                subj_list.append(j[0])
    return subj_list


def create_second_smen(classes):
    cursor.execute(f'delete from [{table_dict["classes_table"][0]}]')
    for cl in classes:
        if dpg.get_value(cl) is True:
            cursor.execute(f'select [{table_dict["classes_table"][1]}] from [{table_dict["classes_table"][0]}] where [{table_dict["classes_table"][2]}] = \'{cl}\'')
            class_id = cursor.fetchall()[0][0]
            cursor.execute(f'insert into [{table_dict["smena_2"][0]}] value (?)', class_id)
            cursor.commit()
    create_bloks_hs()


def wind_create():
    with dpg.window(label='Создание расписания', width=500, height=300, pos=(300, 100)):
        smena = False
        columns = 3
        classes = []
        cursor.execute(f'select [{table_dict["lessons_table"][2]}] from [{table_dict["lessons_table"][0]}]')
        for lesson in cursor.fetchall():
            if '2 смена' in lesson[0]:
                smena = True
        dpg.add_text('Составить расписание для')

        def _selection(sender, app_data, user_data):
            dpg.delete_item('what_classes_in_2_sm')
            if len(classes) == 0:
                pass
            else:
                for cl in classes:
                    dpg.delete_item(cl)
            classes.clear()
            for item in user_data:
                if item != sender:
                    dpg.set_value(item, False)
            if sender == user_data[0]:
                cursor.execute(f'select [{table_dict["classes_table"][2]}] from [{table_dict["classes_table"][0]}]')
                for clas in cursor.fetchall():
                    if clas[0] in ['1 класс', '2 класс', '3 класс', '4 класс']:
                        classes.append(clas[0])
                dpg.add_text('Какие классы учатся во 2-ую смену?', tag='what_classes_in_2_sm', before='create')
                for cl in classes:
                    dpg.add_checkbox(label=cl, tag=cl, before='create')
            else:
                cursor.execute(f'select [{table_dict["classes_table"][2]}] from [{table_dict["classes_table"][0]}]')
                for clas in cursor.fetchall():
                    if clas[0] not in ['1 класс', '2 класс', '3 класс', '4 класс']:
                        classes.append(clas[0])
                dpg.add_text('Какие классы учатся во 2-ую смену?', tag='what_classes_in_2_sm', before='create')
                for cl in classes:
                    dpg.add_checkbox(label=cl, tag=cl, before='create')

        items = (
            dpg.add_selectable(label="1 - 4 классов"),
            dpg.add_selectable(label="5 - 11 классов"),
        )

        for item in items:
            dpg.configure_item(item, callback=_selection, user_data=items)

        dpg.add_button(label='Создать', tag='create', callback=lambda: create_second_smen(classes))




def create_bloks_hs():
    tag = 'bloks_hs'
    cursor.execute(f'delete from [{table_dict[tag][0]}]')
    tt = cursor_select('teachers_table')
    st = cursor_select('subject_table')
    ttcl = cursor_select('thachers_to_classes')
    intensive = cursor_select('sp_table')
    tt_list, st_list, ttcl_list, inten_list = [], [], [], []
    for i in st:
        st_list.append(list([i[0], i[1]]))
    for i in tt:
        subject = find_subject_id(i[3], st_list)
        for j in subject:
            if j != '':
                tt_list.append(list([i[0], j]))
    for i in ttcl:
        ttcl_list.append(list([i[0], i[1], i[2]]))
    for i in intensive:
        inten_list.append(list([i[0], i[1], i[2]]))
    k = 1

    for inten in inten_list:
        for ttcl in ttcl_list:
            if ttcl[2] == inten[0] and ttcl[1] == inten[1]:
                if ttcl[1] in ["Иностранный язык", "Информатика", "Допризывная и медицинская подготовка",
                                         "Трудовое обучение", "Допризывная подготовка", "Медицинская подготовка"]:
                    type = 1
                else:
                    type = 0
                cursor.execute(f'insert into [{table_dict[tag][0]}] values (?,?,?,?,?,?)', [k, ttcl[0], inten[1], inten[0], type, inten[2]])
                cursor.commit()
                k += 1


def wind_success():
    with dpg.window(label='', width=300, height=150, pos=(300, 300)):
        dpg.add_text('Сохранено!', pos=(120, 60))


def print_schedule_all():
    print("hahaha")


def print_schedule_teachers():
    print('hahaha')

with dpg.window(label="School Helper", width=1200, height=600, tag="primary window"):
    demo_layout_child = dpg.generate_uuid()

    with dpg.table(header_row=False, row_background=False,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=False,
                   delay_search=True):

        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():
            for i in range(4):
                if i == 0:
                    btn_save = dpg.add_button(label="Сохранить")
                elif i == 1:
                    with dpg.group(horizontal=True):
                        btn_subjects = dpg.add_button(label="Вводные данные", callback=wind_input_data)
                elif i == 2:
                    with dpg.group(horizontal=True):
                        btn_create_tt = dpg.add_button(label="Создать", callback=wind_create)
                        btn_check = dpg.add_button(label="Проверить")
                elif i == 3:
                    with dpg.group(horizontal=True):
                        btn_plans = dpg.add_button(label="Учебные планы", callback=wind_study_plans)

    with dpg.tab_bar():
        pass
        # with dpg.tab(label="Общее"):
        #     cursor.execute(f'select * from [{schedule_itog["schedule"]}]')
        #     if cursor.fetchall() == 0:
        #         pass
        #     else:
        #         print_schedule_all()
        #
        # with dpg.tab(label="Учителя"):
        #     cursor.execute(f'select * from [{schedule_itog["schedule"]}]')
        #     if cursor.fetchall() == 0:
        #         pass
        #     else:
        #         print_schedule_teachers()

    dpg.bind_font("Default font")

dpg.create_viewport(title='School Helper', width=1200, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary window", True)
dpg.start_dearpygui()