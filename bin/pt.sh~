#!/bin/bash
# tests what we want to do
echo "This starts the test"
echo $@
# for f in url1:filename1 url2:filename2 url3:filename3; 
for f in $@; 
do 
	URL=${f%:*}; 
	FILENAME=${f#*:} ;  
	echo "$URL $FILENAME" ; 
done
