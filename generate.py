# generate commit messages and diffs
import os
import sys

from git import Repo

n_commits = 10000
# output directory for extracted data
data_dir = sys.argv[1]
# repository to take commits from
repo_dir = sys.argv[2]

repo = Repo(repo_dir)

commit_itr = repo.iter_commits('master', max_count=n_commits)
next(commit_itr)

for prev, commit in zip(repo.iter_commits('master', max_count=n_commits),
                        commit_itr):
    if len(commit.parents) == 1:
        diffs = commit.parents[0].diff(commit, create_patch=True)
        for diff in diffs:
            d = ''
            try:
                d = diff.diff.decode('utf-8')
            except:
                print(diff.diff)
                continue

            with open(os.path.join(data_dir,
                                   '%s.diff' % commit.hexsha), 'w') as f:
                f.write(d[:500])

        with open(os.path.join(data_dir, '%s.msg' % commit.hexsha), 'w') as f:
            f.write(commit.message)
