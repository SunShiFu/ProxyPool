# ProxyPool
基于python爬虫+flaskweb框架的IP动态代理池

## 运行环境
* Python 3.6
* Redis
* flask

## 运行代理池
`$ python3 run.py `

## 手动添加代理
`$ python3 importer.py `

## 使用API获取代理

访问`http://127.0.0.1:5555/`进入主页，如果显示'Welcome'，证明成功启动。

访问`http://127.0.0.1:5555/random`可以获取一个可用代理。  

访问`http://127.0.0.1:5555/count`可以获取代理池中可用代理的数量。 

利用requests获取方法如下

```
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```
## 部分模块功能
* crawler.py

  > 爬虫模块

  * 抓取各大网站的免费代理IP（国外IP可用率太低，这里只抓取国内的），由于是免费的，可用率不是很高，所以要进行异步测试


* schedule.py

  > 调度器模块

  * 可以对给定的代理的可用性进行异步检测，测试不通过的分数减少，通过的分数为100，当分数低于0会被从数据库中删除

  * 代理添加器，用来触发爬虫模块，对代理池内的代理进行补充，代理池代理数达到阈值时停止工作。

  * 代理池启动类，运行RUN函数时，会创建两个进程，负责对代理池内容的增加和更新。

* db.py

  > Redis数据库连接模块，维持与Redis的连接和对数据库的增删查该，

* error.py

  > 异常模块
    > 资源枯竭异常，如果从所有抓取网站都抓不到可用的代理资源，则抛出异常。
    > 代理池空异常，如果代理池长时间为空，则抛出异常。

* api.py

  > API模块，启动一个Web服务器，使用Flask实现，对外提供代理的获取功能。

* setting.py

  > 设置
  * Redis数据库的配置，API的配置，测试参数的调整等
## 项目参考

[https://github.com/Python3WebSpider/ProxyPool](https://github.com/Python3WebSpider/ProxyPool)
