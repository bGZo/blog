import os
import sys
import re

from github import Github

def output_label_articles(_repo, _name, _label):
    issues = _repo.get_issues( labels=[_repo.get_label( _label )],
                    creator=_name,
                    state='open')

    if not os.path.exists('_posts'):
        os.makedirs('_posts')
    if not os.path.exists( ('_posts/' + _label) ):
        os.makedirs('_posts/'+_label)


    for issue in issues:
        fileName = '_posts/'+ _label + '/' + \
                    issue.created_at.strftime("%Y-%m-%d") + '-' + \
                    re.sub(' ', '-', issue.title.lower()) + '.md'

        with open(fileName, "w+") as f:
            print('ok')
            f.write('---\n')
            f.write('layout: post\n')
            f.write('title: ' + issue.title+'\n')
            f.write('updated: ' + issue.updated_at.strftime("%Y-%m-%d") + '\n')
            f.write('category: ' + _label + '\n')
            f.write('comment_link: ' + 'https://github.com/bGZo/blog/issues/' + str(issue.number) + '\n')
            f.write('---' + '\n\n')
            f.write(issue.body)
        f.close()


if __name__ == '__main__':
    token = sys.argv[1]
    repoUrl = 'bgzo/blog'

    g = Github(token)
    repo = g.get_repo(repoUrl)
    name = g.get_user().login
    output_label_articles(repo,name,'posts')
    output_label_articles(repo,name,'thoughts')

