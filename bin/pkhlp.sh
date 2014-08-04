#!/bin/bash
# pflint Fri 17 May 2013 07:49:14 AM EDT 
# packs html into String
#
read -d '' String <<"EOF"
-
                          *****DOCUMENTATION*****
 You get this documentation when you put in the wrong number of arguments...
 The name of this program is template.sh, a collection of general purpose tools.
 for managing printing at the VDOL.  This is released under GPL I
 The syntax is:
  - template.sh dummy tests the dummy function
    Output is delivered to the screen...
  - template.sh pause <message> displays message and with enter exits normally
  - template.sh wait <n> <filename> where "n" is
  - template.sh get <n> <message> where "n" is wait time,displays message
    and exits normally
  - template.sh get <n> <filename> where "n" is
  - template.sh get all <n> where "n" is typically
    Output is delivered to the directory you are in...
 For structure information type "grep '^\#\*' template.sh"
    :^)
 (C) P Flint, Barre Open Systems Institute Liscensed under GPLI

EOF
# echo "this is the string"
echo "$String"
