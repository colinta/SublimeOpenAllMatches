OpenAllMatches
==============

Installation
------------

Using Package Control, install "OpenAllMatches" or clone this repo in your packages folder.

I recommended you add key bindings for the commands. I've included my preferred bindings below.
Copy them to your key bindings file (⌘⇧,).

Commands
--------

`open_all_matches`: Prompts for a search, and opens all files in the project that contain the search pattern.

Options: `regex`: Perform a regular expression search (default `False`)

Key Bindings
------------

Copy these to your user key bindings file.

<!-- keybindings start -->
    { "keys": ["super+ctrl+shift+f"], "command": "open_all_matches" },
    { "keys": ["ctrl+alt+shift+f"], "command": "open_all_matches", "args": { "regex" : true } },
<!-- keybindings stop -->
