import csv

file = open('Salary_Data.csv')

type(file)

csvreader = csv.reader(file)