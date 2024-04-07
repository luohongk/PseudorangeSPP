'''
Author: Hongkun Luo
Date: 2024-04-07 19:54:53
LastEditors: Hongkun Luo
Description: 

Hongkun Luo
'''

from readfile import ReadFile
from satelite import Satelite
def main():
    # 在这里编写你的程序逻辑
    print("这是入口函数")
    
    File=["./data/abpo3340.23o","./data/al2h3340.23n"]

    readfile=ReadFile(File)

    print(readfile.ApproxPos)
    
    for i in range(20):
        print(readfile.Satelites[i].)
            
          





if __name__ == "__main__":
    main()