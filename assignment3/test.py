from assignment3.mypandas import *


df = DataFrame.from_csv('SalesJan2009.csv')
# # =========test task1=========
df1 = df.copy()
df1 = df1.sort_by('Price',reverse=True)

df2 = df.copy()
df2 = df2.sort_by('Price',reverse=False)

df3 = df.copy()
df3 = df3.sort_by('Transaction_date',reverse=False)

df4 = df.copy()
df4 = df4.sort_by('Product',reverse=True)

df5 = df.copy()
df5 = df5.sort_by(['Product', 'Price'], [False, False])

df6 = df.copy()
df6 = df6.sort_by(['City', 'Transaction_date'], [False, True])


# =========test task2==========
df1 = df.copy()
df1 = df1[df1['Payment_Type'] == 'Visa']

df2 = df.copy()
df2 = df2[df2['Price'] > 1400]

df3 = df.copy()
df3 = df3[df3['Transaction_date'] >= datetime.datetime(2009, 1, 30, 18, 9)]

# =========test task3==========
df1 = df.copy()
df1 = df1.group_by('Payment_Type', 'Price', avg)

df2 = df.copy()
df2 = df3.group_by(['Product','Payment_Type'],['Price', 'Latitude'],[avg,avg])
