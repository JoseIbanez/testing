import pandas as pd
d1 = {
     'Index': ['KNN', 'SVM', 'MLP'],
     'Value': [1, 2, 3]
}
df1 = pd.DataFrame(data=d1).set_index('Index')


d2 = {
     'Index': ['BNN', 'BVM', 'BLP'],
     'Value': [4, 5, 6]
}
df2 = pd.DataFrame(data=d2).set_index('Index')

df3 = pd.concat([df1, df2])


print(df1)
print(df2)
print(df3)