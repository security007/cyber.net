from bs4 import BeautifulSoup as bs
import requests
from Wappalyzer import Wappalyzer, WebPage
from urllib.parse import urlparse, parse_qs
import base64
import socket


class Garuda:
    def __init__(self):
        self.__version = "1.0.0"
        self.__database = "https://www.bing.com/search?q="
        self.__useragent = "Garuda/{} AppleWebKit/537.36 (KHTML, like Gecko) Garuda/103.0.0.0 NKRI/537.36".format(
            self.__version)

    def portScanner(self, dm):
        res = []
        prt = [80, 8080, 443, 3306, 21, 22, 23,
               139, 137, 445, 8443, 20, 69, 25, 53, 3389]
        sub = {80: 'HTTP', 8080: 'HTTP', 443: 'HTTPS', 8443: 'HTTPS', 445: 'SMB', 137: 'NetBios', 139: 'NetBios',
               3306: 'MYSQL', 21: 'FTP', 20: 'FTP', 22: 'SSH', 23: 'TELNET', 69: 'TFTP', 25: 'SMTP', 53: 'DNS', 3389: "REMOTE DESKTOP"}
        try:
            # will scan ports between 1 to 65,535
            for port in prt:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex(
                    (urlparse(dm).netloc.replace("www.", ""), port))
                if result == 0:
                    res.append("{"+str(port)+":"+str(sub[port])+"}")
                s.close()
        except socket.gaierror:
            res = "Can't Resolve Hostname"
        except socket.error:
            res = "Server Not responding"
        return str(res)

    def getDomain(self, web):
        return "https://"+urlparse(web).netloc

    def scan(self, tg):
        try:
            wappalyzer = Wappalyzer.latest()
            webpage = WebPage.new_from_url(self.getDomain(tg))
            try:
                res = wappalyzer.analyze(webpage)
            except Exception as e:
                res = "Error Scanning Web Technology"
            return str(res)
        except Exception as e:
            return("Error Scanning Web Technology")

    def scrap(self, query="", customPage=False):
        cookie = {
            "SRCHHPGUSR": "SRCHLANG=id&ADLT=OFF&NNT=1&HAP=0&VSRO=1"}  # Don't filter everything
        head = {"User-Agent": self.__useragent}
        judul = []
        link = []
        desc = []
        miniLink = []
        if customPage != False:
            r = requests.get("https://www.bing.com/" +
                             str(customPage), headers=head, cookies=cookie)
        else:
            r = requests.get(self.__database + query,
                             headers=head, cookies=cookie)
        soup = bs(r.text, "lxml")
        # cari data yang dibutuhkan
        content = soup.find_all("li", {"class": "b_algo"})
        if content != None:
            for i in content:
                try:
                    judul.append(i.find("h2").text)
                except:
                    pass
                try:
                    link.append(i.find("a", href=True)["href"])
                except:
                    pass
                ds = i.find("div", {'class': 'b_caption'})
                try:
                    desc.append(ds.find("p").text)
                except:
                    pass
                miniLink.append(i.find("div", {"class": "b_attribution"}).text)
        nextPage = soup.find("a", {"class": "sb_pagN"}, href=True)
        if nextPage != None:
            nx = nextPage["href"]
            nextP = base64.b64encode(bytes(nx, "utf-8"))
        else:
            nextP = None
        res = list(zip(judul, link, desc, miniLink))
        return {'results': res, 'nextP': nextP}


# if __name__ == "__main__":
#     c = Garuda()
#     print(c.scrap(query="Kemerdekaan Indonesia"))
