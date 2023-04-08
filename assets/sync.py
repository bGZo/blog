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

        post_body=issue.body
        post_property = ''
        post_property += '---\n'
        post_property += 'layout: post\n'

        pattern = r"<!--title:\s*\"([^\"]+)\"\s*-->"
        match = re.search(pattern, post_body)
        if match:
            post_title = match.group(1)
            post_body = re.sub(pattern, "", post_body)
            post_property += 'title: "' + post_title +'"\n'
        else:
            post_property += 'title: "' + issue.title +'"\n'

        post_property += 'updated: ' + issue.updated_at.strftime("%Y-%m-%d") + '\n'
        post_property += 'category: ' + _label + '\n'
        post_property += 'source: ' + 'https://github.com/bGZo/blog/issues/' + str(issue.number) + '\n'
        post_property += 'number: ' + str(issue.number) + '\n'
        post_property += '---' + '\n\n'

        with open(fileName, "w+") as f:
            print('open successfully')
            f.write(post_property)
            f.write(post_body)
        f.close()

if __name__ == '__main__':
    token = sys.argv[1]
    repoUrl = 'bgzo/blog'

    g = Github(token)
    repo = g.get_repo(repoUrl)
    name = g.get_user().login
    output_label_articles(repo,name, 'posts')
    output_label_articles(repo,name, 'thoughts')
    output_label_articles(repo,name, 'letters')
