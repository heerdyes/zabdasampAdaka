import os
from vinyAsa import *

# abstract repr of a text buffer
class Buf:
  # decorator to check buffer file binding
  def chkbuf(fn):
    def wrappr(self):
      if not self.currfn or self.currfn=='':
        raise Exception('buffer bound to empty file')
      fn(self)
    return wrappr
  
  # usual instance capability routines
  def __init__(self,bufid,fn,vlnd):
    self.txtdata=[]
    self.id=bufid
    self.bindfile(fn)
    self.cursor=[0,0]
    self.vlndist=vlnd
    
  def moverows(self,dln):
    r=self.cursor[0]
    if r+dln>=len(self.txtdata) or r+dln<0:
      print('cannot leap beyond file ending!')
      return -1
    if r+dln<0:
      print('cannot crawl before file beginning!')
      return -1
    self.cursor[0]=r+dln
    c=self.cursor[1]
    if c+1>=len(self.txtdata[self.cursor[0]]):
      self.cursor[1]=len(self.txtdata[self.cursor[0]])-1
    return 0
    
  def movecols(self,dc):
    r,c=self.cursor[0],self.cursor[1]
    if c+dc>=len(self.txtdata[r]):
      print('cannot exceed the number of columns in row %d!'%r)
      return -1
    if c+dc<0:
      print('cannot access columns in the negative realm!')
      return -1
    self.cursor[1]=c+dc
    return 0
    
  def gotolinum(self,linum):
    if linum<0 or linum>=len(self.txtdata):
      print('linum %d beyond limits!'%linum)
      return -1
    self.cursor[0]=linum
    return 0
    
  def gotorc(self,linum,colnum):
    if linum<0 or linum>=len(self.txtdata):
      print('linum %d beyond limits!'%linum)
      return -1
    if colnum<0 or colnum>=len(self.txtdata[linum]):
      print('colnum %d beyond limits!'%colnum)
      return -1
    self.cursor=[linum,colnum]
    return 0
    
  # bind file data into buffer
  def bindfile(self,fnm):
    self.currfn=fnm
    self.loadfile() # reload buffer
    
  # load file bound to buffer
  @chkbuf
  def loadfile(self):
    with open(self.currfn) as f:
      print('[info] populating buffer...')
      self.txtdata=f.readlines()
    
  # persist buffer data into file
  @chkbuf
  def savefile(self):
    with open(self.currfn,'w') as f:
      print('[info] writing buffer to disk...')
      f.writelines(self.txtdata)
      
  # display buffer
  @chkbuf
  def printbuffer(self):
    print('     0    .    10   .    20   .    30   .    40   .    50   .    60   .    70   .    80')
    print('     |    .    |    .    |    .    |    .    |    .    |    .    |    .    |    .    | ')
    print('     ',end='')
    for ic in range(self.cursor[1]):
      print(' ',end='')
    print('v')
    i=0
    for line in self.txtdata:
      if abs(i-self.cursor[0])<=self.vlndist:
        print('%03d%s %s'%(i,'>' if i==self.cursor[0] else ' ',line),end='')
      i+=1
    print()
  
  # append line after adding newline char
  def addline(self,s,end='\n'):
    print('[info] appending line to buffer...')
    self.txtdata.append(s+end)
    return 0
  
  # remove line number (indexed array style)
  def deleteline(self,lnum):
    print('[info] deleting line number: '+str(lnum))
    print('[info] line contents: '+self.txtdata[lnum])
    del self.txtdata[lnum]
    return 0
  
  # insert line at line number (indexed array style)
  def insertline(self,lnum,s,end='\n'):
    print('[info] inserting line at: '+str(lnum))
    self.txtdata.insert(lnum,s+end)
    return 0
  
  # duplicate line n times
  def duplicateline(self,lnum,ntimes):
    print('[info] duplicating line number %d, %d times'%(lnum,ntimes))
    for x in range(ntimes):
      insertline(lnum,self.txtdata[lnum],end='')
    return 0


