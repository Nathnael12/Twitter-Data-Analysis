from msilib.schema import Class
import mysql.connector as mysql
from mysql.connector import errorcode
import pandas as pd
import os, sys
import pandas as pd
from sqlalchemy import create_engine
sys.path.append(os.path.abspath(os.path.join("../dashboard")))
sys.path.append(os.path.abspath(os.path.join("")))

class DBHandler:
    
    def __init__(self):
        pass
    
    
    def db_connect(self,dbName=None):
        
        try:
            conn = mysql.connect(host='localhost', user='root',
                            password='root', database=dbName, buffered=True)
            cur = conn.cursor()
            return conn, cur
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return None

    def create_db(self,dbName:str)->None:
        conn,cur=self.db_connect()
        cur.execute("CREATE DATABASE IF NOT EXISTS %s ;"%dbName)
        conn.commit()
        cur.close()

    def create_table(self,db_name:str,sql_file_name:str)->None:
        conn,cur=self.db_connect(db_name)

        fd=open("../dashboard/%s"%sql_file_name,'r')
        sql_script=fd.read()
        fd.close()

        
        sql_commands= sql_script.split(';')
        for command in sql_commands:
            try:
                res=cur.execute(command)
            except Exception as ex:
                print("command: %s Skipped \n error %s:"%(command,ex))
        conn.commit()
        cur.close()

    def populate_table(self,df:pd.DataFrame,table_name:str,db_name:str):
        my_conn = create_engine("mysql://root:root@localhost/%s"%db_name) #fill details
        df.to_sql(con=my_conn,name=table_name,if_exists='append')
        # conn,cur=self.db_connect(db_name)
        # df.to_sql(table_name, conn)

# s=open("./dashboard/freq_hash.sql",'r')
# s=open("./dashboard/missing_data.sql",'r')
# s=open("./dashboard/freq_words.sql",'r')
# print(s.read())
# s.close()
# print(sys.path)