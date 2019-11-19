# PyGo
Implementation of Go developed in Python3 using PyQt

## Overview
Go ("encircling game") is an abstract strategy board game for two players, in which the aim is to surround more territory than the opponent.

The game was invented in China over 3,000 years ago, and is therefore believed to be the oldest board game continuously played today. It was considered one of the four essential arts of the cultured aristocratic Chinese scholars in antiquity. Despite its relatively simple rules, Go is very complex, even more so than chess.

## Setup
To get started:

1. Ensure you have git bash tools installed on windows: https://git-scm.com/downloads, this comes natively with Linux / MacOSX
2. Ensure you also have python3, pip3, and virtualenv installed, pip3 comes bundled with python3
3. In the command line clone this repository to your local computer: `git clone git@github.com:Mattamorphic/PyGo.git`
4. While still in the command line run: `bin/setup` from the root of this project,  this setup script will:

- Check to make sure you are in the correct directory by ensuring the app directory is present
- Deactivate any virtual environment you are currently running
- Clear the local ./venv folder if it's present (the virtual environment)
- Create and start a new virtual environment in ./venv
- Download the required modules and install these to the virtual environment
- Start the app

## Making your changes
Once you have setup the project, you can begin working on your changes, you shouldn't have to set this up again unless something goes very wrong.

_Get Hacking!_

The following will walk you through everything you need to get started.


> The reason for all of the below is to allow multiple contributors to work together on a code base. This covers some considerations for using git, as well as how to apply automated formatting fixes, and checks against style to ensure that the code we are writing is standardised.


### Step 1: Creating a branch
Create branch to work on, this should include your username, and the overall goal of the changes you are making, for instance:

`@Mattamorphic/implementing-pieces`

You can create a branch with the following git command:

`git checkout -b @username/branch-name`

These should be created from master, unless you are working on a sub feature of a feature:

1. Checkout master
  - `git checkout master`
2. Pull down any changes
  - `git pull`
3. Create your branch
  - `git checkout -b @username/branch-name`

### Step 2: Coding
Go ahead and code away!

Try to ensure you are following [commenting standard format](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### Step 3: Running the app

Once you've made a change, you want to make sure it works.
In the command line run `bin/start`

This command will:

- Check the virtual environment exists
- Deactivate any running virtual environment
- Start the project specific virtual environment
- Launch the app

Check your change, and if necessary go back to _Step 2_

### Step 4: Committing your changes
Once you've made a change, you'll want to commit this.

Some rules for creating a commit:

1. Commits should be informative

- `Fixed index out of bounds error` :smile:
- `Some fixes` :cry:

2. Commits should be atomic, a commit should be a single pragmatic change, it's better to have lots of small commits, than to have one big commit:

   - `Implement board array` :smile:
   - `Implement board array, and helper functions, and class` :cry:

3. There is a build script that:

  - Runs `yapf` formatting rules, and [formats the code](https://github.com/google/yapf)
  - Runs `flake8` to ensure the code is meeting [python3 pep8 standards](https://www.python.org/dev/peps/pep-0008/)
  - Finally it will regenerate the documentation (in the docs folder)


 #### Creating a commit

 Creating a commit, a snapshot, is relatively straight-forward:

 1. Save the changes you've just made
 2. In the command line run `git status` to see the file changes you've made
 3. Stage the changes you've made, basically decide what to commit - if you want to commit all your changes run `git add .`
 4. Run `git commit -m "INFORMATIVE MESSAGE"` replacing informative message with your amazing commit message


### Step 5: Pushing your changes
When you are ready to push all the changes in your branch up to GitHub run:

`git push`

If the branch isn't yet on GitHub you'll be prompted to set this branch on origin:

`git push --set-upstream origin @username/branch-name`

### Step 6: Pull request, and merging your changes
Once your changes have been pushed to GitHub you can propose your changes to the code base. Create a pull request merging from your branch, into the source of truth, the master branch.

Creating this pull request will also trigger GitHub Actions that will run our CI:

- It will run the `bin/build` script across the whole pull request
- It will run any associated unit / integration tests and report the results

Once we're happy with the changes, we'll merge them into master - Woohoo! :tada:

## Want more help with Git/GitHub?
Firstly, If you are new to Git, I would recommend going through this interactive tutorial:

http://try.github.io

Following this there is the GitHub learning lab, where you can learn more about the GitHub specific tools and features:

https://lab.github.com/

Finally, here's a list of great resources for learning Git and GitHub:

https://help.github.com/articles/what-are-other-good-resources-for-learning-git-and-github