# abstract repr of the editor
class Ed:
  def __init__(self):
    self.bufs=[]
    self.bufidx=-1
    self.cmdmap={
      'b':self.handle_printbuf,
      'B':self.handle_lsbufs,
      'i':self.handle_insline,
      'd':self.handle_delline,
      'r':self.handle_replines,
      'v':self.handle_gotonxtln,
      '^':self.handle_gotoprvln,
      '>':self.handle_gotonxtch,
      '<':self.handle_gotoprvch,
      ':':self.handle_gotorc,
      'w':self.handle_save,
      'W':self.handle_saveas,
      's':self.handle_selbuf,
      'o':self.handle_open,
      'h':self.handle_help,
      'l':self.handle_ls,
      'x':self.handle_bye
    }
    
  # --- editor methods --- #
  def showhelp(self):
    print('--- buffer commands ---')
    print('  b -> display buffer')
    print('  B -> list buffers')
    print('  s <bid> -> select buffer <bufid>')
    print('  w -> save buffer to current file')
    print('  W <fn> -> save buffer as <filename>')
    print('  o <fn> -> open file <filename>')
    print()
    print('--- editing commands ---')
    print('  i <ln> -> insert line at <linum>')
    print('  d <ln> -> delete line at <linum>')
    print('  r <ln> <n> -> repeat line at <linum> <n> times')
    print('  v -> move cursor to next line')
    print('  ^ -> move cursor to prev line')
    print('  < -> move cursor to prev char')
    print('  > -> move cursor to next char')
    print('  : -> move cursor to <rownum> <colnum>')
    print()
    print('--- system commands ---')
    print('  h -> show this help menu')
    print('  l -> ls current dir')
    print('  x -> bye')
    
  def lsbufs(self):
    print('--- active buffers ---')
    for buf in self.bufs:
      print('[%s%d] %s'%('*' if self.bufidx==buf.id else '',buf.id,buf.currfn))
    print()
    
  def curbuf(self):
    if self.bufidx==-1 and len(self.bufs)==0:
      print('no bufs present!')
      raise Exception('no bufs present!')
    if self.bufidx==-1 and len(self.bufs)>0:
      print('bufs present but none selected! selecting 0th buf...')
      self.bufidx=0
    return self.bufs[self.bufidx]
  
  def hasbufs(self):
    return len(self.bufs)>0
  
  def mkbuf(self,fn):
    b=Buf(len(self.bufs),fn,VIEW_LINE_DIST)
    self.bufs.append(b)
    if self.bufidx==-1:
      self.bufidx=0
    
  def selbuf(self,bn):
    if bn<0 or bn>=len(self.bufs):
      raise Exception('buffer selected out of bounds!')
    self.bufidx=bn
    print('active buffer: [%d] %s'%(self.bufidx,self.bufs[self.bufidx].currfn))
  
  # --- end editor methods --- #
  
  # --- command shell handlers --- #
  def handle_printbuf(self,args):
    if self.hasbufs():
      self.curbuf().printbuffer()
    else:
      print('no buffers present!')
  
  def handle_lsbufs(self,args):
    self.lsbufs()
  
  def handle_ls(self,args):
    for fn in os.listdir():
      print(fn)
    print()
    
  def handle_insline(self,args):
    if len(args)!=1:
      print('i requires <linum> as arg!')
      return
    linum=int(args[0])
    insline=input('line: ')
    err=self.curbuf().insertline(linum,insline)
    if err==0 and IMMEDIATE_VIEW:
      self.curbuf().printbuffer()
  
  def handle_delline(self,args):
    if len(args)!=1:
      print('d requires <linum> as arg!')
      return
    linum=int(args[0])
    err=self.curbuf().deleteline(linum)
    if err==0 and IMMEDIATE_VIEW:
      self.curbuf().printbuffer()
    
  def handle_replines(self,args):
    if len(args)!=2:
      print('r requires <ln> and <n> as args!')
      return
    linum=int(args[0])
    duptimes=int(args[1])
    err=self.curbuf().duplicateline(linum,duptimes)
    if err==0 and IMMEDIATE_VIEW:
      self.curbuf().printbuffer()
    
  def handle_gotonxtln(self,args):
    cb=self.curbuf()
    nln=1
    if len(args)>=1:
      nln=int(args[0])
    err=cb.moverows(nln)
    if IMMEDIATE_VIEW and err==0:
      cb.printbuffer()
    
  def handle_gotoprvln(self,args):
    cb=self.curbuf()
    nln=1
    if len(args)>=1:
      nln=int(args[0])
    err=cb.moverows(-nln)
    if IMMEDIATE_VIEW and err==0:
      cb.printbuffer()
  
  def handle_gotonxtch(self,args):
    cb=self.curbuf()
    nch=1
    if len(args)>=1:
      nch=int(args[0])
    err=cb.movecols(nch)
    if IMMEDIATE_VIEW and err==0:
      cb.printbuffer()
  
  def handle_gotoprvch(self,args):
    cb=self.curbuf()
    nch=1
    if len(args)>=1:
      nch=int(args[0])
    err=cb.movecols(-nch)
    if IMMEDIATE_VIEW and err==0:
      cb.printbuffer()
  
  def handle_gotorc(self,args):
    if len(args)!=2:
      print('rc requires <rownum> <colnum> as args!')
      return
    r,c=int(args[0]),int(args[1])
    err=self.curbuf().gotorc(r,c)
    if err==0 and IMMEDIATE_VIEW:
      self.curbuf().printbuffer()
    
  def handle_save(self,args):
    self.curbuf().savefile()
    
  def handle_saveas(self,args):
    if len(args)!=1:
      print('save_as needs 1 argument: <filename>')
      return
    cbuf=self.curbuf()
    cbuf.bindfile(args[0])
    cbuf.savefile()
    
  def handle_open(self,args):
    if len(args)!=1:
      print('[cmdsh] read file requires 1 parameter: filename')
      return
    rfn=args[0]
    if not os.path.exists(rfn):
      with open(rfn,'w') as fp:
        pass
    self.mkbuf(rfn)
    
  def handle_selbuf(self,args):
    if len(args)!=1:
      print('[cmdsh] select buffer requires 1 parameter: bufid')
      return
    bid=int(args[0])
    self.selbuf(bid)
    
  def handle_help(self,args):
    self.showhelp()
    
  def handle_bye(self,args):
    print('bye!')
    exit(0)
  
  # --- end command shell handlers --- #
  
  # the shell itself
  def cmdsh(self):
    while True:
      uin=input('|$| ')
      parts=uin.split(' ')
      ch=parts[0]
      dt=parts[1:]
      self.cmdmap[ch](dt)
