# coding: utf-8
import psutil


# 写个斐波那契数列计算函数，用于消耗cpu资源
def fibbo(number):
    if number <= 2:
        return 1
    else:
        return fibbo(number - 1) + fibbo(number - 2)


# 获取逻辑cpu的数量
count = psutil.cpu_count()
print(f"逻辑cpu的数量是{count}")
# Process实例化时不指定pid参数，默认使用当前进程PID，即os.getpid()
p = psutil.Process()
cpu_lst = p.cpu_affinity()
print("cpu列表", cpu_lst)
# 将当前进程绑定到cpu1上运行，列表中也可以写多个cpu
p.cpu_affinity([1])
# 运行函数消耗cpu资源
fibbo(80)
