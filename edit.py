#!/usr/local/bin/python

import ConfigParser
import cgi, cgitb
import funcs

cgitb.enable()
form = cgi.FieldStorage()

dndinf = funcs.holla_at_config(funcs.PATH_TO_DA_CONFIG)
if 'recur' in form.keys():
    for key in form.keys():
        check = key.split('-')
        if len(check) > 1:
            dndinf.set(check[0], check[1], value=form[key].value)
    dndinf.write(open(funcs.PATH_TO_DA_CONFIG, 'wb'))

keys, conf_table = funcs.html_config(dndinf, 'displayAvailable')
total_workers = dndinf.getfloat('Workers', 'total')

print 'Content-type: text/html\n\n'

print '''

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>D&amp;D Expense Stuff, Holla</title>
<link href="../favicon.ico" rel="shortcut icon" type="image/x-icon">
<link rel="stylesheet" href="../css/o.css" type="text/css">
<script>
function getIntVal(id)
{
  return parseInt(document.getElementById(id).value);
}

function totalAllWorkers() 
{
  var total = 0;
'''
for key in dndinf.options('Assignments'):
    key = 'Assignments-' + key
    print '  var total = total + getIntVal("' + key + '");'

print '''
  return total;
}

function displayAvailable() 
{
  var el = document.getElementById("availdisp");
  var x = ''' + str(total_workers) + ''' - totalAllWorkers();
  el.innerHTML = "Available: " + x;
}

</script
</head>

<header>
  <h1>Edit config</h1>
</header>

<body>
<form name="conf" action="edit.py" method="POST">
''' + conf_table + '''

<div onload="displayAvailable()" id="availdisp" 
 style="background-color:#D94A38;width:100px;height:20px;padding:10px;">
  Available: -- 
</div>

<input type="hidden" name="recur" value=1>
<input type="submit" value="Continue">
</form>

</body>

</html>

'''

                     

