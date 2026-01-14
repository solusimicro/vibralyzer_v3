import queue
import threading
import logging

logger = logging.getLogger(__name__)


class L2JobQueue:
    def __init__(self, maxsize: int = 10):
        self.queue = queue.Queue(maxsize=maxsize)
        self._worker = None
        self._stop_event = threading.Event()

    def start(self, worker_fn):
        if self._worker:
            return

        self._worker = threading.Thread(
            target=self._run,
            args=(worker_fn,),
            daemon=True,
        )
        self._worker.start()

    def stop(self):
        self._stop_event.set()

    def enqueue(self, job: dict) -> bool:
        try:
            self.queue.put_nowait(job)
            return True
        except queue.Full:
            logger.warning("L2 queue full, job dropped")
            return False

    def _run(self, worker_fn):
        while not self._stop_event.is_set():
            try:
                job = self.queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                worker_fn(job)
            except Exception:
                logger.exception("L2 worker failed")
            finally:
                self.queue.task_done()
