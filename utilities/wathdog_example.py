import sys
import time
import logging
import queue
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from workflow.watchdogfileeventhandler import WatchdogFileEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = r"/camera_confs"
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # event_handler = LoggingEventHandler()
    event_handler = WatchdogFileEventHandler(queue.Queue(), "_[A-Za-z0-9 ]*.txt")
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()