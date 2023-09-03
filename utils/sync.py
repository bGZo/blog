import os
import sys
import re
import argparse
from github import Github


PROPERTIES_TEMPLATE = (
    "---\n"
    "layout: post\n"
    "title: {}\n"
    "updated: {}\n"
    "category: {}\n"
    "source: https://github.com/bGZo/blog/issues/{}\n"
    "number: {}\n"
    "---\n"
    "\n"
)
TITLE_PATTERN = r"<!--title:\s*\"([^\"]+)\"\s*-->"


def get_issue_properties(issue, _label):
    return PROPERTIES_TEMPLATE.format(
        get_custom_title(issue),
        issue.updated_at.strftime("%Y-%m-%d"),
        _label,
        str(issue.number),
        str(issue.number)
    )

def get_custom_title(issue):
    content = issue.body
    match = re.search(TITLE_PATTERN, content)
    if match:
        return match.group(1)
    else:
        return issue.title

def get_issue_body(issue):
    post_body = issue.body
    post_body = re.sub(TITLE_PATTERN, "", post_body)
    return post_body


def output_label_articles(_repo, _name, _label):
    target_directory = "_posts/" + _label + "/"
    os.makedirs(os.path.dirname(target_directory), exist_ok=True)

    issues = _repo.get_issues( 
                labels=[_repo.get_label( _label )],
                creator=_name,
                state='open')
    for issue in issues:
        target_file =   target_directory + '/' + issue.created_at.strftime("%Y-%m-%d") + \
                        '-' + re.sub(' ', '-', issue.title.lower()) + '.md'
        post_property   = get_issue_properties(issue, _label)
        post_body       = get_issue_body(issue)


        with open(target_file, "w+") as f:
            f.write(post_property)
            f.write(post_body)
        print('Wirte ' + issue.title + " successfully.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--token', action = 'store',
                        help='Type in your github token')
    parser.add_argument('-p','--repository', action = 'store',
                        help='Type in your repository name, like bgzo/blog')
    parser.add_argument('tags', nargs = '+',
                        help='Type in your tags want to be searched')
    args = parser.parse_args()

    if args.token is not None:
        token = args.token
        print("Parse token  successfully.")
    if args.repository is not None:
        repo_address = args.repository
        print("Parse repo   successfully.")
    if args.tags is not None:
        tags_list = args.tags
        print("Parse tags   successfully.")

    g = Github(token)
    repo = g.get_repo(repo_address)
    name = g.get_user().login
    print("Login Github successfully.")

    for tags in tags_list:
        output_label_articles(repo, name, tags)
