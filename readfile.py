"""
Author: Hongkun Luo
Date: 2024-04-07 20:04:05
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
"""

from satelite import Satelite
import numpy as np


class ReadFile:
    # 定义常量成员

    #  粗略的测站坐标
    ApproxPos = [None] * 3

    #  N文件所有行的数据
    NLines = None

    #  O文件所有行的数据
    OLines = None

    # O文件"END OF HEADER"所在的行
    OHeaderLastLine = 0

    # 类的初始化函数
    def __init__(self, File):

        #  文件路径
        self.oFilePath = File[0]
        self.nFilePath = File[1]

        self.OLines_ = self.ReadOFile()
        self.NLines_ = self.ReadNFile()
        self.ApproxPos = []
        #  O,N文件预处理模块
        self.NHeaderLastLine = ReadFile.PreprocessNFile(self.NLines_)
        self.OHeaderLastLine = ReadFile.PreprocessOFile(self, self.OLines_)

        #  常量初始化
        if ReadFile.NLines == None:
            ReadFile.NLines = self.NLines_
        if ReadFile.OLines == None:
            ReadFile.NLines = self.OLines_
        if ReadFile.ApproxPos == [None] * 3:
            ReadFile.ApproxPos = self.ApproxPos

        if ReadFile.OHeaderLastLine == 0:
            ReadFile.OHeaderLastLine = self.OHeaderLastLine

        self.Satelites = []

        # 这个表示卫星的位置，初始化的时候是
        self.Pos = []

        self.PosName = []

        self.Time = []

        self.RefTime = []

        # 钟飘？反正传入的时候传一个含有三个元素的数组就可以
        self.SateliteClockCorrect = []

        # 这个是卫星观测值，用于计算卫星的位置，本项目中是一个6乘4的矩阵
        self.SateliteObservation = []

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
        with open(self.nFilePath, "r") as file:
            lines = file.readlines()
            ReadFile.NLines = lines
            return lines

    def ReadOFile(self):
        with open(self.oFilePath, "r") as file:
            lines = file.readlines()
            ReadFile.OLines = lines
            return lines

    def PreprocessNFile(lines):

        # 寻找END OF HEADER所在的行
        target_string = "END OF HEADER"
        HeadLine = 0

        # 遍历行，如果找到了end of header就记录并且退出
        for i, line in enumerate(lines, start=1):
            if target_string in line:
                HeadLine = i
                break
        return HeadLine
        # 此处是拓展部分,由于我已经知道我的文件是GPS数据了,就直接命名卫星名字为GXXX
        # 这里可以自己拓展一下
        # if('GPS' in lines[0]):
        #     obs_type='GPS'

    # O文件的预处理，进行粗略坐标的读取
    def PreprocessOFile(self, lines):
        ApproxPosComment = "APPROX POSITION XYZ"
        for i, line in enumerate(lines, start=1):
            # 读取粗略坐标
            if ApproxPosComment in line:
                approx_x = float(line[0:15].strip())
                approx_y = float(line[15:28].strip())
                approx_z = float(line[29:42].strip())
                self.ApproxPos.append(approx_x)
                self.ApproxPos.append(approx_y)
                self.ApproxPos.append(approx_z)

        ObsTargetString = "END OF HEADER"
        ObsHeaderLine = 0

        # 寻找END OF HEADER所在的行
        for i, line in enumerate(lines, start=1):
            if ObsTargetString in line:
                ObsHeaderLine = i
                break

        return ObsHeaderLine

    def CaculateSatRefTime(Time):
        return 0

    def CaculateSatelites(self):
        for i in range(self.NHeaderLastLine, len(self.NLines) - 9, 8):

            line = self.NLines[i]
            num = line[0:2].strip()

            time = [None] * 6
            # print(line[i+2])
            time[0] = int((line[3:5]).strip()) + 2000
            time[1] = int((line[6:8]).strip())
            time[2] = int((line[9:11]).strip())
            time[3] = int((line[12:14]).strip())
            time[4] = int((line[15:17]).strip())
            time[5] = float((line[18:22]).strip())

            # 读取卫星钟差改正参数
            time_change = []
            a = float(line[22:37].strip()) * pow(10, int(line[38:41].strip()))
            time_change.append(a)

            b = float(line[41:56].strip()) * pow(10, int(line[57:60].strip()))
            time_change.append(b)

            c = float(line[60:75].strip()) * pow(10, int(line[76:79].strip()))
            time_change.append(c)

            self.SateliteClockCorrect.append(time_change)

            rows = 6
            cols = 4
            matrix = np.zeros((rows, cols))

            # 读取卫星位置计算的参数
            for j in range(0, rows):
                for k in range(0, cols):
                    matrix[j][k] = float(
                        self.NLines[i + 1 + j][3 + 19 * k : 18 + 19 * k]
                    ) * pow(10, int(self.NLines[i + 1 + j][19 + 19 * k : 22 + 19 * k]))

            self.SateliteObservation.append(matrix)

            SateliteName = "G" + str(num)
            # SateliteRefTime=ReadFile.CaculateSatRefTime(time)

            satelite = Satelite(SateliteName, time, time_change, matrix)

            # 这里需要传入观测时间，计算卫星坐标
            satelite.InitPositionOfSat(time)

            self.Pos.append([satelite.X, satelite.Y, satelite.Z])
            self.Time.append(time)
            self.PosName.append(SateliteName)
            # self.RefTime.append(SateliteRefTime)

            self.Satelites.append(satelite)
