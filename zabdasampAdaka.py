#!/usr/bin/env python3

import sys

# ---------------- #
# global variables #
# ---------------- #

# the text buffer: a list of lines
txtdata=[]
# name of current file being edited
currfn='tmp'


# --------- #
# functions #
# --------- #

# read file data into buffer
def readfiledata(fnm):
  global txtdata
  global currfn
  currfn=fnm
  with open(fnm) as f:
    print('[info] populating buffer...')
    txtdata=f.readlines()

# write buffer data into file
def writefiledata(fnm):
  global txtdata
  with open(fnm,'w') as f:
    print('[info] writing buffer to disk...')
    f.writelines(txtdata)

# display buffer
def printbuffer():
  print('buffer:[')
  i=0
  for line in txtdata:
    print('%3d> %s'%(i,line),end='')
    i+=1
  print(']')

# append line after adding newline char
def addline(s,end='\n'):
  global txtdata
  print('[info] appending line to buffer...')
  txtdata.append(s+end)

# remove line number (indexed array style)
def deleteline(lnum):
  global txtdata
  print('[info] deleting line number: '+str(lnum))
  print('[info] line contents: '+txtdata[lnum])
  del txtdata[lnum]

# insert line at line number (indexed array style)
def insertline(lnum,s,end='\n'):
  global txtdata
  print('[info] inserting line at: '+str(lnum))
  txtdata.insert(lnum,s+end)

# duplicate line n times
def duplicateline(lnum,ntimes):
  global txtdata
  print('[info] duplicating line number %d, %d times'%(lnum,ntimes))
  for x in range(ntimes):
    insertline(lnum,txtdata[lnum],end='')


# --------- #
# main flow #
# --------- #
if len(sys.argv)==2:
  currfn=sys.argv[1]
  readfiledata(currfn)

while True:
  uin=input('|$| ')
  parts=uin.split(' ')
  ch=parts[0]
  dt=parts[1:]
  if ch=='b':
    printbuffer()
  elif ch=='-':
    usrinp=dt
    addline(usrinp)
  elif ch==21:
    linum=int(input('line number: '))
    insline=input('line: ')
    insertline(linum,insline)
  elif ch==30:
    linum=int(input('line number: '))
    deleteline(linum)
  elif ch==40:
    print('[WIP] TODO')
  elif ch==41:
    linum=int(input('line number: '))
    duptimes=int(input('duplicates: '))
    duplicateline(linum,duptimes)
  elif ch==50:
    writefiledata(currfn)
  elif ch==51:
    wfn=input('file name: ')
    writefiledata(wfn)
  elif ch==60:
    rfn=input('enter file name: ')
    readfiledata(rfn)
  elif ch==0:
    print('bye!')
    break

