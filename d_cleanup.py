#!/usr/bin/python

from os.path import getmtime,isdir,isfile
from os import mkdir,listdir,chdir
from datetime import datetime ,timedelta
from shutil import move
import sys
#import pdb

class DirMonthlyClenaup(object):
  def __init__(self,directory):
    self.dir = directory
    chdir(directory)
    self.inner_dirs = [ file for file in listdir(directory) if isdir(file) ]
    self.inner_files = [ file for file in listdir(directory) if isfile(file) ]


  def file_m_date(self,file):
    e_time = getmtime(file)
    dt_obj = datetime.fromtimestamp(e_time)
    d_name = dt_obj.strftime("%Y_%m")
    return (dt_obj , d_name)

  def cleanup(self):
    res = {}
    for file in self.inner_files:
      dobj, dir_name = self.file_m_date(file)
      if dobj <= datetime.now() - timedelta(days=30): 
        if not dir_name in self.inner_dirs:
          mkdir(dir_name)
          self.inner_dirs.append(dir_name)
        res.setdefault(dir_name,[]).append(file)

    if res:
      for k, v in res.items():
        for file2 in v:
          move(file2, k)




if __name__ == "__main__":
  if len(sys.argv) == 2:
    cleanup = DirMonthlyClenaup(sys.argv[1])
    cleanup.cleanup()
  else:
    print "wrong usage"




