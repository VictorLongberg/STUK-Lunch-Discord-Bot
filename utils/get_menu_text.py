from requests_html import AsyncHTMLSession
import re
from config import url_stuk, url_stuk_div, url_matochmat, url_matochmat_div

# TODO Fix so that the error message gets deleted after 60s if !Menu / get_menu_text() fails
# Format the menu text
async def get_menu_text():
    try:
        # source of the url
        source = url_stuk
        # create an AsyncHTMLSession object
        asession = AsyncHTMLSession()
        # use the object to send a GET request to the menu page
        r = await asession.get(url_stuk)
        # wait for the page to load
        await r.html.arender()
        # find all elements with the class "w-restaurant-menu"
        menu = r.html.xpath(url_stuk_div, first=False)

        # If theres not a menu on the stuk url, attempt using the matchomat url instead
        if len(menu) == 0:  # if menu is empty
            # source of the url
            source = url_matochmat
            # create an AsyncHTMLSession object
            r = await asession.get(url_matochmat)
            # wait for the page to load
            await r.html.arender()
            # find all elements with the class "w-restaurant-menu"
            menu = r.html.xpath(url_matochmat_div, first=False)

        # A list of all menu items and dates in text form
        itemlist = []

        # Extract text from menu elements and clean it up
        for item in menu:
            itemlist.append(item.text)

        # TODO cleanup this regex
        # Formatting the list
        cleaned_list = ""
        if source == url_stuk:
            cleaned_list = [re.sub(r"(\d+ kr|\nkr)", "", item) for item in itemlist if "Lördag" not in item and "Söndag" not in item]
            cleaned_list = [re.sub(r"\n\n", " ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(\n)$", "", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(\nLaktosfri|Laktorsfri)", " **Laktosfri** ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(\nGlutenfri|Glutenfri)", " **Glutenfri** ", item) for item in cleaned_list] 
            cleaned_list = [re.sub(r"(\nVegansk|Vegansk)", "  **Vegansk** ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(Laktosfri\n)", " **Laktosfri** \n", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(Glutenfri\n)", " **Glutenfri** \n", item) for item in cleaned_list] 
            cleaned_list = [re.sub(r"(Vegansk\n)", "  **Vegansk** \n", item) for item in cleaned_list]
            print(cleaned_list)

        elif source == url_matochmat:
            cleaned_list = [re.sub(r"\n105\xa0kr\n", " ", item) for item in itemlist if "Lördag" not in item and "Söndag" not in item]  # for the matchomat menu
            cleaned_list = [re.sub(r"\nmed", " ", item) for item in cleaned_list]  # for the matchomat menu
            cleaned_list = [re.sub(r"\n\n", " ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(\n)$", "", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"\n\n", " ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"\n([a-z])", r" \1", item) for item in cleaned_list]  # for the matchomat menu
            cleaned_list = [re.sub(r"(\nLaktosfri|Laktorsfri)", " **Laktosfri** ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(\nGlutenfri|Glutenfri)", " **Glutenfri** ", item) for item in cleaned_list] 
            cleaned_list = [re.sub(r"(\nVegansk|Vegansk)", "  **Vegansk** ", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(Laktosfri\n)", " **Laktosfri** \n", item) for item in cleaned_list]
            cleaned_list = [re.sub(r"(Glutenfri\n)", " **Glutenfri** \n", item) for item in cleaned_list] 
            cleaned_list = [re.sub(r"(Vegansk\n)", "  **Vegansk** \n", item) for item in cleaned_list]
            print(cleaned_list)

        # cleaned_list should be in the format of is a list of [Day of the week dd/mm \n menu item \n menu item \ menu item .....]
        # the list is handled by splitting at the \n 

        formatted_menu = ""
        for item in cleaned_list:
            day = item.split("\n")[0]
            meals = item.split("\n")[1:]
            formatted_menu += "\n**" + day + "**\n"
            for meal in meals:
                formatted_menu += "• " + meal + "\n"

        # if the fommatted menu is empty, theres nothing to scrape from, the menu has yet to be updated.
        if len(formatted_menu) == 0:
            formatted_menu = "\n**The menu has not yet been uploaded, try again later **"
            return formatted_menu
        formatted_menu = "\n**Stuk Lunch Menu:  **\n\n**  Source**: <" + source + ">\n" + formatted_menu
        return formatted_menu

    except Exception as e:
        print(f'An error occurred: {e}')
        return 'Sorry, an error occurred while trying to fetch the menu.'
