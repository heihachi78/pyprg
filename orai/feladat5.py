#if you use an IDE, do not forget to install the requests module in the Command Line, this way:
#pip install requests

import requests
import re

def removeHTMLtags(textWithHTMLTags):
  textWithoutHTML=re.sub("<.*?>","",textWithHTMLTags)
  return textWithoutHTML

result = requests.get('http://shakespeare.mit.edu/romeo_juliet/full.html')
#knowing that the source of the web page does not contain "<" and ">" characters for other purposes than HTML tags
resultedText=removeHTMLtags(result.text)
wordList=resultedText.split()[30:]
print(wordList)