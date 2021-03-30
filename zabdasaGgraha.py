# abstract repr of a text buffer
class Buf:
  def __init__(self,bufid,fn):
    self.txtdata=[]
    self.currfn=fn
    self.id=bufid
    
  # read file data into buffer
  def readfiledata(self,fnm):
    self.currfn=fnm
    with open(fnm) as f:
      print('[info] populating buffer...')
      self.txtdata=f.readlines()
      
  # write buffer data into file
  def writefiledata(self,fnm):
    with open(fnm,'w') as f:
      print('[info] writing buffer to disk...')
      f.writelines(txtdata)
      
  # display buffer
  def printbuffer(self):
    print('buffer:[')
    i=0
    for line in self.txtdata:
      print('%3d> %s'%(i,line),end='')
      i+=1
    print(']')
  
  # append line after adding newline char
  def addline(self,s,end='\n'):
    print('[info] appending line to buffer...')
    self.txtdata.append(s+end)
  
  # remove line number (indexed array style)
  def deleteline(self,lnum):
    print('[info] deleting line number: '+str(lnum))
    print('[info] line contents: '+self.txtdata[lnum])
    del self.txtdata[lnum]
  
  # insert line at line number (indexed array style)
  def insertline(self,lnum,s,end='\n'):
    print('[info] inserting line at: '+str(lnum))
    self.txtdata.insert(lnum,s+end)
  
  # duplicate line n times
  def duplicateline(self,lnum,ntimes):
    print('[info] duplicating line number %d, %d times'%(lnum,ntimes))
    for x in range(ntimes):
      insertline(lnum,self.txtdata[lnum],end='')


# abstract repr of the editor
class Ed:
  def __init__(self):
    self.bufs=[]
    self.bufidx=-1
    
  def lsbufs(self):
    print('[active buffers]')
    for buf in self.bufs:
      print('[%s] %s'%(buf.id,buf.currfn))
    print()
    
  def curbuf(self):
    if self.bufidx==-1 and len(self.bufs)==0:
      print('no bufs present!')
      return
    if self.bufidx==-1 and len(self.bufs)>0:
      print('bufs present but none selected! selecting 0th buf...')
      self.bufidx=0
    return self.bufs[self.bufidx]
  
  def mkbuf(self,fn):
    b=Buf(len(self.bufs),fn)
    self.bufs.append(b)
    if self.bufidx==-1:
      self.bufidx=0
  
  def showhelp(self):
    print('  b -> display buffer')
    print('  i -> insert line at <linum>')
    print('  d -> delete line at <linum>')
    print('  r -> repeat line at <linum> <n> times')
    print('  w -> save buffer to current file')
    print('  W -> save buffer as <filename>')
    print('  s -> select buffer <bufid>')
    print('  o -> open file <filename>')
    print('  h -> show this help menu')
    print('  x -> bye')
    
  def cmdsh(self):
    while True:
      uin=input('|$| ')
      parts=uin.split(' ')
      ch=parts[0]
      dt=parts[1:]
      if ch=='b':
        self.curbuf().printbuffer()
      elif ch=='i':
        linum=int(input('line number: '))
        insline=input('line: ')
        self.curbuf().insertline(linum,insline)
      elif ch=='d':
        linum=int(input('line number: '))
        self.curbuf().deleteline(linum)
      elif ch=='r':
        linum=int(input('line number: '))
        duptimes=int(input('duplicates: '))
        self.curbuf().duplicateline(linum,duptimes)
      elif ch=='w':
        self.curbuf().writefiledata(currfn)
      elif ch=='W':
        wfn=input('file name: ')
        self.curbuf().writefiledata(wfn)
      elif ch=='o':
        rfn=input('enter file name: ')
        self.curbuf().readfiledata(rfn)
      elif ch=='h':
        self.showhelp()
      elif ch=='l':
        self.lsbufs()
      elif ch=='x':
        print('bye!')
        break

