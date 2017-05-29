import numpy as np


a=np.load('brand_names.npy')

a=a.item()
cnt=2
print 'item {'
print '  name: ' + '"' + 'none_of_the_above' + '"'
print '  label: ' + str(0)
print '  display_name:' + '"' + 'background' + '"'
print '}'
print 'item {'
print '  name: ' + '"' + '__background__' + '"'
print '  label: ' + str(1)
print '  display_name:' + '"' + '__background__' + '"'
print '}'



for keys in a:
    print 'item {'
    print '  name: ' + '"' + keys + '"'
    print '  label: ' + str(cnt)
    print '  display_name:' + '"' + keys + '"'
    print '}'
    cnt=cnt+1
