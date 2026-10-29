# 切记,字符串是不可变的对象,所以任何操作对原字符串是不会有任何影响的

# s = 'i am bsx , I LOVE YOU'
# s1 = s.capitalize() #首字母大写
# print(s) #原来s不受影响
# print(s1)
#
# s2 = s.lower() #全部变成小写，有些俄文不能转换成小写，有时无法忽略大小写
# print(s2)
#
# s3 = s.upper() #全部变成大写（重要‼️）忽略大小写
# print(s3)
#
# s4 = s.swapcase() #大写变小写，小写变大写
# print(s4)
#
# ss = 'abc_de fghi哈哈哈abc'
# s5 = ss.title()
# print(s5)



# sss = ' \t \n     我是你     \t \n'
# print(sss)
# print(sss.strip()) #默认是去掉字符串左右两端的空白（空格、\t、\n）
# \t(tab键)、\n（换行）
# print(sss.strip("aa")) #去掉aa


# strip实战
# username = input("请输入用户名：").strip()
# password = input("请输入用户密码：").strip()
#
# if username == 'admin' and password == '123':
#     print('登陆成功！')
# else:
#     print('登陆失败')


# ssss = "我喜欢吃肉"
# print(ssss.replace('肉','*')) #字符串替换

# 去除空格(重要)
# sssss = '   我    爱   你   哈哈哈哈   '
# print(sssss.replace(' ',''))

sa = '张三_李四_王五_赵六'
lst = sa.split('_',1) #正向字符串切割，结果输出成列表
print(lst)

rlst = sa.rsplit('_', 2) #倒向字符串切割
print(rlst)

lst1 = ['张三', '李四', '王五', '赵六']
sb = '_'.join(lst1) #字符串拼接，结果输出成字符串
print(sb)