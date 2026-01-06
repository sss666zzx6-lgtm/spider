import requests
from bs4 import BeautifulSoup



urls = [f'https://travel.qunar.com/place/api/html/comments/dist/300195?sortField=1&img=false&pageSize=10&page={i}' for i in range(1,201)]

for url in urls:
    res = requests.get(url)
    print(res.text)
    # soup = BeautifulSoup(res.text,'lxml')
    # li_tags = soup.find('ul', class_='b_strategy_list').find_all('li', class_='list_item')
    # for li in li_tags:
    #     print(li.get_text().strip())
    #     detail_url = f"https://travel.qunar.com/travelbook/note/{li.find('h2', class_='tit').find('a').get('href').split('/')[-1]}"
    #
    #     print(detail_url)
    # break