# python编写协程的程序
import asyncio #不导入这个包async和await没有效果
import time

# async def func():
#     print('hello,I\'m eli')
#
# if __name__ == '__main__':
#     # func() # 此时的函数是异步协程函数，此时函数执行得到的是一个协程对象
#     g = func()
#     # print(g) #<coroutine object func at 0x10a9b9a80> coroutine：协程
#
#     asyncio.run(g) # 协程程序运行需要asyncio模块的支持


async def func1():
    print('func1')
    # time.sleep(3) #这是一个同步阻塞函数。它会把整个线程死死卡住，导致协程根本无法交出控制权，这就失去了编写协程的意义。在协程里，必须使用 await asyncio.sleep() 来模拟异步等待。
    await asyncio.sleep(3) #异步操作的代码，await相当于挂起
    print('func1111')

async def func2():
    print('func2')
    # time.sleep(2)
    await asyncio.sleep(2)
    print('func2222')

async def func3():
    print('func3')
    # time.sleep(4)
    await asyncio.sleep(4)
    print('func3333')

async def main():
    f1 = func1() #coroutine对象(协程对象)
    f2 = func2()
    f3 = func3()


    # 第一种写法（推荐）
    task1 = asyncio.create_task(f1) #将coroutine对象（协程对象）转为task对象
    task2 = asyncio.create_task(f2)
    task3 = asyncio.create_task(f3)

    # await task1
    # await task2
    # await task3

    # 上面三行等价下面这一行代码
    await asyncio.wait([task1, task2, task3])


    # 第二中写法（gather语法糖，内部封装了create_task和wait）
    # await asyncio.gather(f1, f2, f3) #1行省了6行代码

if __name__ == '__main__':
    t1 = time.time()

    # 一次性启用多个任务（协程）
    asyncio.run(main())

    t2 = time.time()
    print(t2 - t1)

"""
func1
func2
func3
func2222
func1111
func3333
4.002878904342651
"""
