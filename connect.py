import psycopg2
from sql import create__queries,drop__queries
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "µµµµµµµµ"

def DropTable(cur,conn):
    for query in drop__queries:
        cur.execute(query)
        conn.commit()
        
        
def SetUp_DataBase():
    conn = psycopg2.connect(host = host, 
                            dbname = dbname, 
                            user = user, 
                            password = password)  # return a intance of the connection class
    conn.set_session(autocommit=True)               # that command will every time clone the conneection when we finish a query
    cur = conn.cursor()
    conn.close() 

    conn = psycopg2.connect(host =host, 
                            dbname = dbname, 
                            user = user, 
                            password = password)
    cur = conn.cursor()                                       # give a cursor in order to execute any SQL statements
    return cur , conn


def create_tables(cur, conn):
    for query in create__queries:
        cur.execute(query)
        conn.commit()

#def main():
    #cur, conn = SetUp_DataBase()
    #DropTable(cur,conn)
    #create_tables(cur, conn)
    #print("created successfully, happy hacking")
    #conn.close()


#if __name__ == "__main__":
    #main()                           
