import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# sqlite3 practice
def create_database():
    conn = sqlite3.connect('house_price.db')
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS house_price")

    df = pd.read_csv('1st_train_mdf.csv')
    index_str = []
    for i in df.columns:
        if df[i].dtype == 'object':
            tmp_str = f"{i} TEXT"
        if df[i].dtype in ["int64","float64"]:
            tmp_str = f"{i} REAL"
        if i[0].isdigit():
            # string cannot start with number
            tmp_str = "_"+tmp_str
        index_str.append(tmp_str)
    cur.execute(f"CREATE TABLE house_price({', '.join(index_str)})")

    for _, row in df.iterrows():
        row_str = []
        for i in row:
            if pd.isna(i):
                row_str.append('NA') # not missed data but absence of the quality
            elif type(i) == str:
                row_str.append(f"'{i}'")
            else:
                row_str.append(str(i))
        cur.execute(f"INSERT INTO house_price VALUES ({','.join(row_str)})")
    conn.commit()
    conn.close()


def basic_statistics_sqlite():
    conn = sqlite3.connect('house_price.db')
    cur = conn.cursor()
    
    # print the table info
    print("Table info:")
    cur.execute("PRAGMA table_info(house_price);")
    i = 0
    for row in cur:
        i += 1
        if i < 6:
            print(f"    {row[1]}: {row[2]}")
    print('    ...')

    print(f"Number of columns: {i}") 
    cur.execute("SELECT COUNT(Id) FROM house_price;")
    print(f"Number of rows: {cur.fetchone()[0]}")
        


if __name__ == "__main__":
    # create_database()
    basic_statistics_sqlite()



    exit()


    # extract basic statistics
    conn = sqlite3.connect('house_price.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM house_price")
    rows = cur.fetchall()
    print("Number of rows: ", len(rows))
    print("Number of columns: ", len(rows[0]))
    print("Column names: ", df.columns)
    conn.close()

