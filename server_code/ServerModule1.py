import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime


@anvil.server.callable
def add_article(article_dict):
  current_user = anvil.users.get_user()
  if current_user is not None:
    app_tables.articles.add_row(
    created=datetime.now(),
    user = current_user,
    **article_dict
  )

def verify_user_permission(article):
  current_user = anvil.users.get_user()
  if current_user is not None:
    if app_tables.articles.has_row(article) and article['user'] == current_user:
      return True

@anvil.server.callable
def get_articles():
  current_user = anvil.users.get_user()
  if current_user is not None:
    return app_tables.articles.search(
    tables.order_by("created", ascending=False), 
    user = current_user
  )

@anvil.server.callable
def update_article(article, article_dict):
  if verify_user_permission(article):
    article_dict['updated'] = datetime.now()
    article.update(**article_dict)
  else:
    raise Exception("Article does not exist or does not belong to this user")

@anvil.server.callable
def delete_article(article):
  if verify_user_permission(article):
    article.delete()
  else:
    raise Exception("Article does not exist")