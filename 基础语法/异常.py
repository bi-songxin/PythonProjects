# try-except-else-finally基本结构

"""
try:
    你认为会出错的代码

except 要捕捉具体错误类型:

(任意错误)
except:

(你认为try会出错的代码没报错将会执行)
else:

（无论是否出错都会执行）
finally:


"""

# try:
#     user_weight = float(input("请输入您的体重(单位:kg):"))
#     user_height = float(input("请输入您的身高(单位:m):"))
#     user_BMI =user_weight /user_height ** 2
#
# except ValueError :
#     print("输入不为合理数字，请重新运行程序，并输入正确的数字。")
# except ZeroDivisionError:
#     print("身高不能为零，请重新运行程序，并输入正确的数字。")
# except:
#     print("发生了未知错误，请重新运行程序。")
# else:
#     print("您的BMI值为:"+ str(user_BMI))
# finally:
#     print("程序结束运行。")


"""
练习 10.6：加法运算　在提示用户提供数值输入时，常出现的一个问题是，用户提供的是文本而不是数。在这种情况下，当你尝试将输入转换为整数时，
将引发 ValueError 异常。编写一个程序，提示用户输入两个数，再将它们相加并打印结果。在用户输入的任意一个值不是数时都捕获 ValueError 异常，
并打印一条友好的错误消息。对你编写的程序进行测试：先输入两个数，再输入一些文本而不是数。

"""

try:
    number1 = int(input("请输入第一个数："))
    number2 = int(input("请输入第一个数："))

    print(f'两数字相加结果为{number1+number2}')

except ValueError:
    print('请不要输入非数字！')


