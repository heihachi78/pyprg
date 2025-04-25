import requests
#if you use an IDE, do not forget to install the requests module in the Command Line, this way:
#pip install requests
import re

def removeHTMLtags(textWithHTMLTags):
  textWithoutHTML=re.sub("<.*?>","",textWithHTMLTags)
  return textWithoutHTML

result = requests.get('http://shakespeare.mit.edu/romeo_juliet/full.html')
#knowing that the source of the web page does not contain "<" and ">" characters for other purposes than HTML tags
resultedText=removeHTMLtags(result.text)

wordList=resultedText.split()[30:]

#print(wordList)

user_input = input('Please enter a command: ')
words = set()

match user_input.split():
    case ["startsWith", char]:
        for word in wordList:
            if word.startswith(char):
                words.add(word)
    case ["endsWith", char]:
        for word in wordList:
            if word.endswith(char):
                words.add(word)
    case _:
        print('Invalid command!')

for word in words:
   print(word, end=" ")
