# A24

A simple Discord webhook bot that will warn when new A24 movies are added to their Upcoming Movies website page.

All it does is scrape their [Films](https://a24films.com/films) page. Parse the `h3` HTML tag that contains movie titles and write them into a file in the `working directory` of your choosing.

Then every time this runs it will parse the written file and find items that are not in it when A24 updates their website.

After that it will reach out to the OMDB API and try to find info on the new items and the script will compose a Discord Embed with all the info and sends it using a webhook URL in a channel you chose.

Currently it doesn't really 'handle' movies that aren't in the API. It passes so not to break the for loop. But I'm considering expanding it or at least warn of the change in the channel, so people can go look for themselves if they are interested.

You must install `requests`, `BeautifulSoup`, `DiscordWebhook` and `DiscordEmbed` to use this script.

And then you can use cron or systemd to run it on a timer.

In a future update I will modify the script to read the OS ENV table so that I can define API KEYS and Webhook URL inside a systemd service unit as service variables and then complete it with a timer unit.

Criticism appreciated, this is my first fully working Python code.
