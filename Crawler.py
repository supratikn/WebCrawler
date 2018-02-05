from lxml import html
import requests
import time

class Crawler:
    
    def __init__(self,startingURL, depth):
        self.startingURL = startingURL;
        self.depth=depth;
        self.currentDepth=0
        self.links=[]
        self.apps =[];
        
    def crawl(self):
        app =self.getLink(self.startingURL)
        self.apps.append(app)
        self.links.append(app.links)
        
        while self.currentDepth<self.depth:
            currentLinks = []
            for link in self.links[self.currentDepth]:
                currentApp = self.getLink(link)
                currentLinks.extend(currentApp.links)
                self.apps.append(currentApp)
                
                time.sleep(5)# so apple doesn't sue me
                
            self.currentDepth+=1
            self.links.append(currentLinks)    
            
        return 
    
    def getLink(self,link):
        page = requests.get(link)
        tree=html.fromstring(page.text)
        
        name = tree.xpath('//h1[@itemprop="name"]/text()')[0] #look at all the descendents 
        developer = tree.xpath('//div[@class="left"]/h2/text()')[0]
        price = tree.xpath('//div[@itemprop="price"]/text()')[0]
        links = tree.xpath('//div[@class="center-stack]//*/a[@class="name"]/@href')
        
        app = App(name, developer, price, links)
        
        
            
        return app
    
    
    
    
class App:
    
    def __init__(self, name, developer, price, links):
        self.name= name;
        self.developer = developer;
        self.price = price;
        self.links=links;    
    
    def __str__(self):
        return ("Name: "+self.name.encode('UTF-8')+
        "\r\nDeveloper: "+self.developer.encode('UTF-8') +
        "\r\nPrice: "+ self.price.encode('UTF-8')+ "\r\n")
        
        
crawler = Crawler('https://itunes.apple.com/us/app/clash-royale/id1053012308?mt=8', 0)
crawler.crawl()    

for app in crawler.apps:
    print (app)
           
