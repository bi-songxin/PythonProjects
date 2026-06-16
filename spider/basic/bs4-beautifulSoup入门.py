html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href-"http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>

"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html,'lxml')

# prettify标准锁紧格式输出（自动补全）
# print(soup.prettify())

# 输出title标签内容
# print(soup.title.string)  #The Dormouse's story

"""
节点选择器
.标签名

只会选择到第一个匹配的标签
"""
# print(soup.title) #<title>The Dormouse's story</title>
#
# print(type(soup.title)) #<class 'bs4.element.Tag'>
#
# print(soup.head) #<head><title>The Dormouse's story</title></head>
#
# print(soup.p) #<p class="title" name="dromouse"><b>The Dormouse's story</b></p>

# 获取第一个标签的所有属性(.标签名.attrs)
# print(soup.p.attrs) #{'class': ['title'], 'name': 'dromouse'}
#
# # 获取第一个标签的某个属性的值
# print(soup.p.attrs['name']) #dromouse
#
# # 获取第一个标签内容
# print(soup.p.string)

# 嵌套选择(非重点)
# print(soup.html.head.title)  #等价soup.title
#
# print(type(soup.html.head.title))  #<class 'bs4.element.Tag'>
# print(soup.html.head.title.string) #The Dormouse's story


