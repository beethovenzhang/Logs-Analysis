# Logs-Analysis

## Introduction
This is an internal reporting tool to analyze logs from the `news` database. It answers the following three questions through SQL queries:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Usage
In an environment that already contains the `news` database and has Python 3 and its module `pycopg2` installed, run the following command in the command line:
```
python InternalReportingTool.py
```
The results should be printed out in the same window.

## Potential future updates
- Adapted to use with other queries on other databases;
- Output the results in a text file or on a webpage.

## Views
Some views of the `news` database were created to simplify the SQL queries in the code.

1. lightlog: only shows path, status and time columns of the `log` table;
```
create view lightlog as select path, status, time from log;
```

2. popular_articles: shows articles and their views in a descending order;
```
create view popular_articles as select SUBSTRING(path,10) as article,
  count(*) as views from lightlog
  where status='200 OK' and path != '/'
  group by path
  order by views desc;
```

3. author_slug: shows author names and the slugs of their articles;
```
create view author_slug as select name,slug from    authors,articles
  where authors.id=articles.author;
```

4. error_count: shows the number of errors happened on each day;
```
create view error_count as
  select date(time) as date, count(*) as errors from log
  where status like '404%'
  group by date;
```

5. normal_count: shows the number of normal visits on each day;
```
create view normal_count as
  select date(time) as date, count(*) as normals from log
  where status like '200%'
  group by date;
```
