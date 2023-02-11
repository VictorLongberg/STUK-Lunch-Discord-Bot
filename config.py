# URL for the restaurant's menu page
url_stuk = "https://www.stuk.nu/"

url_stuk_div = '//div[@class="w-restaurant-menu"]'

# Alternativ url for the restaurant's menu page
url_matochmat = "https://www.matochmat.se/lunch/lulea/stuk/"

url_matochmat_div = '//div[@class="lunchMenuDetailsDay"]'

# PDF to Image variables
base_url = "https://www.matochmat.se/rest/menu/?"

restaurant = "pqoaIFGvfWDNJYeU8bOQSA%3D%3D" #resturant variable, stuk

pdf_type = "weekly"

pdf_bol = True

# List of available commands
commands = {
    "   **!menu**": "`Displays the restaurant's menu`",
    "   **!help**": "`Lists all the commands the bot has`",
    "   **!url**": "`shows the url from which the menu was taken`",
    "   **!pdf**": "`shows an image of the menu`"
}
