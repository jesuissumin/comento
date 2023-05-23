import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA

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
    plt.figure(figsize=(8, 6))
    sns.histplot(df['SalePrice'])
    skew = df['SalePrice'].skew()
    kur = df['SalePrice'].kurtosis()
    plt.text(0.7, 0.4, f"skew: {skew:.2f}\nkurtosis: {kur:.2f}", 
             fontsize=16, 
              transform=plt.gca().transAxes)
    plt.title('SalePrice histgoram')
    plt.savefig('figs/pd_price.png', bbox_inches='tight', dpi=200)
    plt.clf()
    
    # check categorical variables
    categorical = []
    for i in df.columns:
        if df[i].dtype == 'object':
            categorical.append(i)
        elif len(df[i].unique()) <= 20:
            categorical.append(i)
    print(f"Categorical variables({len(categorical)}):")
    for i in categorical[:5]:
        print(f"    {i}: {len(df[i].unique())}")
    print("  ...")

    # clustering for categorical variables
    for i in [
        "TotRmsAbvGrd",
        "OverallQual",
        "Neighborhood",
        "KitchenQual",
        "HouseStyle",
        "GarageCars",
        "Fireplaces",
        "FullBath",
        ]:
        plt.figure(figsize=(10, 8))
        plt.title(i)
        sns.scatterplot(data=df, x='GrLivArea', y='SalePrice', hue=i)
        plt.savefig(f'figs/pd_scatter_{i}.png', bbox_inches='tight', dpi=200)
        plt.clf()

    # correlation for continue variables
    continue_df = df.drop(columns=categorical)
    corr = continue_df.corr()
    corr_high = corr.index[abs(corr['SalePrice']) > 0.5]
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[corr_high].corr(), annot=True)
    plt.savefig('figs/pd_corr.png', bbox_inches='tight', dpi=200)
    plt.clf()


def anal_fig():
    df = pd.read_csv("1st_train_mdf.csv")

    # print variance of variables
    print("Variance of variables:")
    var_s = {}
    for i in df.columns:
        if df[i].dtype == 'object':
            continue
        var_s[i] = df[i].var()
    var_s = pd.Series(var_s)
    var_s = var_s.sort_values(ascending=False)
    for i in var_s.index[:5]:
        print(f"    {i}: {var_s[i]:.2f}")
    print("  ...")
    sns.scatterplot(data=df,x="GrLivArea", y="LotArea", hue="SalePrice")
    plt.savefig('figs/anal0.png', bbox_inches='tight', dpi=200)

    # saleprice by year sold
    plt.figure(figsize=(8, 6))

    ax1 = sns.histplot(data=df, x='YrSold')
    ax1.set_xticks(np.sort(df['YrSold'].unique()))

    avg_sales = []
    for i in np.sort(df['YrSold'].unique()):
        avg_sales.append(df[df['YrSold']==i]['SalePrice'].mean())
    ax2 = ax1.twinx()
    ax2.plot(np.sort(df['YrSold'].unique()), avg_sales, color='red')
    ax2.set_ylim(150000, 200000)
    ax2.set_ylabel('Average SalePrice')

    plt.title("SalePrice by YrSold")
    plt.savefig('figs/anal1.png', bbox_inches='tight', dpi=200)
    plt.clf()

    # scatter plot x = GrLivArea, y = SalePrice, color = OverallQual
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='GrLivArea', y='SalePrice', hue='OverallQual')
    # draw fitted line
    x = df['GrLivArea'][df['GrLivArea']<3000] # remove outliers
    y = df['SalePrice'][df['GrLivArea']<3000]
    fp1 = np.polyfit(x, y, 2)
    f1 = np.poly1d(fp1)
    x = np.sort(df['GrLivArea'])
    plt.plot(x, f1(x), color='red')
    plt.title("SalePrice by GrLivArea")
    plt.savefig('figs/anal2.png', bbox_inches='tight', dpi=200)

    # barplot x = sold year - built year or remodeled year, y = average price
    df['YrSold'] = df['YrSold'].astype(int)
    df['Age_at_sale'] = np.floor((df['YrSold'] - df[['YearBuilt','YearRemodAdd']].max(axis=1))/5)*5
    df['Age_at_sale'][df['Age_at_sale']<0] = 0
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='Age_at_sale', y='SalePrice')
    plt.title("SalePrice by Age at Sale")
    plt.savefig('figs/anal3.png', bbox_inches='tight', dpi=200)
    plt.clf()

    # OverallQual per neighborhood
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='Neighborhood', y='SalePrice')
    plt.xticks(rotation=90)
    plt.title("SalePrice by Neighborhood")
    plt.savefig('figs/anal4.png', bbox_inches='tight', dpi=200)
    plt.clf()

    # PCA for continue variables
    categorical = []
    for i in df.columns:
        if df[i].dtype == 'object':
            categorical.append(i)
        elif len(df[i].unique()) <= 20:
            categorical.append(i)
    continue_df = df.drop(columns=categorical+['SalePrice'])
    continue_df = continue_df[continue_df['LotArea']<100000] # remove outliers
    continue_df = continue_df.dropna() # remove rows with nan
    pca = PCA(n_components=2)
    pca.fit(continue_df)
    pca_df = pd.DataFrame(pca.transform(continue_df), columns=['PC1', 'PC2'])
    pca_df['SalePrice'] = df['SalePrice']
    var_ratio = pca.explained_variance_ratio_
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='SalePrice')
    plt.title("PCA")
    plt.text(0, 4000, f"Explained variance ratio: {var_ratio[0]:.2f}, {var_ratio[1]:.2f}",
             fontsize=16)
    plt.savefig('figs/anal5.png', bbox_inches='tight', dpi=200)
    plt.clf()

    # top 10 important features
    # transform categorical variables to dummy variables
    df = df.fillna('0')
    dummy_df = pd.get_dummies(df, columns=categorical)
    X = dummy_df.drop(columns=['SalePrice'])
    y = df['SalePrice']
    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    indices = indices[:10]
    mse = mean_squared_error(y, model.predict(X))
    plt.figure(figsize=(8, 6))
    plt.title("Feature importances")
    plt.bar(range(10), importances[indices], align="center")
    plt.xticks(range(10), X.columns[indices], rotation=90)
    plt.xlim([-1, 10])
    plt.text(2, 0.25, f"MSE: {mse:.2f}", fontsize=16)
    plt.savefig('figs/anal6.png', bbox_inches='tight', dpi=200)
    plt.clf()


if __name__ == "__main__":
    # create_database()
    # basic_statistics_sqlite()
    # anal_using_pandas()
    anal_fig()
