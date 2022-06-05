import os

import requests
from bs4 import BeautifulSoup
import string

def page_content(url):
    response = requests.get(url)
    if response:
        r = response.content
        soup = BeautifulSoup(r, 'html.parser')
        return soup
    else:
        return False

def article_search(pages, article_type_user):
    working_directory = os.getcwd()
    for page_current in range(1, pages + 1):
        os.chdir(working_directory)
        os.mkdir(f'Page_{page_current}')
        os.chdir(f'Page_{page_current}')
        user_url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_current}'
        saved_articles = []
        nature_page = page_content(user_url)
        if nature_page:
            articles = nature_page.findAll('li', {'class': 'app-article-list-row__item'})
            for article in articles:
                article_type = article.find('span', {'data-test': 'article.type'}).text.strip('\n')
                if article_type == article_type_user:
                    article_link = article.find('a', {'class': 'c-card__link u-link-inherit'})
                    article_link_ref = article_link.get('href')
                    article_link = article_link.text
                    article_link_nopunct = article_link.translate(str.maketrans('', '', string.punctuation))
                    article_title = article_link_nopunct.replace(' ', '_')
                    saved_articles.append(article_title)
                    link_url = 'https://www.nature.com' + article_link_ref
                    article_page = (page_content(link_url))
                    article_body = article_page.find('div', {'class': 'c-article-body'}).text.strip()
                    file_name = article_title + '.txt'
                    with open(file_name, mode='w', encoding='utf-8') as file:
                        file.write(article_body)
        else:
            print('Invalid URL!')
    print(article_type_user)
    print('Saved all articles.')

pages = int(input())
article_type_new = string.capwords(input())
article_search(pages, article_type_new)
