import pandas as pd
import pymysql
# import matplotlib.pyplot as plt
import pdb;pdb.set_trace()

steelers = "select * from defense where home ='Steelers';"
runningbacks = """ SELECT 
	rb.week,
	CONCAT_WS(' ', rb.fname, rb.lname) runningbacks,
	rb.receiving_targt,
	rb.receiving_recpt,
	rb.ftps,
	CONCAT_WS(' ', t.city, t.mascot) team
FROM
    runningbacks rb
        INNER JOIN
    nfl_teams t ON rb.team_id = t.team_id; """

quarterbacks = """ SELECT 
	qb.week,
	CONCAT_WS(' ', qb.fname, qb.lname) quarterbacks,
	qb.passing_att,
	qb.passing_cmp,
	qb.passing_yd,
	qb.passing_td,
	qb.passing_int,
	qb.ftps,
	CONCAT_WS(' ', t.city, t.mascot) team
FROM
    quarterbacks qb
        INNER JOIN
    nfl_teams t ON qb.team_id = t.team_id; """
    
ben = """ select concat_ws(" ",fname,lname) as full_name,week,passing_att,passing_cmp,passing_yd,passing_td,passing_int,passing_rate,ftps from quarterbacks where fname = 'Ben'; """
    
con = pymysql.connect(
							 host='localhost',
                             user='root',
                             password='',
                             db='testdb',
                             charset='utf8mb4',
        					 cursorclass=pymysql.cursors.DictCursor
        					 )

cur = con.cursor()

cur.execute(ben)
cur.fetchall()
df = pd.read_sql(ben,con = con)
print(df.head())
print(df.describe())
print(df.corr())
print(df.rank())

# df['FPTS'].hist(bins=40)
# df.boxplot(column='FPTS', by = 'opponent') 
# x = df['FPTS']
# y = df['week']
# plt.scatter(x, y, label= "stars", color= "m",  
#             marker= "*", s=30) 
# df.plot.pie
# plt.show() 
print("hello")
