# why you need this?
When you want to use MongoDB to query every single point in the polygon, we can use $geoWith. 
We can use the following syntax:
```
{
   // We don't need to give this location field any indexes.
   // unless you want to use $near or $geoNear
   <location field>: {
      $geoWithin: {
         $geometry: {
            type: "Polygon",
            coordinates: [
            		[
            			[lon1, lat1],
                        [lon2, lat2],
                        [lon3, lat3],
                        ...,
                        [lon1, lat1]
                    ]
                ] // the first and last coordinate should be same cause we need a 'closed loop'.
         }
      }
   }
}
```
If there is any intersect in the Polygon, MongoDB will throw an query error. 
We can check it before we do the query, so we only send the valid query to MongoDB.

# 这个判断有什么用？
使用MongoDB进行地理查询时，如果想要查询所有在polygon（多边形）里面的数据点，可使用$geoWithin这个关键词。具体用法如下：
```
{
   // 我们不需要给这个字段配置地理位置索引
   // 如果你想用$near或者$geoNear，则需要配置。我在项目中使用'2dsphere'。我的基础坐标系为'wgs84'
   <location field>: {
      $geoWithin: {
         $geometry: {
            type: "Polygon",
            coordinates: [
            		[
            			[lon1, lat1],
                        [lon2, lat2],
                        [lon3, lat3],
                        ...,
                        [lon1, lat1]
                    ]
                ] // 数组的第一个经纬度和最后一个经纬度保持一致，形成闭环。
         }
      }
   }
}
```

如果坐标里面有内部交叉，MongoDB查询会抛出错误。我们在前端进行一次检查，少一次网络交互。
