"""
Author: Hongkun Luo
Date: 2024-04-07 20:43:56
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
"""

from readfile import ReadFile
from satelite import Satelite
import datetime
import numpy as np


class Position:

    def __init__(self, SateliteObservation, SateliteName, Time, SateliteClockCorrect):

        # 卫星索引列表
        self.SateliteObservation = SateliteObservation
        self.SateliteName = SateliteName
        self.Time = Time
        self.SateliteClockCorrect = SateliteClockCorrect

        # 获取O文件的数据，这就包括文本数据以及END OF Header所在的行
        self.Lines = ReadFile.OLines
        self.OHeaderLastLine = ReadFile.OHeaderLastLine

        # 获取坐标粗略值
        self.ApproxPos = ReadFile.ApproxPos

    def GenerateObs(self):
        return 0

    def MatchObservationAndCaculate(self):
        # line用于临时存储的行数
        line = self.Lines[self.OHeaderLastLine]

        # 这个变量用于标记读取的行数
        NReadLine = self.OHeaderLastLine

        while line != "":

            # 这里表示从O文件获取当前观测时间
            obs_time = [None] * 6
            obs_time[0] = int((line[1:3]).strip()) + 2000
            obs_time[1] = int((line[4:6]).strip())
            obs_time[2] = int((line[7:9]).strip())
            obs_time[3] = int((line[10:12]).strip())
            obs_time[4] = int((line[13:15]).strip())
            obs_time[5] = int((line[17:18]).strip())

            # 这里表示当前观测时间下，有多少个卫星观测值
            num_sat = int(line[30:32])

            # 这里希望获取当前观测时间下,卫星名称列表在O文件所占有的行数
            if num_sat % 12 == 0:
                n = int(num_sat / 12)
            else:
                n = int((num_sat / 12)) + 1

            str = ""

            for j in range(n):
                str = str + self.Lines[NReadLine + j][32:68].strip()
            # 这里表示当前观测时间下，卫星的名称列表
            obs_sat_PRN = []
            for k in range(num_sat):
                obs_sat_PRN.append(str[k * 3 : k * 3 + 3])

            NReadLine = NReadLine + n

            # 接下来获取伪距列表
            ObsPseudorange = []
            for j in range(NReadLine, NReadLine + 2 * num_sat, 2):
                line = self.Lines[j]

                # 获取伪距
                if line[34:46].strip() == "":
                    Pseudorange = 0
                else:
                    Pseudorange = float(line[34:46])

                ObsPseudorange.append(Pseudorange)

            # 直接计算当前位置下的测站位置并且打印
            SatLiteXYZ = self.MatchToSatlite(obs_time, obs_sat_PRN)

            # print(ObsPseudorange)
            # print(SatLiteXYZ)

            # 进行非线性最小二乘，平差计算地面坐标
            a = self.SolutionLeastSquares(
                ObsPseudorange, SatLiteXYZ, ReadFile.ApproxPos
            )

            # 更新读取的行数
            NReadLine = NReadLine + 2 * num_sat

            # 更新读取的内容
            line = self.Lines[NReadLine]

    def MatchToSatlite(self, ObsTime, ObsSatPrn):

        # 匹配结果保存

        SatLiteXYZ = []
        # 进行卫星匹配
        # 遍历观测值文件某个时间下的卫星编号
        # AfterMatch
        for index, SatPRN in enumerate(ObsSatPrn):
            # 遍历卫星参考时刻的PRN号

            #   这四个元素的说明，前三个元素保存卫星坐标，后一个保存是否匹配上的一个标签值,卫星钟差
            TemXYZ = [None] * 5

            TimeDiff = []
            for index1, SatPRN1 in enumerate(self.SateliteName):
                if SatPRN == SatPRN1:
                    # 计算时间差

                    TimeDiff.append(
                        self.CaculateTimeDifference(ObsTime, self.Time[index1])
                    )
                else:
                    # 这里设置三天所有的秒数，保证足够大，找最小值的之后不找到就可以了
                    TimeDiff.append(2592000)

            #     没有匹配上的判断
            NotMatch = all(x == 2592000 for x in TimeDiff)
            if NotMatch == True:
                TemXYZ[0] = 0
                TemXYZ[1] = 0
                TemXYZ[2] = 0
                TemXYZ[3] = 0
                TemXYZ[4] = 0
            else:
                # 寻找最小时间差的索引
                MinTime = min(TimeDiff)
                MinTimeindex = TimeDiff.index(MinTime)

                # 计算这个最小索引卫星的坐标
                satelite = Satelite(
                    self.SateliteName[MinTimeindex],
                    self.Time[MinTimeindex],
                    self.SateliteClockCorrect[MinTimeindex],
                    self.SateliteObservation[MinTimeindex],
                )

                # 这里需要传入观测时间，计算卫星坐标
                satelite.InitPositionOfSat(ObsTime)
                TemXYZ[0] = satelite.X
                TemXYZ[1] = satelite.Y
                TemXYZ[2] = satelite.Z
                TemXYZ[3] = 1
                TemXYZ[4] = satelite.Delta_T
            SatLiteXYZ.append(TemXYZ)
        return SatLiteXYZ

        # 计算伪距所对应的卫星的位置

    def CaculateTimeDifference(self, Time1, Time2):
        time1 = datetime.datetime(
            Time1[0], Time1[1], Time1[2], Time1[3], Time1[4], int(Time1[5])
        )
        time2 = datetime.datetime(
            Time2[0], Time2[1], Time2[2], Time2[3], Time2[4], int(Time2[5])
        )
        diff = time2 - time1
        seconds = diff.total_seconds()
        return seconds

    # 最小二乘算法求解
    def SolutionLeastSquares(self, ObsPseudorange, SatLiteXYZ, ApproxPos):
        # 判断匹配上的伪距是否多于四个，因为最小二乘至少要四个观测方程，求解地面坐标，求解接收机钟差

        t = 0
        # 平差矩阵的存储
        B = []
        L = []

        # 获取到的卫星数目，也就是当前时刻能够匹配上的伪距数目
        SizeSatLiteXYZ = len(SatLiteXYZ)

        # 看看观测方程的个数，因为这里面，至少要有四个观测方程才能求解四个参数
        for i in range(SizeSatLiteXYZ):
            t = t + SatLiteXYZ[i][3]
        # 如果观测方程的数目不够，就不进行平差计算
        if t < 4:
            print("无法进行平差计算")
            return 0
        else:
            # 进行平差计算
            for k in range(SizeSatLiteXYZ):

                # 跳过没有匹配上的卫星
                if SatLiteXYZ[k][3] == 0:
                    continue

                # 结束标志
                if k == SizeSatLiteXYZ - 1:
                    break
                # 计算P0
                P0 = np.sqrt(
                    np.square(SatLiteXYZ[k][0] - ApproxPos[0])
                    + np.square(SatLiteXYZ[k][1] - ApproxPos[1])
                    + np.square(SatLiteXYZ[k][2] - ApproxPos[2])
                )

                # 计算Bj矩阵每一行的数据
                TemB0 = -1 * (SatLiteXYZ[k][0] - ApproxPos[0]) / P0
                TemB1 = -1 * (SatLiteXYZ[k][1] - ApproxPos[1]) / P0
                TemB2 = -1 * (SatLiteXYZ[k][2] - ApproxPos[2]) / P0
                c = 3 * (10**8)
                TemB3 = 1

                TemBRol = [TemB0, TemB1, TemB2, TemB3]
                B.append(TemBRol)

                # 计算L矩阵每一行的数据
                TemLRol = ObsPseudorange[k] - P0 + c * SatLiteXYZ[k][4]
                L.append(TemLRol)

            # 求解坐标改正量
            ArrayB = np.array(B)
            ArrayL = np.array(L)

            # 进行间接公式进行平差计算
            x = np.linalg.inv(np.transpose(ArrayB) @ ArrayB) @ (
                np.transpose(ArrayB) @ ArrayL
            )
            # 平差后的坐标存储容器
            PosXYZ = np.array(ApproxPos)
            print(
                "平差后的X坐标:",
                PosXYZ[0] + x[0],
                "平差后的Y坐标:",
                PosXYZ[1] + x[1],
                "平差后的Z坐标:",
                PosXYZ[2] + x[2],
            )

            # 这里可以加入一个迭代q

            return 1
