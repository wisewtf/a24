import requests
import re
import os
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import date
import json

DIR = os.getcwd()
R = re.compile(r'<[^>]+>') 
URL = 'https://a24films.com/films/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}
YEAR = date.today().year
API = 'FILL_THIS_WITH_OMDB_API'
WEBHOOK = DiscordWebhook(url='FILL_THIS_WITH_DISCORD_WEBHOOK_URL', rate_limit_retry=True)

films_page = requests.get(URL, headers=HEADERS)
parser = BeautifulSoup(films_page.content, "html.parser")
found_items = parser.find_all("h3")

movies = []
for item in found_items:
    stripped_movie = re.sub(R, '', str(item))
    movies.append(stripped_movie)

movie_list = []
with open(f'{DIR}/old_movies.json', 'r') as fp:
    for line in fp:
        x = line[:-1]
        movie_list.append(x)

new_movie = []
for movie in movies:
    if movie not in movie_list:
        title = str(movie)
        API_URL = f'http://www.omdbapi.com/?apikey={API}&t={title}&y={YEAR}'
        omdb_data = requests.get(API_URL)
        new_movie.append(omdb_data.text)

with open(f'{DIR}/old_movies.json', 'w') as fp:
    for title in movies:
        fp.write("%s\n" % title)

for film in new_movie:
    y = json.loads(film)
    response = y["Response"]
    if response == "True":
        title = y["Title"]
        plot = y["Plot"]
        poster = y["Poster"]
        rating = y["Rated"]
        release = y["Released"]
        runtime = y["Runtime"]
        director = y["Director"]
        writer = y["Writer"]
        genre = y["Genre"]
        embed = DiscordEmbed(title=f'{title}', description=f'{plot}', color='ffffff')
        embed.set_author(name='NEW A24 UPCOMING MOVIE', url='https://a24films.com/films', icon_url='https://i.imgur.com/Il4vJct.png')
        embed.set_image(url=f'{poster}')
        embed.set_thumbnail(url='https://i.imgur.com/Il4vJct.png')
        embed.set_footer(text='A24 Upcoming Movies bot coded by WISE (POG)')
        embed.set_timestamp()
        embed.add_embed_field(name='Director', value=f'{director}')
        embed.add_embed_field(name='Writer', value=f'{writer}')
        embed.add_embed_field(name='Genre', value=f'{genre}')
        embed.add_embed_field(name='Rating', value=f'{rating}')
        embed.add_embed_field(name='Runtime', value=f'{runtime}')
        embed.add_embed_field(name='Release Date', value=f'{release}')
        WEBHOOK.add_embed(embed)
        response = WEBHOOK.execute(remove_embeds=True)
    else:
        pass