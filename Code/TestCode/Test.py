import pygit2

# Path to your local repository
repo_path = 'C:/Projects/GitClient/Repo/Git-Client'

# Open the local repository
repo = pygit2.Repository(repo_path)

# Display commit history
for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TIME):
    print(f"Commit: {commit.message}")
