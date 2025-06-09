import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime


@anvil.server.callable
def add_article(article_dict):
  app_tables.articles.add_row(
    created=datetime.now(),
    **article_dict
  )

@anvil.server.callable
def get_articles():
  # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
  return app_tables.articles.search(
    tables.order_by("created", ascending=False)
  )

@anvil.server.callable
def update_article(article, article_dict):
  # check that the article given is really a row in the ‘articles’ table
  if app_tables.articles.has_row(article):
    article_dict['updated'] = datetime.now()
    article.update(**article_dict)
  else:
    raise Exception("Article does not exist")

@anvil.server.callable
def delete_article(article):
  # check that the article being deleted exists in the Data Table
  if app_tables.articles.has_row(article):
    article.delete()
  else:
    raise Exception("Article does not exist")