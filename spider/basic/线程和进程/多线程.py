# 线程，进程
#进程是资源单位，每一个进程至少要有一个线程
#线程是执行单位

# 启动每一个程序默认都会有一个主线程


# 单线程
# def func():
#     for i in range(1000):
#         print('func:',i)
#
# if __name__ == '__main__':
#     func()
#     for i in range(1000):
#         print('main:',i)

# 多线程
from threading import Thread

# 写法一：

# def func():
#     for i in range(1000):
#         print('func:',i)
#
# if __name__ == '__main__':
#
#     t = Thread(target=func) # 开辟一个线程并给线程安排任务
#     t.start()  # 多线程状态为可以开始工作状态，具体的执行时间由CPU决定
#
#     # 再新增多个线程
#     # t2 = Thread(target=func,args=())
#     # t2.start()
#     #
#     # t3 = Thread(target=func,args=())
#     # t3.start()
#
#     for i in range(1000):
#         print('main:',i)



# 给线程传递参数args
def func(name):
    for i in range(1000):
        print(name,i)

if __name__ == '__main__':

    # 双线程 同函数不同参数实战
    t1 = Thread(target=func,args=('周杰伦',)) # args必须是元祖(tupe)类型，后面必须加,号
    t1.start()

    t2 = Thread(target=func, args=('王力宏',))
    t2.start()


# 写法二：
# class MyThread(Thread):
#     def run(self): #固定的 -> 当线程被执行的时候，被执行的就是run()
#         for i in range(1000):
#             print('子线程:',i)
#
# if __name__ == '__main__':
#     t = MyThread()
#     # t.run() #方法调用了 -> 是单线程
#     t.start() #开启线程
#
#     for i in range(1000):
#         print('主线程:',i)


