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

    # print the max, min, mean of the price
    print("1. print the max, min, mean of the price")
    cur.execute("SELECT MAX(SalePrice), MIN(SalePrice), AVG(SalePrice) FROM house_price;")
    ma, mi, me = cur.fetchone()
    print(f"    max: {ma/1000:.1f}K")
    print(f"    min: {mi/1000:.1f}K")
    print(f"    mean: {me:.2f}")

    # print the histogram of the negiborhood 
    print("2. print the histogram of the negiborhood")
    cur.execute("select Neighborhood, count(Neighborhood) from house_price group by 1 order by 2 desc;")
    rows = cur.fetchall()
    for c, i in enumerate(rows):
        if c == 5:
            break
        print(f"    {i[0]}: {i[1]}")
    x = [row[0] for row in rows]
    y = [row[1] for row in rows]
    plt.figure(figsize=(10, 8))
    plt.bar(x, y)
    plt.xticks(rotation=90)
    plt.savefig('figs/sql_neighborhood.png', bbox_inches='tight', dpi=200)
    plt.clf()

    # print the histogram of the year built
    print("3. print the histogram of the year built")
    cur.execute("select (YrSold-YearBuilt), count(YrSold-YearBuilt) from house_price group by 1 order by 1;")
    rows = cur.fetchall()
    for c, i in enumerate(rows):
        if c == 5:
            break
        print(f"    {i[0]}: {i[1]}")
    x = [row[0] for row in rows]
    y = [row[1] for row in rows]
    plt.bar(x, y)
    plt.xticks(rotation=90)
    plt.savefig('figs/sql_yearbuilt.png', bbox_inches='tight', dpi=200)

def anal_using_pandas():
    df = pd.read_csv('1st_train_mdf.csv')
    # histogram of price
    plt.figure(figsize=(10, 8))
    sns.histplot(df['SalePrice'])
    plt.savefig('figs/pd_price.png', bbox_inches='tight', dpi=200)
    plt.clf()
    
    # print the max, min, mean of the price
    print("The max, min, mean of the price: " + \
        f"max: {df['SalePrice'].max()/1000:.1f}K " + \
        f"min: {df['SalePrice'].min()/1000:.1f}K " + \
        f"mean: {df['SalePrice'].mean()/1000:.2f}")

    # missing values
    print("Missing values:")
    null_df = (df.isna().sum() /len(df))*100
    null_df = null_df.drop(null_df[null_df == 0].index).sort_values(ascending=False)[:20]
    print(null_df.head(20))
    # remove top 6 columns > 17% missing
    

    # correlation


if __name__ == "__main__":
    # create_database()
    # basic_statistics_sqlite()
    anal_using_pandas()
