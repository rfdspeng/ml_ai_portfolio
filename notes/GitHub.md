git branch											show local branches
git branch -r										show remote branches
git checkout 'branch name'							move to local 'branch name'
git checkout -b 'branch name'						create new 'branch name' and move to 'branch name'
* `git checkout -b branch_name origin/branch_name`: Create new branch tracking `origin/branch_name`
git branch -d 'branch name'							delete 'branch name'
git push -u origin									push new commits on current branch to remote
git push --set-upstream origin 'branch name'		create new remote 'branch name' and push local 'branch name' commits
git remote show origin								show local to remote branch mapping (push and pull)
git fetch											fetch changes from remote branch
git pull											pull changes from remote branch
git status											check for changes on local branch and differences b/w remote and local branches
git add 'file or folder name'						stage changes in 'file or folder name'
git diff 'file name'								diff changes in 'file name' against committed 'file name'
git commit -m "'message'"							commit staged changes under 'message'
git restore --staged 'file or folder name'			unstage changes in 'file or folder name'
git reset											unstage all changes










git add <file>
* git add -u: stage changes to all tracked files, ignoring untracked files

git rm <file>
* git rm --cached <file>: untrack a file but keep it in the working directory (on disk)
* git rm -r <directory>: recursively delete and stage all files in a directory
* git rm -r --cached <directory>: untrack all files in a directory
* git rm -f <file>: by default, git rm will not delete a file with uncommitted changes. Use this option to forcibly remove the file.


git push -u 
git push origin main. Don't need -u?
git pull origin main
git branch dev_branch: create dev_branch
git push origin dev_branch


reading git log --oneline - understand this. origin/main, origin/dev_branch, HEAD -> main
(HEAD -> main) means this is the current commit
(origin/main) means the changes were pushed onto origin/main

git log --graph: see the graphical version of the branching

# Rolling back

git reset --soft commit_number: revert to commit commit_number. Keeps changes as staged.
git restore --staged files/folders to unstage
git checkout -- file: revert to current commit's changes

git reset commit_number: revert to commit commit_number. Keeps changes, but unstages changes.
git checkout -- file: revert to current commit's version

git reset hard?
git checkout commit_number?

# Merging local branches

On your current branch, git merge branch_to_merge
git merge branch_to_merge -m "Merged branch_to_merge"
What happens if you don't add a commit message -m?

If there are conflicts, merging will fail. Need to manually fix the conflict.

In conflict.txt,

<<<<<<<<<<<<<< HEAD
conflicting line 1
===============
conflicting line 2
>>>>>>>>>>>>>> branch_to_merge

Fix it, then commit. 

# Rebasing

# GitHub Actions - workflows are CI/CD

Automation, e.g. after pushing or merging to main, automatically run tests

In your repo, `mkdir -p .github/workflows`. In `workflows`, create `.yml` files.

example.yml

name: Example Workflow

on: [push]

jobs:
	build:
		runs-on: ubuntu-latest
	
		steps:
			- name: Checkout code
			  uses: actions/checkout@v3
			
			- name: Say Hello
			  run: echo "Hello, MLOps!" or python main.py (in your root directory)

What are unit tests?
python3 -m unittest discover tests
This is running on GitHub server, so you won't be doing anything heavy. Just sanity checks to make sure you didn't break anything.