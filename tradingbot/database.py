import sqlite3

def insert(id, start_time, symbol, purchased_quantity, purchase_price):
    con = sqlite3.connect("Data/data.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO Orders 
				(id, start_time, symbol, purchased_quantity, purchase_price,
				 sold_quantity, profit, end_time, result)
				VALUES (%s, %s, "%s","%s","%s",0,0,0,0)"""
                %(id, start_time, symbol, purchased_quantity, purchase_price))
    con.commit()
    con.close()



def update(params, param_values, conditions, cond_values):
    print  params, param_values,conditions,cond_values
    mask = """update Orders set %s where %s"""
    str_param = ""
    str_cond = ""

    for el in params:
        str_param += "{} = %s,".format(el)
    for el in conditions:
        str_cond += "{} %s,".format(el)

    request = mask%(str_param[:-1],str_cond[:-1])%(param_values + cond_values)
    print request
    con = sqlite3.connect('Data/data.db')
    cur = con.cursor()
    cur.execute(request)
    con.commit()
    con.close()

def select(params, conditions, cond_values):
    mask = """select %s from Orders where %s"""
    str_param = ""
    str_cond = ""

    for el in params:
        str_param += " {},".format(el)
    for el in conditions:
        str_cond += " {} %s and".format(el)

    request = mask % (str_param[:-1], str_cond[:-3]) % (cond_values)
    print request
    con = sqlite3.connect('Data/data.db')
    cur = con.cursor()
    cur.execute(request)
    result = cur.fetchall()
    con.commit()
    con.close()

    return result
