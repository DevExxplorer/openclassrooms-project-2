from csv import DictWriter
from get_book import parse_html, get_book
from re import sub
from requests import get


def get_slug_with_title(title):
    title = title.lower().strip()
    title = sub(r'[^\w\s-]', '', title)
    title = sub(r'[-\s]+', '-', title)
    return title


def download_img(img, title, category):
    name_category = category.split('_')
    f = open('images/' + name_category[0] + '/' + get_slug_with_title(title) + '.jpg', 'wb')
    f.write(get(img).content)
    f.close()


def make_csv(data, category):
    name_category = category.split('_')
    data_key = data[0].keys()
    with open('csv/' + name_category[0] + '.csv', "w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=data_key)
        writer.writeheader()
        writer.writerows(data)


def check_next_page(url):
    next_page = False
    data = parse_html(url)

    if data.find(class_="next"):
        next_page = True

    return next_page


def save_books_category(category, all_category=False):
    data = []
    next_p = True
    page = 1

    while next_p:
        path = 'index' if page == 1 else 'page-' + str(page)
        url = 'https://books.toscrape.com/catalogue/category/books/' + category + '/' + path + '.html'
        categories = parse_html(url)

        for article in categories.find_all('article'):
            link = article.find_all('a')[0]
            href = link.get('href')
            path_name = href.split('../')
            books = get_book('https://books.toscrape.com/catalogue/' + path_name[-1])
            data.append(books)

            if all_category:
                download_img(books['img'], books['title'], category)

        if check_next_page(url):
            page += 1
        else:
            next_p = False

    make_csv(data, category)


