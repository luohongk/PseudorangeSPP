'''
Author: Hongkun Luo
Date: 2024-04-07 20:43:56
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
'''
from readfile import ReadFile
class Position:

     def __init__(self):
          self.ApproxPos=ReadFile.GetApproxPos()
          self.OLines=ReadFile.GetOLines()
          self.OHeaderLastLine=ReadFile.GetOHeaderLastLine()

          self.Time = [ [None] * 6 for _ in range(6) ]
          self.SatliteName=[]

          self.PseudorangeList=[]
     
     def GenerateObs(self):
          return 0