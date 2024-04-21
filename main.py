"""
Author: Hongkun Luo
Date: 2024-04-07 19:54:53
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
"""

from readfile import ReadFile
from satelite import Satelite
from position import Position


def main():
    # 在这里编写你的程序逻辑
    print("这是入口函数")

    # 定义O文件与N文件的路径
    File = ["./data/abpo3340.23o", "./data/al2h3340.23n"]

    # 实例化ReadFile类，得到readfile对象，实例化过程中对文件进行读取
    readfile = ReadFile(File)

    # 输出读取结果，粗略坐标值
    print("粗略坐标")
    print(ReadFile.ApproxPos)

    # 计算N文件参考时刻的卫星位置，我自己核对一下数据算对了没有
    readfile.CaculateSatelites()

    # 输出读取的N文件读取的结果，并且分门别类存成列表
    for i in range(40):
        print(readfile.Pos[i], readfile.PosName[i], readfile.Time[i])

    print("打印完成")

    # 实例化定位类，构造定位对象
    position = Position(
        readfile.SateliteObservation,
        readfile.PosName,
        readfile.Time,
        readfile.SateliteClockCorrect,
    )

    # 定位对象调用计算函数进行平差坐标计算
    position.MatchObservationAndCaculate()


if __name__ == "__main__":
    # 主函数程序入口
    main()
