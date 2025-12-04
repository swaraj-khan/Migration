# PS C:\KOVON\Migration> python -m replicator.main
# To run look above command in terminal



# from __future__ import annotations
# from typing import List
# from .mongo.client import get_db
# from .mongo.change_stream import watch_collection
# from .utils.logger import info, error


# def get_all_collections() -> List[str]:
#     """
#     Discover all MongoDB collections dynamically.
#     """
#     db = get_db()
#     collections = db.list_collection_names()
#     return [c for c in collections if not c.startswith("system.")]


# def start_replication() -> None:
#     """
#     Start replication for all MongoDB collections.
#     """
#     collections = get_all_collections()

#     info("=== Starting MongoDB → Supabase Replication ===")
#     info(f"Discovered collections: {collections}")

#     for coll in collections:
#         info(f"Watching collection: {coll}")
#         try:
#             watch_collection(coll)
#         except Exception as e:
#             error(f"Fatal error watching '{coll}': {e}")
#             continue


# if __name__ == "__main__":
#     try:
#         start_replication()
#     except KeyboardInterrupt:
#         info("Shutting down replication...")


from typing import List
from .mongo.client import get_db
from .mongo.change_stream import watch_collection
from .utils.logger import info, error
import threading
import time

def main():
    db = get_db()

    collections = db.list_collection_names()
    info(f"Discovered collections: {collections}")

    threads = []

    for coll_name in collections:
        info(f"Starting thread for: {coll_name}")

        t = threading.Thread(
            target=watch_collection,
            args=(db[coll_name], coll_name),
            daemon=True    # Threads die when main process ends
        )
        t.start()
        threads.append(t)

    info("🔥 All change streams are now running in parallel!")

    # Keep the main thread alive forever
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        info("🛑 Shutdown requested. Stopping all listeners...")


if __name__ == "__main__":
    main()
