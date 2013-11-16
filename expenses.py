#!/usr/local/bin/python

import cgi, cgitb

from funcs import do_money

cgitb.enable()
form = cgi.FieldStorage()

wks = int(form['wks'].value)
days = int(form['days'].value)

the_money = do_money(wks, days)

print 'Content-type: text/html\n\n'

print '''

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>D&amp;D Expense Stuff, Holla</title>
<link href="../favicon.ico" rel="shortcut icon" type="image/x-icon">
<link rel="stylesheet" href="../css/o.css" type="text/css">
</head>

<header>
  <h1>Expenses</h1>
</header>

<body>
''' + the_money + '''
</body>

</html>

'''

                     
