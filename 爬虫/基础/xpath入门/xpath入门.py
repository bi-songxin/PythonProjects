# xpath是在XML文档中搜索内容的一门语言
# html是xml的子集
"""
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <author>
        <nick>周大强</nick>
        <nick>周芷若</nick>
    </author>
</book>
"""

# 安装lxml模块
# pip install lxml
# xpath解析

from lxml import etree
import os

html ="""
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>l.23</price>
    <nick>臭豆腐</nick>
    <author>
        <nick id="10086">周大强</nick>
        <nick id="10010">周芷若</nick>
        <nick class="joy">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
        <div>
            <nick>惹了1</nick>
        </div>
        <span>
            <nick>惹了2</nick>
        </span>
    </author>
    
    <partner>
        <nick id="ppc">胖胖陈</nick>
        <nick id="ppbc">胖胖不陈</nick>
    </partner>
</book>
"""

# tree = etree.XML(html)
# result = tree.xpath("/book") # /表示层级关系。第一个/是根节点  [<Element book at 0x10d69bb00>]

# result = tree.xpath("/book/name")  #[<Element name at 0x11f5a1500>]

# text()拿文本
# result = tree.xpath("/book/name/text()")  #['野花遍地香']

# result = tree.xpath("/book/author/nick/text()")  #['周大强', '周芷若', '周杰伦', '蔡依林']

# // 表示后代
# result = tree.xpath("/book/author//nick/text()")  #['周大强', '周芷若', '周杰伦', '蔡依林', '惹了1', '惹了2']

# * 表任意节点 类似.通配符
# result = tree.xpath("/book/author/*/nick/text()")  #['惹了1', '惹了2']
# print(result)



# 1. 动态获取当前脚本所在的文件夹绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 拼接出同级目录下 b.html 的绝对路径
file_path = os.path.join(current_dir, 'b.html')

# 3. 传入绝对路径进行解析
tree2 = etree.parse(file_path)

# [索引值] 索引筛选
# xpath的顺序是从1开始数的，[]表示索引
# result = tree2.xpath("/html/body/ul/li[1]/a/text()") #['百度']

#[@属性='属性值'] 属性筛选
# result = tree2.xpath("/html/body/ol/li/a[@href='dapao']/text()")  # ['大炮']

# print(result)


# 法一
ol_li_list = tree2.xpath("/html/body/ol/li")
#从每一个li中提取文字信息
for li in ol_li_list:
    # .相对查找
    # result1 = li.xpath("./a/text()") #在li中继续查找
    # print(result1)
    # 拿属性值：@属性值
    result2 = li.xpath("./a/@href")
    print(result2)

# 法二
print(tree2.xpath("/html/body/ol/li/a/@href"))




"""
页面获取指定位置数据的xpath技巧：
1.打开F12开发者工具，使用左上角小箭头工具定位需要获取的信息
2.定位到页面源代码，拷贝对应的xpath
"""