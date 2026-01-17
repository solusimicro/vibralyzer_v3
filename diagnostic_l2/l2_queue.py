import queue
import threading
import logging

logger = logging.getLogger(__name__)

class L2JobQueue:
    def __init__(self, maxsize=10):
        self.queue = queue.Queue(maxsize=maxsize)
        self._worker_thread = None
        self._running = False

    def start(self, worker_fn):
        if self._worker_thread:
            return

        self._running = True

        def _run():
            while self._running:
                try:
                    job = self.queue.get()
                    worker_fn(job)
                except Exception:
                    logger.exception("L2 worker failed")
                finally:
                    self.queue.task_done()

        self._worker_thread = threading.Thread(
            target=_run, daemon=True
        )
        self._worker_thread.start()
            
    def enqueue(self, job: dict) -> bool:
        try:
            self.queue.put(job, block=False)
            return True
        except queue.Full:
            logger.warning("L2 queue full — job dropped")
            return False

    def stop(self):
        self._running = False

 