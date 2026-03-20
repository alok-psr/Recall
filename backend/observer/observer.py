# use this to live check if files are added or removed to update the db
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from process_folder.process_ocr import process_folder_ocr
from pathlib import Path
from db.db_utils import delete_file

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            parent_path = Path(event.src_path).parent
            res = process_folder_ocr(parent_path)
            print("updated db with new file : ", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            delete_file(event.src_path)
            print(f"File removed: {event.src_path}")

# Set up the observer
path = "/home/alok/my_files/projects/hackathon/test/"
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=False)

# Start monitoring
observer.start()
print(f"Monitoring {path} for file additions and removals...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()