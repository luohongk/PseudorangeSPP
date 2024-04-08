'''
Author: Hongkun Luo
Date: 2024-04-07 19:54:53
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
'''

from readfile import ReadFile
from satelite import Satelite
from position import Position


def main():
    # 在这里编写你的程序逻辑
    print("这是入口函数")

    File = ["./data/abpo3340.23o", "./data/al2h3340.23n"]

    readfile = ReadFile(File)

    print("粗略坐标")
    print(ReadFile.ApproxPos)

    readfile.CaculateSatelites()

    for i in range(40):
        print(readfile.Pos[i], readfile.PosName[i], readfile.Time[i])

    print("打印完成")

    # 实例化定位对象
    position = Position(readfile.SateliteObservation, readfile.PosName, readfile.Time, readfile.SateliteClockCorrect)
    position.MatchObservationAndCaculate()


if __name__ == "__main__":
    main()
