from web.apis.tasks import celery
import multiprocessing

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    celery.start()