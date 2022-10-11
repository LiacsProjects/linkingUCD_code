# How to use git from the command line

## Init - initiate git on a folder  
$ git init  

## Set up an SSH conection to GitHub
https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

## Clone - get a remote git repository copy locally
$ git clone "url github"  

## Status - get a list of files which have been altered 
$ git status

## Show branch list  
$ git branch

## Checkout branch 
$ git checkout "branchname"

## Make new branch 
$ git branch "branchname"

## Add files 
$ git add "filename"

## Commit added files  
$ git commit -m "message text"

## Push commit to remote 
$ git push origin "branchname"

## Pull commits from remote  
$ git pull origin "branchname"

## Merge branch to main  
$ git checkout main 
$ git pull origin main  
$ git merge "branchname"  
$ git push origin main  

## Merge main to branch  
$ git checkout "branchname" 
$ git pull origin "branchname"  
$ git merge main  
$ git push origin "branchname"

## Remote and fetch branch changes
$ git remote
$ git remote -v
$ git fetch

## Delete branch 
$ git branch -d "branchname"

## Show merge branch tree  
$ gitk

# Install Git Bash

https://gitforwindows.org/

It will give a nice command prompt for Linux commands (emulator for Linux on Windows).

![image](https://user-images.githubusercontent.com/37830964/116661126-4272b600-a994-11eb-8c54-94e9c7f1d0ef.png)

![image](https://user-images.githubusercontent.com/37830964/116661403-af864b80-a994-11eb-87e0-e07b95e1627f.png)

Here find an example of setup of:

1. create a local branch AddGitHowTo and checkout this branch,
2. add the document HOW-TO-USE-GIT.md to it and commit. If you do not commit and checkout main, the AddGitHowTo will be merged with the local main, 
3. checkout local main, pull the remote main because this could have been changed (this is in fact a merge of remote main and local main),
4. merge the local main with the local AddGitHowTo. Step 3 + 4 are a good practise to avoid conflicts later on, so recommendation is to do this frequently,
5. add something to the document HOW-TO-USE-GIT.md and commit the change,
6. checkout the local main,
7. pull the remote main again because this could have been changed,
8. merge the local AddGitHowTo to the local main,
9. push the local main to the remote main,
10. push the local branch AddGitHowTo to the remote as well (it will be created) or delete it locally.
11. DONE!

![Sketch of Git example](https://user-images.githubusercontent.com/37830964/118492414-45093580-b720-11eb-9781-76a889761970.jpg)

