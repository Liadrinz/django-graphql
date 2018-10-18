# Django 前后端分离开发快速入门 for 胖胖组

#### 1. Windows下环境搭建
- 安装 python 3.6.5 <br>
https://www.python.org/downloads/release/python-365/
- 安装 pip <br>
https://blog.csdn.net/zytbft/article/details/72566197?utm_source=blogxgwz5
- 使用 pip 安装 django
```cmd
pip install django
```

#### 2. Ubuntu下环境搭建
- 安装 python3 (系统默认是python2)
```shell
sudo apt-get install python3
```
- 安装 pip3 (pip对应python2, pip3对应python3)
```shell
sudo apt-get install pip3
```
- 使用 pip3 安装 django
```shell
pip3 install django
```

#### 3. 了解 Django
官方文档：https://docs.djangoproject.com/zh-hans/2.1/ <br>
Django 框架可以简单地分为以下下几层
- 模型层 —— 构建和操纵数据库<br>
在模型层中可以创建一个个的类，他们都是django.db.models.Model的派生类，一个类就相当于一张数据库表
- 视图层 —— 接收请求，返回响应<br>
在视图层中可以创建一个个的类或是函数，用来接收请求并返回响应
- 模板层<br>
django模板是特殊的html文件，视图层中的响应数据可以被传到模板层，呈现到html页面上 <br>
使用django做前后端分离的开发时，一般不需要用到模板层。可以理解为：独立的前端取代了模板层，成为视图层中响应数据的接收端。

#### 4. Django ORM
ORM (Object-Relation Mapping) 对象-关系映射 <br>
ORM封装了SQL语句，所以我们在操作数据库中的数据时，只需用操作对象的方式即可。<br>
例如，先在models.py(模型层)中建立一个老师模型
```python
from django.db import models


# 建立一个老师模型
class Teacher(models.Model):
  name = models.CharField(max_length=100)
  school = models.CharField(max_length=100)
```
然后将模型迁移到数据库(这个过程可以理解为建立映射关系)
```shell
# linux shell
python3 manage.py makemigrations
python3 manage.py migrate

# windows cmd
python manage.py makemigrations
python manage.py migrate
```
此后，数据库中就建立了一张老师的表，具有name和school字段，还有一个自增的id字段。然后使用面向对象的语句可以对该表进行增删查改：
```python
# 该文件与models.py在同一文件夹下
from dir_name.models import Teacher  # 导入Teacher类

Teacher.objects.create(name="赵方", school="软件学院")  # 在Teacher类对应的表中创建(插入)一条数据
Teacher.objects.get(pk=1) # 返回Teacher类对应的表中id为1的数据
Teacher.objects.all() # 返回该表中的所有数据
Teacher.objects.get(pk=1).name = "王安生"  # 修改id为1的老师的姓名
Teacher.objects.get(pk=1).delete()  # 从表中删除id为1的老师

```
更多操作见3中的django官方文档，或学习5中的实践教程

#### 5. 用django创建一个博客网站
教程视频：https://www.imooc.com/learn/790 <br>
非重点关注：模板、表单、admin (其他都重点关注一下) <br>
PS:不必做出完整的博客，只需掌握对django的原理有一定的理解

#### 6. 前后端分离的开发
开发一个博客后端，提供博客的增删查改四个接口给前端使用。<br>
需要在视图层做的工作：接收前端请求 -> 获取请求中的数据 -> 使用数据执行业务逻辑 -> 返回给前端一个响应 <br>
(前端工作：向后端发送请求 -> 接收后端响应 -> 获取响应中的数据 -> 使用数据执行业务逻辑) <br>
例如这是一个前端使用POST方法发送请求来创建博客的(伪)代码
```python
# views.py
# 规定前端传数据的格式为 {"blog": {"title": "博客标题", "content": "博客内容"}}

import json
from django.http import HttpResponse
from dir_name.models import Blog  # 导入模型

def create_blog(request):
  post_data = request.POST['blog']  # 获取数据中的blog字段
  title = post_data['title']  # 获取标题
  content = post_data['content'] # 获取内容
  Blog.objects.create(title=title, content=content) # 在数据库中创建(插入)博客
  return HttpResponse(json.dumps({"msg": "ok"}))  # 返回一个json格式的响应给前端
```
#### 7. Django REST framework
了解什么是REST framework和RESTful API，详情参见阮一峰老师的博客：http://www.ruanyifeng.com/blog/2011/09/restful.html <br>
简单概述：如果按照传统的方式设计API，对于一个资源(比如老师)的增、删、查、改，需要使用4个不同的url，例如/create_teacher, /delete_teacher, /get_teacher, /edit_teacher，这种API设计根本不适合前后端分离开发，对于前端来说API太多。而在RESTful API中，url本身并不表示一个动作，只表示一个资源，这种url也叫uri，至于要对资源做什么动作，由发送请求的方法决定，例如对/teacher发送POST请求表示增加一名老师，对/teacher发送GET请求表示获取所有老师，这相当于上述的/create_teacher和/delete_teacher。至于删和改，则需要定位到更精确的uri，如/teacher/1，/teacher/2。

#### 8. 比 REST 更灵活的 GraphQL
GraphQL是一种查询语言，如果在后端搭建GraphQL，就能接收前端发送的GraphQL请求 <br>
GraphQL语法请参见: http://graphql.cn/ <br>

为什么使用 GraphQL ? <br>
因为REST 每次只能操纵一个资源 <br>
假设某Django项目有两个模型，老师(Teacher)和课程(Course)，且每门课程只能由一门老师任教。在课程模型中，有老师这个字段，存储的是老师的id；同时，在老师模型中也有课程，存储的是这名老师所任教的所有课的id(可以理解为一个列表)。使用RESTful API，要获取某名老师教的所有课程的详细信息，前端发送请求的步骤如下： <br>
1. GET请求id为1的老师，获取老师信息中的课程字段，得到一个装有课程id的列表<br>
2. 设id列表为idList，对于每个idList中的idItem，GET请求id为idItem的课程，获取课程的详细信息<br>
在 GraphQL 中，只需要写如下GraphQL语句：<br>
```gql
query {
  teachers(id: 1) {
    courses {
      id
      courseName
      courseStartTime
    }
  }
}
```
就能获取id为1的老师所教所有课程的id、课程名和课程开始时间 <br>
7和8讲述的都是对前端使用API而言的，对于后端如何构建API，方法如下：<br>
- Django + GraphQL <br>
文档: https://docs.graphene-python.org/en/latest/quickstart/ <br>
实践: https://blog.csdn.net/kuangshp128/article/details/79491137
- Django + REST framework <br>
文档: https://www.django-rest-framework.org/ <br>
实践: https://www.cnblogs.com/bayueman/p/6647641.html
