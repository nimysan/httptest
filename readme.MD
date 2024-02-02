# 测试


https://locust.io/

test url: http://d2v7mm0wuwqays.cloudfront.net

[标准教程入口](https://docs.locust.io/en/stable/writing-a-locustfile.html#user-class)

指导文档
[一文让 locust 小白，变成性能测试老司机 ](http://testingpai.com/article/1595507305331/comment/1597912972635)

## 主副

```bash
locust -f simple.py --master --master-bind-host=172.31.46.167 --processes -1
locust -f simple.py --worker --master-host=172.31.46.167 --processes -1
```

## 本地开启一个dash频道

```bash
ffmpeg_to_dash.sh创建一个mpd和相应的文件， 在moive目录下
```

```bash
#启动一个静态文件服务器
python -m http.server 8000
```

使用VLC播放: http://localhost:8000/moive/moive.mpd


## 转发老唐的视频
地址： http://52.50.139.233/sample.ts
