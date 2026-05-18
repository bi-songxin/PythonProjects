# assert len('hi') == 3 # AssertionError

assert len('hi') == 2 # True

assert 'a' in ['b','c']

# assert的缺点：一出现AssertionError后，程序就终止了

# 解决办法：使用专门做测试用例的库，他们一次性能跑多个测试用例，并能直观的展示哪些测试用例通过了

# unittest:python中最常用的单元测试库，python自带库
# 单元测试：对软件中的最小可测试单元进行验证，如验证函数是否符合预期

# 一般来说测试代码是独立文件，不能将要测试的代码放在一个文件里
# 使用python -m unittest运行编写的自动化测试用例
# 细节:unittest 的测试文件名和测试用例函数必须以test_开头，否则在python -m unittest时将找不到


