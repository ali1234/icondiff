First build and install the modified svgtopng. It is modified to force
generation of a 64x64 icon instead of exiting with an error when the
size cannot be extracted from the path name.

In the top of this repo run:

    pip3 install .
    
This will install icondiff to ~/.local/bin, which should be pathed.

Run it like:

    icondiff [-a] <repository> <commit>, [<commit>, ...]
    
This will produce a directory for each commit containing the svg and png
files, and a file called ```diff.html``` which shows the changed png files side
by side.

The ```-a``` option will cause diff.html to show all png files. This is
implicit if you specify only one commit.

Quickly open the ```diff.html`````:

    xdg-open diff.html

All the directories and ```diff.html``` are created in the current directory.

Files are considered different if they are different in at least two of the
supplied commits, or if they are not present in any commit.

