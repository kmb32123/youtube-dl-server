from queue import Queue
from threading import Thread
from ydl_server.logdb import JobsDB, Job, Actions


class JobsHandler:
    def __init__(self):
        self.queue = Queue()
        self.thread = None
        self.done = False


    def start(self, dl_queue):
        self.thread = Thread(target=self.worker, args=(dl_queue,))
        self.thread.start()


    def stop(self):
        self.done = True


    def put(self, obj):
        self.queue.put(obj)


    def finish(self):
        self.done = True


    def worker(self, dl_queue):
        db = JobsDB(readonly=False)
        while not self.done:
            action, job = self.queue.get()
            if action == Actions.PURGE_LOGS:
                db.purge_jobs()
            elif action == Actions.INSERT:
                db.insert_job(job)
                dl_queue.put(job)
            elif action == Actions.UPDATE:
                db.update_job(job)
            elif action == Actions.RESUME:
                db.update_job(job)
                dl_queue.put(job)
            elif action == Actions.SET_NAME:
                job_id, name = job
                db.set_job_name(job_id, name)
            elif action == Actions.SET_LOG:
                job_id, log = job
                db.set_job_log(job_id, log)
            elif action == Actions.SET_STATUS:
                job_id, status = job
                db.set_job_status(job_id, status)
            self.queue.task_done()


    def join(self):
        if self.thread is not None:
            return self.thread.join()