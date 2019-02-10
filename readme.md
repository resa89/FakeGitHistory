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


## Setup with your github repository
```
git remote add origin git@github.com:resa89/FakeGitHistory.git
git push --set-upstream origin master
```


## Trouble shooting
At the moment file names with special characters are not added to the git history. To solve this you have to change the name, what will change the edition timestamp of the file. 