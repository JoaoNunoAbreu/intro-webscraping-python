import fileinput
# Beautiful Soup
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# read options
print("Insert the product here: ",end = "")
item = "+".join(input().split())
print("Searching...")
my_url = "https://www.fnac.pt/SearchResult/ResultList.aspx?SCat=0%211&Search=" + item + "&sft=1&sa=0"
# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html,"html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"clearfix Article-item js-Search-hashLinkId"})

print("Completed!")
print("Show results in:")
print("\t1 - stdin")
print("\t2 - file.csv")
print("Choice: ",end="")
choice = int(input())

while(choice != 1 and choice != 2):
    print("Invalid option!")
    print("Choice:",end="")
    choice = int(input())

if(choice == 2):
    filename = "products.csv"
    f = open(filename,"w")
    headers = "name, price\n"
    f.write(headers)

if(choice == 1):
    print("--------------")

for container in containers:
    name_container = container.a.get_text(strip=True)
    price_container = container.find("div","floatl")
    if price_container.find("strong"):
        price_container = price_container.get_text(strip=True).replace("\xa0","")
    else:
        price_container = container.find("div","floatl").a.get_text(strip=True).replace("\xa0","")
    
    if(choice == 1):
        print("Name : " + str(name_container))
        print("Price : " + str(price_container))
        print("--------------")
    else:
        f.write(name_container.replace(",","|") + "," + price_container.replace(",",".") + "\n")

if(choice == 2):
    f.close()