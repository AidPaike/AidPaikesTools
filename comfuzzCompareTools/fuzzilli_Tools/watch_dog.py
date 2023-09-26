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
        try:
            save_tmp(event.pathname)
        except Exception as e:
            print(e)
            print("保存文件出错了")
        print("文件被修改:", event.pathname)

    def process_IN_OPEN(self, event):
        """
         文件被打开
        :param event:
        :return:
        """
        print("OPEN event:", event.pathname)

#
# def save_tmp(name):
#     global flag
#     path = CodeAlchemist_path + str(flag) + ".js"
#     from_path = name
#     copyfile(from_path, path)
#     print("复制" + from_path + "到" + str(path))
#     flag += 1
#     print("已储存" + str(flag))


if __name__ == '__main__':
    watch_dir = "/"
    CodeAlchemist_path = "/root/CodeAlchemist/testcase_all/"
    monitor_obj = pyinotify.WatchManager()
    # path监控的目录
    monitor_obj.add_watch(watch_dir, pyinotify.IN_MODIFY, rec=True)
    # event handler
    event_handler = MyEventHandler()
    # notifier
    monitor_loop = pyinotify.Notifier(monitor_obj, event_handler)
    monitor_loop.loop()
