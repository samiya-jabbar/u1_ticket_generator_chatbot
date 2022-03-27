import pandas as pd
data= pd.read_csv("Salary_Data.csv")
print(data.columns)
a = list(data.Salary)
print(a)

if '1234' in a :
    print("ok")
else :
    print("not ok")
