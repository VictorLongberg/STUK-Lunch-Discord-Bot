# STUK Lunch Discord Bot

This is a simple Discord bot that fetches the daily menu from the website [STUK](https://www.stuk.nu/) using the `requests_html` library and posts it to a Discord channel upon command. 

## Features
- Displays the restaurant's menu
- Lists all the commands the bot has
- Shows the url from which the menu was taken

## Installation
1. Clone the repository using `git clone https://github.com/[your_username]/stuk-lunch-discord-bot.git`
2. Navigate to the cloned repository and create a new file called `.env`
3. In the `.env` file, add your Discord bot token like this: `SECRET_KEY_DISCORD=your_token_here`
4. Make sure you have `discord.py` and `requests_html` installed. If not, run `pip install discord.py requests_html` in your command prompt
5. Run the script using `python stuk_lunch_discord_bot.py`

## Usage
Once the bot is running and added to your Discord server, you can use the following commands to interact with it:

- `!menu` - Displays the restaurant's menu
- `!help` - Lists all the commands the bot has
- `!url` - shows the url from which the menu was taken

## Contribution
Feel free to contribute to this project by submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgment
* [STUK](https://www.stuk.nu/) for providing the menu data
* [Matochmat](https://www.matochmat.se/lunch/lulea/stuk/) for providing the alternativ menu data
* [Discord API](https://discord.com/developers/docs/intro) for providing the Discord bot functionality
* [requests_html](https://requests.readthedocs.io/projects/requests-html/en/latest/) for making it easy to scrape the menu from the website