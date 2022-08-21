from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum


class singleEnum(Enum):
    RUNNING = 1
    SHUTDOWN = 0


class futureInfo:
    def __init__(self, future: Future, single: singleEnum = singleEnum.RUNNING):
        self.future = future
        self.single = single


class threadPool:
    """
    create global thread pool
    """

    def __init__(self):
        """
        future_dict 中存放每个线程对象Future和一个信号量的列表
        信号量用于强制终止线程
        """
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.future_dict = dict()

    def is_running(self, project_id):
        """
           check if the future is running and
           then return the running status and future object
        """
        future: futureInfo = self.future_dict.get(project_id)
        if future and future.future.running() and future.single == singleEnum.RUNNING:
            return True, future
        return False, None

    def destroy_task(self, project_id):
        running, future = self.is_running(project_id)
        if not running and future.single == singleEnum.SHUTDOWN:
            return True
        else:
            future.single = singleEnum.SHUTDOWN
            return True
