#!/bin/bash
# pflint Fri 17 May 2013 07:49:14 AM EDT 
# packs html into String
#
# the following evaluates the string... go to line 58 for more stuff...
read -d '' String <<"EOF"
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<meta http-equiv="refresh" content="10;url=http://10.0.1.45/furmon/out.html">
<html><head>

<meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
<title>Pellergy Control For Furmon Site</title>


</head><body>
<img style="width: 847px; height: 642px;" alt="Drawing of control plate should be here" src="http://docbox.flint.com/%7Eflint/furmon/Pellergy_Control_blank_plate.png">
<table style="position: relative; z-index: 1; left: 120px; top: -510px; width: 606px; height: 179px;" cellpadding="2" cellspacing="2">

<tbody>
<tr>
<td colspan="2" rowspan="1" style="position: relative; width: 305px;"><big> Purging </big><br>
</td>
<td colspan="3" rowspan="1" style="position: relative; width: 257px;"><big> 1000 </big><br>
</td>
</tr>
<tr>
<td style="position: relative; width: 150px;">T <br>
</td>
<td style="position: relative; width: 150px;">2 <br>
</td>
<td style="position: relative; width: 140px;">345 &#8457 <br>
</td>
<td style="position: relative; width: 140px;">F <br>
</td>
<td style="position: relative; width: 140px;">10<br>
</td>
</tr>
<tr>
<td colspan="2" rowspan="1" style="position: relative; width: 103px;">No Alarm<br>
</td>
<td colspan="3" rowspan="1" style="position: relative; width: 257px;">All is well<br>
</td>
</tr>
<tr>
<td style="position: absolute; left: 180px; top: 340px;">Param<br>
</td>
<td style="position: absolute; left: 340px; top: 340px;">Test<br>
</td>
<td style="position: absolute; left: 490px; top: 340px;">Enabl<br>
</td>
<td style="position: absolute; left: 640px; top: 340px;">Feed</td>
</tr>
</tbody>
</table>
<br>
<br>
</body></html>
EOF
# echo "this is the string"
echo "$String" > in.html
rm -rf outpcp.html
newrd1=$1
newrd2=$2
t11="test 1,1"
t12="test 1,2"
#
# very last line erases all extra test files
# cat start.html |sed -r "s|test .,.|  |g" > outpcp.html;cp outpcp.html start.html
change="${String/Purging/banana}"
String="${change/1000/1001}"
echo "${String/Purging/banana}" > out.html
echo "the difference between these strings is"
diff in.html out.html
sleep 5
firefox 2>/dev/null out.html
