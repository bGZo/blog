import os
import re

def proof(path):
  with open(path, 'r') as f:
    lines = f.readlines()
    print('Read ' + path + ' successfully')

  with open(path, 'w' ) as f:
    for line in lines:
      # Half width characters
      line = re.sub(r'([\u4e00-\u9fa5])\, ([\u4e00-\u9fa5])', '\g<1>，\g<2>', line)
      line = re.sub(r'([\u4e00-\u9fa5])\. ([\u4e00-\u9fa5])', '\g<1>。\g<2>', line)

      f.write(line)

if __name__ == '__main__':
  target = r'_posts/'

  for root, dirs, files in os.walk(target):
    for article_name in files:
      article_path = root + '/' + article_name
      proof(article_path)
