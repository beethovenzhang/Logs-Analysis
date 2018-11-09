#!/usr/bin/env python3

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
    c.execute("""select title, views from articles, popular_articles
    where popular_articles.article=articles.slug
    order by views desc
    limit 3""")
    res = c.fetchall()
    db.close()
    print('The top three most popular articles are:')
    print_results(res, 'views')


def most_popular_authors():
    '''Answers the second question about the most popular ariticle authors'''
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""select name,sum(views) as total_views
    from author_slug, popular_articles
    where author_slug.slug=popular_articles.article
    group by name
    order by total_views desc;""")
    res = c.fetchall()
    db.close()
    print('The most popular article authors are:')
    print_results(res, 'views')


def days_of_more_errors():
    '''Answers the third question about the days with more errors'''
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""select error_count.date,
    CAST(errors as decimal(10))/CAST(normals as decimal(10)) as error_ratio
    from error_count, normal_count
    where error_count.date=normal_count.date
    and CAST(errors as decimal(10))/CAST(normals as decimal(10))>0.01;""")
    res = c.fetchall()
    db.close()
    print('The day with more than one percent errors:')
    for row in res:
        print(str(row[0]) + ' -- errors ' + str("{:.2%}".format(row[1])))


def print_results(list, par):
    '''Prints out the query results in a clear format'''
    for row in list:
        print(str(row[0]) + ' -- ' + par + ' ' + str(row[1]))


if __name__ == '__main__':
    most_popular_articles()
    print()
    most_popular_authors()
    print()
    days_of_more_errors()
