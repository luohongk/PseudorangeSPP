<!--
 * @Author: Hongkun Luo
 * @Date: 2024-04-08 01:27:27
 * @LastEditors: Hongkun Luo
 * @Description: 
 * 
 * Hongkun Luo
-->

# PseudorangeSPP

本项目为GNSS伪距单点定位python面向对象的版本

## 说明

* 如果代码有问题的地方或者有疑问的地方，欢迎联系我，我的github主页有联系方式。
* 代码我还会继续完善，后面会把代码里面的变量命名以及代码注释都写得非常规范。
* 后续我还会在这个代码里面加入一些有趣的东西，敬请期待。

## 运行此项目

```
git clone https://github.com/luohongk/PseudorangeSPP.git
cd PseudorangeSPP
python main.py
```

## 教学视频

<a href="https://www.bilibili.com/video/BV1wZ421q7nD/?spm_id_from=333.999.0.0&vd_source=3d68818394dd7dd28a8186a3fe19fee5">
  <img src="https://s2.loli.net/2024/04/09/XZ3yUkqe2PMtv6w.jpg" alt="B站GNSS伪距单点定位教学">
</a>

## 文件解释

| 文件名      | 文件功能                                     |
| ----------- | -------------------------------------------- |
| main.py     | 主函数，函数入口                             |
| readfile.py | 文件读取类，读与存数据                       |
| satelite.py | 卫星类，用于计算位置位置                     |
| position.py | 定位类，用于进行观测值的匹配以及地面坐标解算 |

## 定位原理

如果通过广播星历以及观测值文件进行单点定位比较困难，需要熟系观测值文件格式以及卫星位置计算的一些算法。可以再加电离层，对流层延迟。

### 对于每一个观测伪距

$$
R=\sqrt{\left( x_s-x_r \right) ^2+\left( y_s-y_r \right) ^2+\left( z_s-z_r \right) ^2}=f\left( x_r,y_r,z_r \right)
$$

### 线性化（泰勒公式）：

$$
R^0+V=\sqrt{\left( x_s-x_{r}^{0} \right) ^2+\left( y_s-y_{r}^{0} \right) ^2+\left( z_s-z_{r}^{0} \right) ^2}+\frac{\partial f}{\partial x_r}\varDelta x_r+\frac{\partial f}{\partial y_r}\varDelta y_r+\frac{\partial f}{\partial z_r}\varDelta z_r
$$

### 上述公式线性化后可以化简为：

<div style="text-align:center">

![线性化后的公式](https://latex.codecogs.com/svg.latex?V%3D%5Cleft%28%20%5Cfrac%7B-%5Cleft%28%20x_s-x_r%20%5Cright%29%7D%7B%5Crho_0%7D%2C%5Cfrac%7B-%5Cleft%28%20y_s-y_r%20%5Cright%29%7D%7B%5Crho_0%7D%2C%5Cfrac%7B-%5Cleft%28%20z_s-z_r%20%5Cright%29%7D%7B%5Crho_0%7D%2C-c%20%5Cright%29%20%5Cleft%5B%20%5Cbegin%7Barray%7D%7Bc%7D%0A%20%20%20%20%5CDelta%20x_r%5C%5C%0A%20%20%20%20%5CDelta%20y_r%5C%5C%0A%20%20%20%20%5CDelta%20z_r%5C%5C%0A%20%20%20%20%5Csigma_%7Btr%7D%5C%5C%0A%20%5Cend%7Barray%7D%20%5Cright%5D%20-L)

</div>

![L](https://latex.codecogs.com/svg.image?L=c\sigma&space;_{ts}+R^0-\rho&space;_0-Delay)

有:

![P0](https://latex.codecogs.com/svg.image?%5Crho%20_0=%5Csqrt%7B%5Cleft(x_s-x_%7Br%7D%5E%7B0%7D%5Cright)%5E2+%5Cleft(y_s-y_%7Br%7D%5E%7B0%7D%5Cright)%5E2+%5Cleft(z_s-z_%7Br%7D%5E%7B0%7D%5Cright)%5E2%7D)

### 上述公式可以简化为

$$
V=Bx-L
$$

$$
x=\left( B^TB \right) ^{-1}\left( B^TL \right)
$$

### 需要进行迭代的话迭代方程为

$$
\left\{ \begin{array}{l}
	x_r=x_r+\varDelta x_r\\
	y_r=y_r+\varDelta y_r\\
	z_r=z_r+\varDelta z_r\\
\end{array} \right.
$$
