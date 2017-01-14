# generate commit messages and diffs
from git import Repo


repo = Repo('../ipython')
print(repo.commit('master'))


for prev, commit in zip(repo.iter_commits('master', max_count=3),
                        list(repo.iter_commits('master', max_count=3))[1:]):
    print(commit.hexsha)
    print(commit.message)
    print()
    diffs = commit.parents[0].diff(commit, create_patch=True)
    for diff in diffs:
        print(diff.diff.decode('utf-8'))
        print()
