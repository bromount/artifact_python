'''
Created on 30-Jul-2015

@author: bromount
'''
#!/usr/bin/python

import subprocess
import re

# Get process info
ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0]
vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0]

# Iterate processes
processLines = ps.split('\n')
sep = re.compile('[\s]+')
rssTotal = 0 # kB
for row in range(1,len(processLines)):
    rowText = processLines[row].strip()
    rowElements = sep.split(rowText)
    try:
        rss = float(rowElements[0]) * 1024
    except:
        rss = 0 # ignore...
    rssTotal += rss

# Process vm_stat
vmLines = vm.split('\n')
sep = re.compile(':[\s]+')
vm_stats = {}
for row in range(1,len(vmLines)-2):
    rowText = vmLines[row].strip()
    rowElements = sep.split(rowText)
    vm_stats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

print 'Wired Memory:\t\t%d MB' % ( vm_stats["Pages wired down"]/1024/1024 )
print 'Active Memory:\t\t%d MB' % ( vm_stats["Pages active"]/1024/1024 )
print 'Inactive Memory:\t%d MB' % ( vm_stats["Pages inactive"]/1024/1024 )
print 'Free Memory:\t\t%d MB' % ( vm_stats["Pages free"]/1024/1024 )
print 'Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 )