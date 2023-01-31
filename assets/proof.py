import os
import re

def proof(path):
  with open(path, 'r') as f:
    lines = f.readlines()
    print('Read ' + path + ' successfully')

  with open(path, 'w' ) as f:
    for line in lines:
      line = re.sub(r'\[(.*?)\|(.*?)\]', '[\g<1>-\g<2>]', line)

      # Half width characters
      line = re.sub(r'([\u4e00-\u9fa5])\, ([\u4e00-\u9fa5])', '\g<1>，\g<2>', line)
      line = re.sub(r'([\u4e00-\u9fa5])\. ([\u4e00-\u9fa5])', '\g<1>。\g<2>', line)

      # Logseq
      line = re.sub(r'  \n', '\n', line)
      line = re.sub(r'[^!]\[([A-Z0-9_]+)\]', '[^\g<1>]', line)

      # URL via: https://stackoverflow.com/questions/3809401
      line = re.sub(r'( )(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)([;, ])', '\g<1><\g<2>>\g<3>\g<4>', line)
      line = re.sub(r'^(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)', '<\g<1>>', line)

      f.write(line)

if __name__ == '__main__':
  target = r'_posts/'

  for root, dirs, files in os.walk(target):
    for article_name in files:
      article_path = root + '/' + article_name
      proof(article_path)
