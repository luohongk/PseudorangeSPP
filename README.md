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

待完善(敬请期待)

## 文件解释

| 文件名      | 文件功能                                     |
| ----------- | -------------------------------------------- |
| main.py     | 主函数，函数入口                             |
| readfile.py | 文件读取类，读与存数据                       |
| satelite.py | 卫星类，用于计算位置位置                     |
| position.py | 定位类，用于进行观测值的匹配以及地面坐标解算 |

## 定位原理

如果通过广播星历以及观测值文件进行单点定位比较困难，需要熟系观测值文件格式以及卫星位置计算的一些算法。但是就比赛而言，核心的就只有误差方程的建立。因为比赛会直接给你卫星的坐标，GPS时，电离层，对流层延迟就可以。直接根据误差方程构建间接平差模型就可以。

### 对于每一个观测伪距

$$
R=\sqrt{\left( x_s-x_r \right) ^2+\left( y_s-y_r \right) ^2+\left( z_s-z_r \right) ^2}=f\left( x_r,y_r,z_r \right)
$$

### 线性化（泰勒公式）：

$$
R^0+V=\sqrt{\left( x_s-x_{r}^{0} \right) ^2+\left( y_s-y_{r}^{0} \right) ^2+\left( z_s-z_{r}^{0} \right) ^2}+\frac{\partial f}{\partial x_r}\varDelta x_r+\frac{\partial f}{\partial y_r}\varDelta y_r+\frac{\partial f}{\partial z_r}\varDelta z_r
$$

### 上述公式线性化后可以化简为：

$$
V=\left( \frac{-\left( x_s-x_r \right)}{\rho _0},\frac{-\left( y_s-y_r \right)}{\rho _0},\frac{-\left( z_s-z_r \right)}{\rho _0},-c \right) \left[ \begin{array}{c}

    \varDelta x_r\\

    \varDelta y_r\\

    \varDelta z_r\\

    \sigma _{tr}\\

\end{array} \right] -L
$$

$$
L=c\sigma _{ts}+R^0-\rho _0-Delay
$$

$$
\rho _0=\sqrt{\left( x_s-x_{r}^{0} \right) ^2+\left( y_s-y_{r}^{0} \right) ^2+\left( z_s-z_{r}^{0} \right) ^2}
$$

### 上述公式可以简化为

$$
V=Bx-L
$$

$$
x=\left( B^TB \right) ^{-1}\left( B^TL \right)
$$

### 需要进行迭代的话迭代方程为

$$
x_r=x_r+\varDelta x_r
$$

$$
y_r=y_r+\varDelta y_r
$$

$$
z_r=z_r+\varDelta z_r
$$

$$


$$
