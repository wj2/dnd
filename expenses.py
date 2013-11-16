#!/usr/bin/python

import ConfigParser
import warnings 
import random
import sys
import cgi, cgitb

cgitb.enable()
form = cgi.FieldStorage()

PATH_TO_DA_CONFIG = 'villager_assignments'
TYPE_DICT = {1:'fail', 2:'common',3:'common',4:'common',5:'common',6:'common',
             7:'common',8:'common',9:'uncommon',10:'uncommon',11:'uncommon',
             12:'uncommon',13:'rare',14:'rare',15:'very rare',16:'disaster',
             17:'disaster',18:'disaster',19:'disaster',20:'win'}

def dict_of_sect(parsage, sect):
    dictage = {}
    for opt in parsage.options(sect):
        dictage[opt] = parsage.getint(sect, opt)
    
    return dictage

def holla_at_config(path):
    info = ConfigParser.ConfigParser()
    info.read(path)
    print info.sections()
    
    return info    

def tally_expenses(wks, days, inf):
    num_employ = inf['Costs']['employees'] 
    num_player = inf['Costs']['players']
    comfort = inf['Costs']['comfort'] / 4.0 # per week 
    pay = inf['Costs']['employeepay'] / 4.0 # per week

    wks = wks + (days / 7.0)
    return wks * (num_employ * pay
                  + num_player * comfort)

def roll_n_d_x(n, x):
    roll = 0
    for times in xrange(n):
        roll += random.randint(1, x)
    return roll 

def calculate_gains(inf):
    cap_dict = dict_of_sect(inf, 'Capacities')
    alloc_dict = dict_of_sect(inf, 'Assignments')
    max_work = inf.getint('Workers', 'total')
    if max_work < sum(alloc_dict.values()):
        raise ValueError('too many workers allocated')
    elif max_work > sum(alloc_dict.values()):
        warnings.warn('not all workers allocated', UserWarning)
    gain_string = ''
    for key in cap_dict.keys():
        gain_string += key + ': '
        for times in xrange(alloc_dict[key] / cap_dict[key]):
            roll = roll_n_d_x(1, 20)
            result = TYPE_DICT[roll]
            gain_string += result + ' (' + str(roll) + '), '
        gain_string += '\n'
    return gain_string

def do_money(wks, days):
    info = holla_at_config(PATH_TO_DA_CONFIG)
    sect_names = ['Costs', 'Workers', 'Capacities', 'Assignments']
    dndinf = {}
    for name in sect_names:
        dndinf[name] = dict_of_sect(info, name)
    
    expenses = tally_expenses(wks, days, dndinf)    
    gains = calculate_gains(info)

    return 'expenses: ' + str(expenses) + '\n\n' + gains

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

                     
