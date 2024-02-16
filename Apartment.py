from abc import ABC, abstractmethod
from typing import List
import urllib.request
from Option import Option

class Apartment(ABC):
    @abstractmethod
    def getPrice(self) -> List[Option]:
        pass

    def getHTMLdocument(self, url):
        return urllib.request.urlopen(url).read()