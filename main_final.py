# Personal project
__author__ = "Eolus"

# Standard libraries
import queue
import time
# Third party libraries
# Custom libraries
from workflow.watchdogfileeventhandler import WatchdogFileEventHandler
from workflow.changewatcher import ChangeWatcher
from workflow.orchestrator import Orchestrator


def __main__():
    # Configuration
    conf_path = ".\\camera_confs\\"
    conf_file_pattern = r'^_[A-Za-z\d_ ]*.yaml$'

    # Configuration change observer and orchestrator
    configuration_change_queue = queue.Queue()
    own_watchdog = WatchdogFileEventHandler(configuration_change_queue,
                                            conf_file_pattern)
    change_watcher = ChangeWatcher(conf_path, conf_file_pattern,
                                   configuration_change_queue, own_watchdog)
    orchestrator = Orchestrator(change_watcher, configuration_change_queue)
    try:
        while True:
            orchestrator.check_queue()
            time.sleep(0.5)
    except Exception as inst:
        print(f"Error while running the orchestrator: {inst}")
        orchestrator.close_and_clean()


__main__()

