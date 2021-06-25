import bs4
import requests
from bs4 import BeautifulSoup
from soupsieve import select
import os.path

url = "https://thoughtcatalog.com/january-nelson/2021/01/best-insults/"

class Insults():
    
    def __init__(self):
        self.result = requests.get(url)
        self.soup = BeautifulSoup(self.result.text, 'lxml')
        self.file_created = os.path.isfile('insults.txt')

    def get_insults(self):
        insults = []
        for insult in self.soup.select('.li1'):
            insults.append(insult.text)
        insults = insults[: len(insults) - 10]
        return insults
    
    def create_insults_file(self):
        insults = self.get_insults()
        myfile = open("insults.txt", mode='w')
        for insult in insults:
            myfile.write(insult + '\n')
        myfile.close()
    
    def read_insults_file(self):
        myfile = open("insults.txt", mode='r')
        content = myfile.read().splitlines()
        myfile.close()
        return content
    
    def file_main(self):
        if self.file_created:
            return self.read_insults_file()
        else:
            self.create_insults_file()
            return self.read_insults_file()
        