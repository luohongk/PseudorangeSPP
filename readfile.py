'''
Author: Hongkun Luo
Date: 2024-04-07 20:04:05
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
'''
class ReadFile:
    def __init__(self, File[2]):
        self.oFilePath = File[0]
        self.nFilePath = File[1]


    def ReadNFile(self):
            with open(self.nFilePath,'r') as file:
              lines=file.readlines()
              return lines
    
    def ReadOFile(self):
        with open(self.oFilePath, 'r') as file:
              lines=file.readlines()
              return lines
    
    def PreprocessNFile(lines):
            target_string='END OF HEADER'
            HeadLine=0
            for i,line in enumerate(lines,start=1):
                if target_string in line:
                    HeadLine=i
                    break
    