# Algorithm in Opencv

## Reference
[《OpenCV算法精解：基于Python与C++》(张平 编著)【简介_书评_在线阅读】 - 当当图书 (dangdang.com) http://product.dangdang.com/25182999.html](http://product.dangdang.com/25182999.html)

## shift

**run**
```
cd shift
python shift_.py
```
<img src="./shift/sunoray_x-100_concat.jpg" width="39%"/>..............<img src="./shift/sunoray_y60_concat.jpg" width="39%"/>

## scale

**run**
```
cd scale
python scale_.py
```
<img src="./scale/sunoray_scale2.jpg" width="36%"/><img src="./scale/scalescale.jpg" width="20%"/><img src="./scale/sunoray_scale0.5.jpg" width="36%"/>

按照某一点来缩放的

<img src="./scale/sunoray_x0y00.5.jpg" width="39%"/>..............<img src="./scale/sunoray_x0y02.jpg" width="39%"/>

## rotate

**run**
```
cd rotate
python rotate_.py
```
<img src="./rotate/sunoray_rotate1.0471975511965976.jpg" width="60%"/>

## calculate_transform_matrix

**run**
```
cd calculate_transform_matrix
python getaffinetransform.py
```
<img src="./calculate_transform_matrix/sunoray_getaffine1.0471975511965976.jpg" width="60%"/>

## Insertion

**run**
```
cd insert
python neighbor_insert.py 
```

neighbor_insert, compared with no insertion.

<img src="./insert/sunoray_x0y0_up2_LINEAR.jpg" width="60%"/>

<img src="./insert/sunoray_x0y0_up2_nearest.jpg" width="60%"/>

no insertion.

<img src="./scale/sunoray_scale2.jpg" width="60%"/>

**run**
```
cd insert
python rotate__.py 
```

rotate__ , compared with no insertion.

<img src="./insert/sunoray_rotate1.0471975511965976.jpg" width="60%"/>

no insertion.

<img src="./rotate/sunoray_rotate1.0471975511965976.jpg" width="60%"/>

**run**
```
cd insert
python getaffinetransform__.py 
```

getaffinetransform__ , compared with no insertion.

<img src="./insert/sunoray_getaffine1.0471975511965976.jpg" width="60%"/>

no insertion.

<img src="./calculate_transform_matrix/sunoray_getaffine1.0471975511965976.jpg" width="60%"/>