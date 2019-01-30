import pymysql

def commit_air_quality_data(pm2,pm10,temp,humi,addr,time):
    # connect database
    db = pymysql.connect("localhost","logic","logic","logic")

    # get cursor object

    cursor = db.cursor()

    # insert statement
    sql = """INSERT INTO fresh_air(pm2,pm10,temp,humi,addr,time) \
    values (%s, %s,  %s,  %s, %s, '%s' )"""%(pm2,pm10,temp,humi,addr,time)
    print(sql)
    try:
        # execute sql

        result =cursor.execute(sql)
        # commit sql
        db.commit()
        return result
    except:
        print("something error ")
        db.rollback()
        return False

    # close database connect
    db.close()
