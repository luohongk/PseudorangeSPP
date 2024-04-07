'''
Author: Hongkun Luo
Date: 2024-04-07 20:04:05
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
'''
from satelite import Satelite
class ReadFile:
    def __init__(self, File):
         
        #  文件路径
         self.oFilePath=File[0]
         self.nFilePath=File[1]

        #  N文件所有行的数据
         self.NLines=ReadFile.ReadNFile(self)

        #  O文件所有行的数据
         self.OLines=ReadFile.ReadOFile(self)

                #  粗略的测站坐标
         self.ApproxPos=[]

        #  O,N文件预处理模块
         self.NHeaderLastLine=ReadFile.PreprocessNFile(self.NLines)
         self.OHeaderLastLine=ReadFile.PreprocessOFile(self,self.OLines)

         self.Satelites=[]
    
    @classmethod
    def GetApproxPos(self):
        return self.ApproxPos
    
    @classmethod
    def GetOLines(self):
        return self.OLines
    
    @classmethod
    def GetOHeaderLastLine(self):
        return self.OHeaderLastLine
    
    @classmethod
    def GetNlines(self):
        return self.NLines
    
    @classmethod
    def GetNHeaderLastLine(self):
        return self.NHeaderLastLine

    def ReadNFile(self):
            with open(self.nFilePath,'r') as file:
              lines=file.readlines()
              return lines
    
    def ReadOFile(self):
        with open(self.oFilePath, 'r') as file:
              lines=file.readlines()
              return lines
    
    def PreprocessNFile(lines):
            
            # 寻找END OF HEADER所在的行
            target_string='END OF HEADER'
            HeadLine=0
            for i,line in enumerate(lines,start=1):
                if target_string in line:
                    HeadLine=i
                    break
            return HeadLine
            # 此处是拓展部分,由于我已经知道我的文件是GPS数据了,就直接命名卫星名字为GXXX
            # 这里可以自己拓展一下
            # if('GPS' in lines[0]):
            #     obs_type='GPS'
    def PreprocessOFile(self,lines):
            ApproxPosComment='APPROX POSITION XYZ'
            for i,line in enumerate(lines,start=1):
                if(ApproxPosComment in line):
                    approx_x=float(line[0:15].strip())
                    approx_y=float(line[15:28].strip())
                    approx_z=float(line[29:42].strip())
                    self.ApproxPos.append(approx_x)
                    self.ApproxPos.append(approx_y)
                    self.ApproxPos.append(approx_z)

            ObsTargetString='END OF HEADER'
            ObsHeaderLine=0

            for i,line in enumerate(lines,start=1):
                if(ObsTargetString in line):
                    obs_HeaderLine=i
                    break       
            return ObsHeaderLine
            

    def CaculateSatelites(self):
         for i in range(self.NHeaderLastLine,len(self.NLines),9):
                # satelite=Satelite(self.NLines[i:i+9])
                line=self.NLines[i]
                num=line[0:2].strip()

                time=[None]*6
                time[0]=int((line[i][1:3]).strip())
                time[1]=int((line[i][4:6]).strip())
                time[2]=int((line[i][7:9]).strip())
                time[3]=int((line[i][10:12]).strip())
                time[4]=int((line[i][13:15]).strip())
                time[5]=int((line[i][17:18]).strip())
                
