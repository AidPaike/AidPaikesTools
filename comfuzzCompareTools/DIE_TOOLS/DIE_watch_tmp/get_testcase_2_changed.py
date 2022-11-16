import os
import time
from shutil import copyfile


import pyinotify

flag = 0


class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_ACCESS(self, event):
        """
        文件被访问
        :param event:
       :return:
        """
        print("件被访问:  ", event.pathname)

    def process_IN_ATTRIB(self, event):
        """
        文件属性被修改，如chmod、chown、touch等
        :param event:
        :return:
        """
        print("文件属性被修改:", event.pathname)

    def process_IN_CLOSE_NOWRITE(self, event):
        """
        不可写文件被close
        :param event:
        :return:
        """
        print("不可写文件被close event:", event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        """
        可写文件被close
        :param event:
        :return: rsync -av /etc/passwd  192.168.204.168:/tmp/passwd.txt
        """
        print("可写文件被close:", event.pathname)

    def process_IN_CREATE(self, event):
        """
        创建新文件
        :param event:
        :return:
        """
        print("创建新文件:", event.pathname)

    def process_IN_DELETE(self, event):
        """
        文件被删除
        :param event:
        :return:
        """
        print("文件被删除:", event.pathname)

    def process_IN_MODIFY(self, event):
        """
        文件被修改
        :param event:
        :return:
        """
        if event.pathname == "/DIE/output-1/.cur_input.js":
            save_tmp(1)
        elif event.pathname == "/DIE/output-0/.cur_input.js":
            save_tmp(0)
        elif event.pathname == "/DIE/output-2/.cur_input.js":
            save_tmp(2)
        elif event.pathname == "/DIE/output-3/.cur_input.js":
            save_tmp(3)
        elif event.pathname == "/DIE/output-4/.cur_input.js":
            save_tmp(4)
        elif event.pathname == "/DIE/output-5/.cur_input.js":
            save_tmp(5)
        elif event.pathname == "/DIE/output-6/.cur_input.js":
            save_tmp(6)
        elif event.pathname == "/DIE/output-7/.cur_input.js":
            save_tmp(7)
        elif event.pathname == "/DIE/output-8/.cur_input.js":
            save_tmp(8)
        elif event.pathname == "/DIE/output-9/.cur_input.js":
            save_tmp(9)
        elif event.pathname == "/DIE/output-10/.cur_input.js":
            save_tmp(10)
        elif event.pathname == "/DIE/output-11/.cur_input.js":
            save_tmp(11)
        elif event.pathname == "/DIE/output-12/.cur_input.js":
            save_tmp(12)
        elif event.pathname == "/DIE/output-13/.cur_input.js":
            save_tmp(13)
        elif event.pathname == "/DIE/output-14/.cur_input.js":
            save_tmp(14)
        elif event.pathname == "/DIE/output-15/.cur_input.js":
            save_tmp(15)
        print("文件被修改:", event.pathname)

    def process_IN_OPEN(self, event):
        """
         文件被打开
        :param event:
        :return:
        """
        print("OPEN event:", event.pathname)


def save_tmp(i):
    global flag
    path = path_testcase + "/{}".format(flag) + ".js"
    from_path = "output-" + str(i) + "/.cur_input.js"
    copyfile(from_path, path)
    print("复制" + from_path + "到" + str(path))
    flag += 1
    print("已储存" + str(flag))


if __name__ == '__main__':
    watch_dir = "/DIE/output-1/.cur_input.js"
    watch_dir2 = "/DIE/output-0/.cur_input.js"
    watch_dir3 = "/DIE/output-2/.cur_input.js"
    watch_dir4 = "/DIE/output-3/.cur_input.js"
    watch_dir5 = "/DIE/output-4/.cur_input.js"
    watch_dir6 = "/DIE/output-5/.cur_input.js"
    watch_dir7 = "/DIE/output-6/.cur_input.js"
    watch_dir8 = "/DIE/output-7/.cur_input.js"
    watch_dir9 = "/DIE/output-8/.cur_input.js"
    watch_dir10 = "/DIE/output-9/.cur_input.js"
    watch_dir11 = "/DIE/output-10/.cur_input.js"
    watch_dir12 = "/DIE/output-11/.cur_input.js"
    watch_dir13 = "/DIE/output-12/.cur_input.js"
    watch_dir14 = "/DIE/output-13/.cur_input.js"
    watch_dir15 = "/DIE/output-14/.cur_input.js"
    watch_dir16 = "/DIE/output-15/.cur_input.js"
    path_testcase = "/DIE/output_testcase2"
    monitor_obj = pyinotify.WatchManager()
    # path监控的目录
    monitor_obj.add_watch(watch_dir, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir2, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir3, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir4, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir5, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir6, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir7, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir8, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir9, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir10, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir11, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir12, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir13, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir14, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir15, pyinotify.IN_MODIFY, rec=True)
    monitor_obj.add_watch(watch_dir16, pyinotify.IN_MODIFY, rec=True)
    # event handler
    event_handler = MyEventHandler()

    # notifier
    monitor_loop = pyinotify.Notifier(monitor_obj, event_handler)
    monitor_loop.loop()
