#!/bin/bash
# make an html file for installation in output
rm -rf $2; touch $2 ; chmod +x $2
cat $1 | while read line; do echo "#html "$line >> $2; done 
# echo "grep -e \"^#html\" $0 |cut -c 7-  "
echo "grep -e \"^#html\" $2 |cut -c 7-  "  >> $2

