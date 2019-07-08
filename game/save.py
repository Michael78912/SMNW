"""with the save file we need to be able to dump *all* relevant
data from  MAIN_GAME_STATE to a file.
I have devised a tree which will let us do so
MAIN_GAME_STATE
 Characters
  Char1
   Inventory
   Stats
  ...
 Main inventory
 Other info (like stages beaten, etc...)

now the hard part is actually making it
"""

from class_.inventory import Inventory
