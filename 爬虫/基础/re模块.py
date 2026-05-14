import re

# findall（用的并不多） 匹配字符串中所有符合正则的内容，返回列表
# lst = re.findall(r'\d+','我的电话号码是10086，我女朋友的电话号码是10010')
# print(lst)


# finditer（最重要） 匹配字符串中所有符合正则的内容，返回迭代器，从迭代器中拿到内容需要.group()
# it = re.finditer(r'\d+','我的电话号码是10086，我女朋友的电话号码是10010')
# print(it)  #<callable_iterator object at 0x124151210>
# for i in it:
#     print(i) #match对象。  <re.Match object; span=(7, 12), match='10086'>  <re.Match object; span=(23, 28), match='10010'>
#     print(i.group())   #10086   10010


# search，找到一个结果就返回，返回的结果是match对象，拿数据需要.group()
# s = re.search(r'\d+','我的电话号码是10086，我女朋友的电话号码是10010')
# print(s)  #match对象。 <re.Match object; span=(7, 12), match='10086'>
# print(s.group())  #10086


# match，从头开始匹配
# ss = re.match(r'\d+','10086，我女朋友的电话号码是10010')
# print(ss)   #None
# print(ss.group())


# 预加载正则表达式compile，优势：1.可以反复使用正则表达式  2.稍微提高程序运行速度

# obj = re.compile(r'(\d+)')
# ret = obj.finditer('我的电话号码是10086，我女朋友的电话号码是10010')
#
# for match in ret:
#     print(match.group())
#
#
# ret1 = obj.findall('我的电话号码是10086，我女朋友的电话号码是10010')
# print(ret1)


sss = """
<div class='jay'><span id='1'>郭麒麟</span></div>
<div class='jj'><span id='2'>宋铁</span></div>
<div class='jolin'><span id='3'>大聪明</span></div>
<div class='sylar'><span i='4'>范思哲</span></div>
<div class='tory'><span id='5'>胡说八道</span></div>
"""

# (?P<分组名字>正则) 可以单独从正则匹配的内容中进一步提取内容
# obj1 = re.compile(r"<div class='.*?'><span id='(?P<id>\d+)'>(?P<name>.*?)</span></div>",re.S)  #re.S:让 . 能匹配换行符
#
# result = obj1.finditer(sss)
#
# for match in result:
#     print(match.group('id'), match.group('name'))
