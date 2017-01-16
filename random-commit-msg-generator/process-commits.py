from git import Repo
import sys

repo_dir = sys.argv[1]
out_file = sys.argv[2]
repo = Repo(repo_dir)


def get_commit_title(commit):
    return commit.message.split('\n', 1)[0]


with open(out_file, 'w') as text_file:
    for commit in repo.iter_commits():
        msg = str(get_commit_title(commit))
        if not msg.startswith('Merge'):
            text_file.write(msg + '\n')
