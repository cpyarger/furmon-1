#!/bin/bash
# output an html file
#html <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
#html <meta http-equiv="refresh" content="10;url=http://10.0.1.45/furmon/outpcp.html">
#html <html><head>
#html > outpcp.html
#html   
#html   <meta content="text/html; charset=ISO-8859-1" 
#html http-equiv="content-type">
#html   <title>Pellergy Control For Furmon Site</title>
#html 
#html   
#html </head><body>
#html <img style="width: 847px; height: 642px;" alt="Drawing of control plate 
#html should be here" 
#html src="Pellergy_Control_For_Furmon_Site_files/Pellergy_Control_blank_plate.png">
#html <table style="position: relative; z-index: 1; left: 250px; top: -500px; 
#html width: 606px; height: 212px;" 1="" cellpadding="2" cellspacing="2">
#html 
#html   <tbody>
#html     <tr>
#html       <td style="position: relative;">test 1,1 </td>
#html       <td style="position: relative;">test 1,2<br>
#html       </td>
#html       <td style="position: relative;">test 1,3<br>
#html       </td>
#html       <td style="position: relative;">test 1,4<br>
#html       </td>
#html     </tr>
#html     <tr>
#html       <td style="position: relative;">test 2,1 <br>
#html       </td>
#html       <td style="position: relative;">test 2,2 <br>
#html       </td>
#html       <td style="position: relative;">test 2,3 <br>
#html       </td>
#html       <td style="position: relative;">test 2,4 <br>
#html       </td>
#html     </tr>
#html     <tr>
#html       <td style="position: relative;">test 3,1<br>
#html       </td>
#html       <td style="position: relative;">test 3,2<br>
#html       </td>
#html       <td style="position: relative;">test 3,3<br>
#html       </td>
#html       <td style="position: relative;">test 3,4<br>
#html       </td>
#html     </tr>
#html     <tr>
#html       <td style="position: relative;">test 4,1<br>
#html       </td>
#html       <td style="position: relative;">test 4,2<br>
#html       </td>
#html       <td style="position: relative;">test 4,3<br> echo $(echo $line |sed "s|test |$newrd |")  >> outpcp.html

#html       </td>
#html       <td style="position: relative;">test 4,4<br>
#html       </td>
#html     </tr>
#html   </tbody>
#html </table>
#html 
#html <br>
#html 
#html <br>
#html 
#html </body></html>
rm -rf outpcp.html
newrd=$1
grep "#html" $0 |cut -c 7-  |while read line; 
do 
 #debug echo $line  >> outpcp.html 
 # echo $(echo $line |sed "s|test |$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 1,1|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 1,2|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 1,3|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 1,4|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 2,1|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 2,2|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 2,3|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 2,4|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 3,1|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 3,2|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 3,3|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 3,4|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 4,1|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 4,2|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 4,3|$newrd |")  >> outpcp.html
 echo $(echo $line |sed "s|test 4,4|$newrd |")  >> outpcp.html
 # had enough?
done
