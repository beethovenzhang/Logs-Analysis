# This is an internal reporting tool that answers the following
# three questions about the news database:

# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2

dbname = "news"


def most_popular_articles():
    '''Answers the first question about the most popular articles'''
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""select SUBSTRING(path,10) as article,
    count(*) as views from lightlog
    where status='200 OK' and path != '/'
    group by path
    order by views desc
    limit 3""")
    res = c.fetchall()
    db.close()
    print_results(res, 'views')


def most_popular_authors():
    '''Answers the second question about the most popular articles'''
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""select SUBSTRING(path,10) as article,
    count(*) as views from lightlog
    where status='200 OK' and path != '/'
    group by path
    order by views desc""")
    res = c.fetchall()
    db.close()
    print_results(res, 'views')

#def days_of_more_errors():

def print_results(list, par):
    '''Prints out the query results in a clear format'''
    for row in list:
        print(row[0] + ' -- ' + par + ' ' + str(row[1]))



if __name__ == '__main__':
    most_popular_articles()
