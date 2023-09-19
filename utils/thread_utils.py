import threading
import concurrent.futures

from viam.logging import getLogger


class ContextManager:
    """
    ThreadManager

    A singleton pattern to ensure we have only
    one Multithreaded executor spinning for the
    viam integration.

    The multithreaded executor is used so we can
    support multiple processs as needed.
    """
    mgr = None

    @classmethod
    def get_instance(cls):
        """
        return either a new instance or the existing

        :return:
        """
        if cls.mgr is None:
            cls.mgr = concurrent.futures.ThreadPoolExecutor()
        return cls.mgr

    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.debug('ContextManager: initialized ThreadPoolExecutor')
        self.thread_pool = concurrent.futures.ThreadPoolExecutor()
        self.logger.debug(f'Created ContextManager {self.thread_pool}')

    def spin_and_add_thread(self, process):


    def remove_thread(self, node):
        self.logger.debug(f'RclpyNodeManager: attempting to remove node: {node.get_name()}')
        for n in self.executor.get_nodes():
            if n.get_name() == node.get_name():
                self.logger.info(f'RclpyNodeManager: found {node.get_name()}, removing node')
                self.executor.remove_node(node)
        self.logger.debug(f'RclpyNodeManager: successfully remove node: {node.get_name()}')

    def shutdown(self):
        self.logger.info('shutting down thread executor & joining threads')
        pool.shutdown(wait=True)
        self.executor_thread.join()