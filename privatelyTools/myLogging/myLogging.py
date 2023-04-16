import logging


class Logger:
    def __init__(self, log_path, log_level=logging.INFO, log_outputs=None):
        if log_outputs is None:
            log_outputs = ['console', 'file']
        self.log_path = log_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # 遍历log_outputs列表，设置输出方式
        for output in log_outputs:
            if output == 'console':
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_level)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
            elif output == 'file':
                file_handler = logging.FileHandler(log_path)
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            else:
                # 如果log_outputs中存在未知的输出方式，直接忽略
                pass

    def info(self, message):
        """
        记录正常运行信息。
        """
        self.logger.info(message)

    def error(self, message):
        """
        记录错误信息。
        """
        self.logger.error(message)

    def warning(self, message):
        """
        记录警告信息。
        """
        self.logger.warning(message)

    def debug(self, message):
        """
        记录调试信息。
        """
        self.logger.debug(message)

    def critical(self, message):
        """
        记录严重错误信息。
        """
        self.logger.critical(message)

    def exception(self, message):
        """
        记录异常信息。
        """
        self.logger.exception(message)

    def log(self, level, message):
        """
        记录指定等级的信息。
        """
        self.logger.log(level, message)

    def fatal(self, message):
        """
        记录致命错误信息。
        """
        self.logger.fatal(message)

    def trace(self, message):
        """
        记录追踪信息。
        """
        self.logger.log(5, message)  # 5级为trace等级

    def notice(self, message):
        """
        记录注意信息。
        """
        self.logger.log(25, message)  # 25级为notice等级

    def success(self, message):
        """
        记录成功信息。
        """
        self.logger.log(35, message)  # 35级为success等级

    def verbose(self, message):
        """
        记录详细信息。
        """
        self.logger.log(15, message)  # 15级为verbose等级

    def warn(self, message):
        """
        记录警告信息。
        """
        self.logger.warning(message)


if __name__ == '__main__':
    # logger = Logger('./logfile.log', log_outputs=['console', 'file'])
    logger2 = Logger('./logfile.log', log_outputs=['file'])
    # logger.info("logger info")
    logger2.info("logger2 info")
