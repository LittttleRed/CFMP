minio使用方法
# 后端
1 pip install django-minio-storage

2.settings.py中设置minio服务器信息(已完成)

3.使用minio_storage.storage.MinioStorage()来上传文件
方法(demo)
```python
class UploadPortraitView(APIView):
    def post(self, request):
        file=request.FILES['image']#使用request.FILES来获取上传的文件
        file.name='test1.jpg'#正确且唯一的命名,建议结合时间戳与用户(商品)主键命名
        storage=MinioMediaStorage()#获取存储对象
        storage.save(file.name,file)#存储文件
        
        # 将storage.url(file.name)存到数据库中,并返回给前端
        # storage.url(file.name)的形式:http://59.110.23.64:9000/img/test.jpg
        
        return Response(storage.url(file.name),status=status.HTTP_200_OK)

    def get(self,request):
        storage=MinioMediaStorage()
        date={'image':storage.url('test.jpg')}#按照返回格式将url返回给前端
        return Response(date,status=status.HTTP_200_OK)
```

# 前端
1.为解决跨域问题,在vite.config.js中添加如下代码
```javascript
 "/minio":{
          target: "http://59.110.23.64:9000",
            changeOrigin: true,
            secure: false,
            agent: new http.Agent(),
            rewrite: (path) => path.replace(/^\/minio/, ""),
        }
```
2.详情请见 [前端] views中的test_img