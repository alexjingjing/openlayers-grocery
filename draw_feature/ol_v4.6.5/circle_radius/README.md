# Radius calculation


# 半径计算
OpenLayers内置的getRadius()方法有问题，给出的半径会比实际圈划出的半径大，于是我就自己写了个简单方法：
1、使用OpenLayers内置的getExtent()方法，获取圈划范围的minx,miny,maxx,maxy. 根据这四个坐标可以获取一个矩形。
2、由于我们画的是圆形，因此这个矩形是正方形。
3、minx,miny,maxx,maxy可以计算出斜边长。
4、斜边长除以根号二再除以2即为半径长。
