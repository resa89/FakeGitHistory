# Generate Git History
This is a skript to help you generate a git history for an untracked project.

_Usecase_

When you have an old project or a started project where you don't used git, but now you want to track and to version it with git, the problem with the inital commit is that all files are added at the same day. Even if the files are written long before that initial date. For the history before that intial git date you will loose temporal information. 

_Solution_

GenGitHist will help you to generate a pseudo git history for your project. You run it once, and a git history with as much commits as editing dates in the project folder are generated. And all files are added to the retrospective commits. When you push a repository afterwards, you can see all commits in the past.

_How it works_

This script will automatically look at the editing date of all files in your project folder and will automatically add those files from the same editing day to one commit. At the end you will as much commits as days you last-edited something in your project. 

When you save your git repository on github you will see the pasted commit dates at exactly that days you worked on your project in the contribution matrix with the green squares.


## Initialize folder with git

```
git init
git config --global user.name "Theresa Kocher"
git config --global user.email the.kocher@gmx.de
```

## Execute Fake Git History script
At the moment the script has to be executed from the folder where you wish to generate the git history. Then you have to relatively path to the script file.
```
python3 ../<relative>/<path>/<to>/<script>/fakeGitHistory.py -i .
```

You can choose any folder you want to instead of '.'
With ```python3 -h```you see how to use the python script.

You can check your generated commit tree with:
```
git log --graph --oneline --all
```

And you can check which files were not added to the git repo automatically with `git status`
If you wish to add them too, then add them manually with `git add <filename>` and afterwards commit them manually with `git commit -m '<commit message>'`


## Setup with your github repository
```
git remote add origin git@github.com:resa89/FakeGitHistory.git
git push --set-upstream origin master
```


## Trouble shooting (not fixed yet)
- At the moment file names with **special characters** or **spaces** are not added to the git history. To solve this you have to change the name, what will change the edition timestamp of the file. 

- If files are not added because of special characters or because they are ignored by a .gitignore file those files are still named in the commit message.

- If the script is run for another folder than '.' the command line commands don't work at the moment.


