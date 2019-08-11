import requests
import bs4

alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("urban_dict.txt", 'w') as f:

    for char in alph:
        # Note that when you ask for a page that is out of range, you get redirected to the Urban Dictionary homepage.
        # Also, explicitly entering page=1 sends you to a different page
        page = 1 
        params = {"character":char}
        # For keeping track of the scraper's progress
        print(char)

        while True:
     
            response = requests.get("https://www.urbandictionary.com/browse.php", params = params)
            html = response.text 
            url = response.url

            if (url == "https://www.urbandictionary.com/"):
                # This will occur if you get redirected to the Urban Dictionary homepage (i.e.
                # out of page range
                break
            
            else:

                soup = bs4.BeautifulSoup(html, "html.parser")
                # 'main' is a narrowed-down version of 'soup' which just contains the block
                # on which the words are listed (this prevents interference from other a-tags)
                main = soup.find(class_ = "no-bullet")
            
                taglist = main.find_all("a")

                for tag in taglist:
                
                    f.write(tag.string)
                    f.write('\n')

                page += 1
                params["page"] = page


