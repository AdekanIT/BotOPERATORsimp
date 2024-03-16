import sqlite3


data = sqlite3.connect('info.db', check_same_thread=False)
sql = data.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS operators '
            '(op_id INTEGER PRIMARY KEY AUTOINCREMENT, op_name TEXT, telNo TEXT, check_id INTEGER);')

sql.execute('CREATE TABLE IF NOT EXISTS geo '
            '(g_id INTEGER PRIMARY KEY AUTOINCREMENT, g_name TEXT, cr1 TEXT, cr2 TEXT, loc_name TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, photo TEXT, price INTEGER);')


def checker_pr(id):
    if sql.execute('SELECT * FROM products WHERE pr_id=?;', (id, )).fetchone():
        return True
    else:
        return False


def get_pr_by_id(id):
    return sql.execute('SELECT name, photo, price FROM products WHERE pr_id=?;', (id, )).fetchall()


def get_all_pr():
    product = sql.execute('SELECT pr_id, name FROM products;').fetchall()
    all_product = [i[0] for i in product]
    return str(all_product)


def get_all_pr_info():
    product = sql.execute('SELECT * FROM products;').fetchall()
    return product


def get_all_loc():
    cursor = sql.execute('SELECT g_id, g_name FROM geo;').fetchall()
    all_loc = [i[1] for i in cursor]
    return all_loc


def add_pr(name, category, photo, price):
    sql.execute('INSERT INTO products(name, category, photo, price)'
                'VALUES(?, ?, ?, ?);', (name, category, photo, price))
    data.commit()


def dell_pr(id):
    sql.execute('DELETE FROM products WHERE pr_id=?;', (id, ))
    data.commit()


def get_pr_but(category):
    pr = sql.execute('SELECT pr_id, name FROM products WHERE category=?;', (category, )).fetchall()
    return pr


def get_products_bt(category, offset, limit=6):
    products = sql.execute('SELECT * FROM products WHERE category=? LIMIT ? OFFSET ?;',
                           (category, limit, offset)).fetchall()
    return products


def get_loc(id):
    return sql.execute('SELECT g_id, g_name, cr1, cr2, loc_name FROM geo WHERE g_name=?;', (id, )).fetchone()


def add_loc(name, cr1, cr2, location):
    sql.execute('INSERT INTO geo(g_name, cr1, cr2, loc_name) VALUES(?, ?, ?, ?);', (name, cr1, cr2, location))
    data.commit()


def delete_loc(id):
    sql.execute('DELETE FROM geo WHERE g_id=?;', (id, ))
    data.commit()


def loc_but():
    return sql.execute('SELECT g_id, g_name, cr1, cr2, loc_name FROM geo;').fetchall()


def get_all_op():
    return sql.execute('SELECT op_id, op_name, telNo, check_id FROM operators;').fetchall()


def loc_null_checker():
    result = sql.execute('SELECT COUNT(*) FROM geo;').fetchall()
    if result[0][0] > 1:
        return True
    elif result[0][0] <= 1:
        return False


def add_op(id, name, phone):
    sql.execute('INSERT INTO operators(check_id, op_name, telNo) VALUES(?, ?, ?);', (id, name, phone))
    data.commit()


def delete_op(id):
    sql.execute('DELETE FROM operators WHERE op_id=?;', (id, ))
    data.commit()


def check_op(id):
    if sql.execute('SELECT * FROM operators WHERE op_id=?;', (id, )).fetchone():
        return True
    else:
        return False


def check_op_t(id):
    if sql.execute('SELECT * FROM operators WHERE check_id=?;', (id, )).fetchone():
        return True
    else:
        return False


