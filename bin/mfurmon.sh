#!/bin/bash
# pflint Tue 18 Dec 2012 07:35:16 AM EST Start Program Design
# pflint Fri 01 Mar 2013 07:24:48 AM EST refactor into three systems
# add a test output feature puts test in description field
# Thu 21 Mar 2013 11:19:14 AM EDT add furnace object
# 
version="0.130321"
#
# unset term to make crontab based stuff happy
tset=$TERM
unset TERM
#
# hold environment
export S=$PWD
#
#* move to the appropriate directorygrep '^\#\*' mfurmon.sh
cd /var/www
# cd ??
#
#* check location of vital programs, sanity check
# timeout
# python 2.6
# pythhon serial
# miniterm
#
#* check location of vital files, sanity check
# ??
#
# Define files to be used
# uid="" ; if [ "$uid" == "" ]; then echo "Set user id!"; exit; fi
# passwd="" ; if [ "$passwd" == "" ]; then echo "Set user passwd!"; exit; fi
# ??
# hold environment
export S=$PWD
tset=$TERM
unset TERM
rm -rf /var/lock/mrtg/_etc_mrtg_itemp.cfg_l
# pflint Sun 23 Dec 2012 01:28:59 PM EST 
# outputs mrtg compatible temperatures
# echo "here we go"
# msg1=$(uptime|cut -d "," -f 1| cut -d " " -f 5)
msg1=$(uptime|cut -d "," -f 1 | rev |cut -d " " -f 1 | rev)
tlog="/var/www/itemp/logs/itemp.log"
# echo -n "starting mfurmon.sh "#d >> $tlog ;date #d >> $tlog 
#* move to the appropriate directorygrep '^\#\*' mfurmon.sh
#
#* check location of vital files and programs, sanity check
# ??
#
# Define files to be used
# uid="" ; if [ "$uid" == "" ]; then echo "Set user id!"; exit; fi
# passwd="" ; if [ "$passwd" == "" ]; then echo "Set user passwd!"; exit; fi
# ??
#
#
#* function help  - Help function for template basic help goes here
function help(){
clear;
echo "This is "$0"  version "$version
cat $0 | grep '^## ' | sed -e 's/##//'
# echo "This is the help function"
##                       *****DOCUMENTATION*****
## You get this documentation when you put in the wrong number of arguments...
## The name of this program is mfurmon.sh, a collection of tools 
## This is released under GPL I
## The syntax is:
##  - mfurmon.sh itemp writes itemp.data with proper information 
##  - mfurmon.sh otemp writes otemp.data with proper information 
##  - mfurmon.sh cit   outputs itemp.data for use in mrtg
##  - mfurmon.sh cot   outputs otemp.data for use in mrtg
##  - mfurmon.sh testo <n> tests outside *must have <n> number*
##  - mfurmon.sh testi <n> tests house *must have <n> number*
##  - mfurmon.sh status outputs raw data from arduino
##  - mfurmon.sh tempf <1-N> details a current or temperature
##    the output in Fahrenheit is delivered to the screen...
##  - mfurmon.sh tempc <1-N> details a current or temperature
##    the output in Centigrade is delivered to the screen...
##  - mfurmon.sh cleanup [test] optionally a rehearsal
##    Output is delivered to the directory you are in...
##  - mfurmon.sh nz numbers zombie tparse processes
##  - mfurmon.sh kz lists and kills related zombie processes
##    Output is delivered to the screen...
##  - mfurmon.sh status details what the current situation is
##    where n is interger number end-to-end test   
##  - mfurmon.sh dummy the test program  
## For structure information type "grep '^\#\*' mfurmon.sh"
##    :^)
## (C) P Flint, Flint Information Technology Systems, licensed under GPL1
##
#          *****Documentation Loop ends here the rest is function******
} # Test: mfurmon.sh
#
#* function dummy - Rename and fill stuff in between braces
function dummy(){
echo "In version "$version" This is the dummy function"
} # Test:
#
#
#* function cit - cat indoor temps 
function cit(){
out="/var/www/itemp/itemp.data"
tlog="/var/www/itemp/logs/itemp.log"
echo "In version "$version" This is the cit function" >> $tlog
cd /var/www/itemp
# check data...
echo "itemp lines are "$(wc -l $out) >> $tlog
# get data...
cat $out
} # Test: mfurmon.sh cit
#
#
#* function cot - cat outdoor temps
function cot(){
# echo "In version "$version" This is the cot function"
cd /var/www/otemp
out="/var/www/otemp/otemp.data"
tlog="/var/www/otemp/logs/otemp.log"
# check data...
echo "otemp lines are "$(wc -l $out) >> $tlog
# get data...
cat $out
} # Test:
#
#
#* function testo - tests the house all the way through
function testo(){
echo "In version "$version" This is the testo function" #debug 
#debug echo "args = "$#"  var1= "$var1"    var2= "$var2"   var3=  "$var3"   ARGS=  "   
#
# first name the logs..
tlog="/var/www/otemp/logs/otemp.log"
#
# remove log files and reset
rm $tlog 
touch $tlog 
# remove lock file
rm -rf /var/lock/mrtg/*
#
echo "do $var2 times"
# do this thing.
for i in $(eval echo {1..$var2}) 
do 
 env LANG=C /usr/bin/mrtg /etc/mrtg/otemp.cfg 2>>$tlog >> $tlog 
 echo "just did otemp "$i; 
done
} # Test:mfurmon.sh testo
#
#
#* function testi - tests the house all the way through
function testi(){
echo "In version "$version" This is the testi function" #debug 
#debug echo "args = "$#"  var1= "$var1"    var2= "$var2"   var3=  "$var3"   ARGS=  "  
#
# first name the logs..
tlog="/var/www/itemp/logs/itemp.log"
#
# remove log files and reset
rm $tlog 
touch $tlog 
rm -rf /var/lock/mrtg/*
#
# echo $var2
echo "do $var2 times"
# do this thing.
# for i in {1..'$var2'};
for i in $(eval echo {1..$var2}) 
do 
 env LANG=C /usr/bin/mrtg /etc/mrtg/itemp.cfg 2>>$tlog >> $tlog 
 echo "just did itemp "$i; 
done
} # Test:mfurmon.sh testi
#
#
#* function status - Outputs the whole frame. Use this to troubleshoot. 
function status(){
echo "This is the status function to end use <ctrl> ]"
# device="/dev/ttyACM0"
device="/dev/ttyUSB0"
# python /usr/share/doc/python-serial/examples/miniterm.py -p $device -D #|sed 's|\\x1b\[2J|\n|' 
python /usr/share/doc/python-serial/examples/miniterm.py -p $device -D |sed 's|\\xfe| |g' #|sed 's|\\xfe| |g' 
} # Test:
#
#
#* function tempf - Outputs only an integer
function tempf(){
#debug echo "args = "$#"  var1= "$var1"    var2= "$var2"   var3=  "$var3"   ARGS=  "$ARGS >> /var/www/itemp/logs/itemp.log result=$(timeout 5 python /usr/share/doc/python-serial/examples/miniterm.py -p /dev/ttyACM0 -D 2>/dev/null |
result=$(timeout 5 python /usr/share/doc/python-serial/examples/miniterm.py -p /dev/ttyACM0 -D 2>/dev/null |
	         while read line; 
			do 
				if [[ "$line" == *"temp$var2"* ]]; 
				then 
				 echo $line; 
			        fi; 
			    done | 
	                     rev | 
       		 cut -d " " -f 1 | 
                               rev)
stty sane 2>/dev/null
test=$(echo $result | tr -d [:punct:])
if ! [ "$test" -eq "$test" ] 2>/dev/null; then # is this a string or a number?
# if [ "$test" -eq "$test" ] 2>/dev/null; then # is this a string or a number?
  # echo "error "$result   # it is a string 
  # add an increment variable...fix zombie
  tempf $var2 
else 
  echo $result | cut -d "." -f 1
fi
} # Test:./2tp.sh tempf 1
#
#* function tempc - Outputs the whole line...
function tempc(){
#debug echo $#"     "$var1"     "$var2"    "$var3"    "$ARGS 
# echo -n "temp$var2 in Centigrade is: "
result=$(timeout 5 python /usr/share/doc/python-serial/examples/miniterm.py -p /dev/ttyACM0 -D 2>/dev/null |
	         while read line; do if [[ "$line" == *"temp$var2"* ]]; then echo $line; fi; done | 
	     							                          head -1 | 
											      rev | 
                                                                                  cut -d " " -f 3 | 
                                                                                              rev )
stty sane 2>/dev/null
# if ! [[ "$result" =~ ^[0-9]+([.][0-9]+)?$ ]] ; then
# if [[ "$result" =~ ^[0-9]+([.][0-9]+)?$ ]] ; then
if [ "$result" -eq "$result" ] 2>/dev/null; then
  echo "error" 
  tempc $var2 
else 
  echo $result 
fi
} # Test:./2tp.sh tempc 1
#
#
#* function otemp - get outside temp data...
function otemp(){
outo="/var/www/otemp/otemp.data"
tlog="/var/www/otemp/logs/otemp.log"
echo "Version "$version" resetting "$outo;rm -rf $outo; touch $outo
echo -n "parsing temp 1 (outside temp) ">> $tlog;date >> $tlog
/var/www/bin/mfurmon.sh tempf 1 | cut -d "." -f 1 >> $outo 2>/dev/null #debug| tee --append  $outo 2>/dev/null
echo 0 >> $outo 2>/dev/null #debug| tee --append  $outo 2>/dev/null
echo $msg1 >> $outo 2>/dev/null #debug | tee --append  $outo 2>/dev/null
echo "Outside temperature" >> $outo 2>/dev/null #debug | tee --append  $outo 2>/dev/null
cat $outo >> $tlog
} # Test: mfurmon.sh otemp
#
#* function itemp - get inside temp data...
function itemp(){
outh="/var/www/itemp/itemp.data"
tlog="/var/www/itemp/logs/itemp.log"
# get house temp data...
echo "version $version at $(date +%T) resetting $outh and removing locks " >> $tlog
rm -rf $outh; touch $outh
rm -rf /var/lock/mrtg/*
echo -n "parsing temp 2 ">> $tlog;date >> $tlog
/var/www/bin/mfurmon.sh tempf 2 | cut -d "." -f 1 | tee --append  $outh >> $tlog 2>$tlog
echo -n "parsing temp 3 ">> $tlog;date >> $tlog
/var/www/bin/mfurmon.sh tempf 3 | cut -d "." -f 1 | tee --append  $outh >> $tlog 2>$tlog
echo $msg1  | tee --append  $outh >> $tlog 2>$tlog
echo "steam and hot water temperature" | tee --append  $outh >> $tlog 2>$tlog
# echo 0
# echo "Inside temp"
cat $outh >> $tlog
} # Test: mfurmon.sh itemp
#
#* function nz - enumerates all tparse zombies
function nz(){
echo "* number args: "$#" var1" "$var1" var2: "$var2" var3: "$var3"    "$ARGS" #debug 
if [ $var2 ] 
then 
 zombie=$var2; echo -n "At $(date +%T) the number of $zombie zombies is: "; ps aux | grep $zombie |grep -v gedit | grep -v grep | wc -l
else
 for zombie in mtsp tparse python 
  do
   echo -n "At $(date +%T) the number of $zombie zombies is: "; ps aux | grep $zombie |grep -v gedit | grep -v grep | wc -l
  done
fi
#echo -n "At ";date;echo -n "the number of python zombies is: "; ps aux | grep python |grep -v gedit | grep -v grep | wc -l
} # Test: itemp.sh nz
#
#
#* function kz - kill all tparse zombies
function kz(){
zombie="mtsp"
echo -n "At ";date;echo -n "the number of zombies is: "; ps aux | grep tparse |grep -v gedit | grep -v grep | wc -l
echo -n "number of temp.sh zombies is ">> $tlog;ps aux | grep tparse |grep -v gedit | grep -v grep | wc -l>> $tlog
ps aux | grep $zombie |grep -v gedit | grep -i temp| tr -s [:space:] |cut -d " " -f 2 |xargs -I xxx kill -9 xxx 2>/dev/null
ps aux | grep $zombie |grep -v gedit | grep -i temp| tr -s [:space:] |cut -d " " -f 2 |xargs -I xxx kill -9 xxx 2>/dev/null
# ps aux | grep mtsp |grep -v gedit | tr -s [:space:] |cut -d " " -f 2 |xargs -I xxx kill -9 xxx 2>/dev/null
echo -n "Now there are this number of zombies  ">> $tlog;ps aux | grep tparse |grep -v gedit | grep -v grep | wc -l>> $tlog
} # Test: itemp.sh kz
#
#
#* function kz - kill all python zombies
function kpz(){
zombie="python"
echo -n "At ";date;echo -n "the number of zombies is: "; ps aux | grep tparse |grep -v gedit | grep -v grep | wc -l
echo -n "number of temp.sh zombies is ">> $tlog;ps aux | grep tparse |grep -v gedit | grep -v grep | wc -l>> $tlog
ps aux | grep $zombie |grep -v gedit | tr -s [:space:] |cut -d " " -f 2 |xargs -I xxx kill -9 xxx 2>/dev/null
ps aux | grep $zombie |grep -v gedit | tr -s [:space:] |cut -d " " -f 2 |xargs -I xxx kill -9 xxx 2>/dev/null
# ps aux | grep mtsp |grep -v gedit | tr -s [:space:] |cut -d " " -f 2 |xargs -I xxx kill -9 xxx 2>/dev/null
echo -n "Now there are this number of zombies  ">> $tlog;ps aux | grep tparse |grep -v gedit | grep -v grep | wc -l>> $tlog
} # Test: itemp.sh kz
#
# 
#*######################################STANDARD AND MAYBE USEFUL FUNCTIONS BELOW
#
#
#
#* function tarry   - A simple tarry...
function tarry(){
   # -t sets time
   # read -t $pt -p "$*" ans
   read -p "Hit enter to continue..." ans
   echo $ans
}
#
#* function pause    - Allows many ways to tarry...
function pause(){
#debug echo "Vairables in Pause are: "
#debug echo $#"     "$-e 1"    "$ARGS 

   # -t sets time
   # read -t $var3 -p "$*" ans$(ls -1 | grep backup |wc -l)
case "$ARGS" in
   "6") read -t $time -p "$prompt";;
   "5") read -p "$prompt";;
   "1") read;;
esac # end of choices
   # echo $ans
} # TESTS: mfurmon.sh pause; mfurmon.sh pause "Testing wait"; mfurmon.sh pause 3 "Testing 1,2,3";
#
#* function fwatch - Watches the end of a file indefinitely
function fwatch(){
#debug echo $#"     "$var2"    "$ARGS
 watch tail -20 $var2
} # Test: mfurmon.sh fwatch  var/log/messages
#
#
#* function cleanup  - Cleanup function deletes all the day directories in current directory
function cleanup(){
# debug echo "This is the clean up function"
# debug echo $#"     "$var1"     "$var2"     "$var3"    "$ARGS   
# Clean up stuff in logs, note TEST function
#
ilog="/var/www/itemp/logs/itemp.log"
olog="/var/www/otemp/logs/otemp.log"
if [ "$(echo $dtest | tr [:lower:] [:upper:])" == "TEST" ];
then
	echo "I was only kidding! We would have erased these 2 logs:" 
	ls -alt $ilog
	ls -alt $olog
	exit 1  
fi
echo "we are cleaning these up now:"
ls -alt $ilog
ls -alt $olog
tarry
echo "Resetting: "$ilog
rm -rf $ilog; touch $ilog;chmod 777 $ilog
echo "Resetting: "$olog
rm -rf $olog; touch $olog;chmod 777 $olog
} # Test: mfurmon.sh cleanup
#
#
#*###################################### MAIN ENTRY POINT AND COMPOUND CASE
#debug echo "mfurmon.sh version "$version" starts"
#debug echo $#"     "$1"    "$2"    "$3"    "$ARGS #debug
#
#* Evaluator Routine
# Note the evaluator allows for many cases and error checking...
# ARGS=$#         # carries the number of args into the functions...
if [ "$#" -eq "1" ] && [ "$1" = "cit"     ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "cot"     ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "itemp"   ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "otemp"   ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "kz"      ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "nz"      ]; then ARGS="1"; fi
if [ "$#" -eq "2" ] && [ "$1" = "kz"      ]; then ARGS="2"; fi
if [ "$#" -eq "2" ] && [ "$1" = "nz"      ]; then ARGS="2"; fi
if [ "$#" -eq "2" ] && [ "$1" = "testo"   ]; then ARGS="2"; fi
if [ "$#" -eq "1" ] && [ "$1" = "testo"   ]; then ARGS="0"; fi
if [ "$#" -eq "2" ] && [ "$1" = "testi"   ]; then ARGS="2"; fi
if [ "$#" -eq "1" ] && [ "$1" = "testi"   ]; then ARGS="0"; fi
if [ "$#" -eq "1" ] && [ "$1" = "help"    ]; then ARGS="9"; fi
if [ "$#" -eq "1" ] && [ "$1" = "status"  ]; then ARGS="1"; fi
if [ "$#" -eq "2" ] && [ "$1" = "tempf"   ]; then ARGS="2"; fi
if [ "$#" -eq "2" ] && [ "$1" = "tempc"   ]; then ARGS="2"; fi
if [ "$#" -eq "1" ] && [ "$1" = "spause"  ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "pause"   ]; then ARGS="1"; fi
if [ "$#" -eq "2" ] && [ "$1" = "pause"   ]; then ARGS="5"; fi
if [ "$#" -eq "3" ] && [ "$1" = "pause"   ]; then ARGS="6"; fi
if [ "$#" -eq "2" ] && [ "$1" = "waiw"    ]; then ARGS="2"; fi
if [ "$#" -eq "3" ] && [ "$1" = "waiw"    ]; then ARGS="3"; fi
if [ "$#" -eq "1" ] && [ "$1" = "cleanup" ]; then ARGS="1"; fi
if [ "$#" -eq "2" ] && [ "$1" = "cleanup" ]; then ARGS="2"; fi
if [ "$#" -eq "3" ] && [ "$1" = "cleanup" ]; then ARGS="3"; fi
if [ "$#" -eq "1" ] && [ "$1" = "dummy"   ]; then ARGS="1"; fi
if [ "$#" -eq "1" ] && [ "$1" = "help"    ]; then ARGS="9"; fi
# this tests the evaluator...
#debug echo $#"     "$1"    "$2"    "$3"    "$ARGS 
# typical cases, be careful to make your own...
case "$ARGS" in
    "0") clear; cat $0 | grep '^## ' | sed -e 's/##//'; exit 1;; # got nothing, display help and go
    "1") $1 ;;                                              	 # run the command
    "2") var2=$2;  $1 ;;                                    	 # run the command with an argument
    "3") var3=$3; var2=$2;  $1 ;;                           	 # run the command with two arguments
    "4") var4=$4; var3=$3; var2=$2;  $1 ;;                       # run the command with three arguments
      *) clear; cat $0 | grep '^## '| sed -e 's/##//'; exit 1;;  # Anything else run help and exit...
esac # End main loop. To TEST:
#
# echo " ";
#debug echo "mfurmon.sh stops" # >> /var/www/itemp/logs/itemp.log #debug
#  That's all folks!!
# Junk shop
#     if [ "$#" -eq "3" ] && [ "$1" = "get" ] && [ "$2" = "all"  ];  then ARGS="7"; fi
#    "2") secs=$2;  while read line ; do $1; done;;             # read from a file and process
#     *) clear; cat $0 | grep '^## ' | sed -e 's/##//'; exit 1;;
#* restore environment
cd $S
#d export TERM=$tset

