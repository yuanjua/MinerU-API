import time
import shutil
from pathlib import Path
from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

def _cleanup_old_files(directory: Path, max_age_seconds: int):
    """Internal cleanup function."""
    logger.info(f"Running scheduled cleanup in directory: {directory}")
    now = time.time()
    for f in directory.iterdir():
        if f.is_file():
            try:
                file_mod_time = f.stat().st_mtime
                if (now - file_mod_time) > max_age_seconds:
                    logger.info(f"Deleting old file: {f.name}")
                    f.unlink()
            except Exception as e:
                logger.error(f"Error deleting file {f}: {e}")
    for d in directory.iterdir():
        if d.is_dir() and not any(d.iterdir()):
            logger.info(f"Deleting empty directory: {d.name}")
            d.rmdir()

@asynccontextmanager
async def scheduler_service(output_dir: Path):
    """
    A dedicated lifespan context manager for the APScheduler service.
    """
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        _cleanup_old_files,
        'interval',
        hours=1,
        args=[output_dir, 7 * 24 * 3600]
    )
    
    try:
        logger.info("Starting scheduler service...")
        scheduler.start()
        yield scheduler  # Provide the scheduler instance if needed elsewhere
    finally:
        logger.info("Shutting down scheduler service...")
        scheduler.shutdown()

def flatten_folder(target_dir: Path, levels: int):
    """
    Flatten a folder and all its subfolders into the target directory.
    """
    for i in range(levels):
        flatten_this_level(target_dir)

def flatten_this_level(current_dir: Path):
    """
    Flatten the first level of the folder.
    """
    for file in current_dir.iterdir():
        if file.is_dir():
            for f in file.iterdir():
                f.rename(current_dir / f.name)
            file.rmdir()

def zip_folder(target_dir: Path, output_file: Path):
    """
    Zip the folder and all its subfolders.
    """
    shutil.make_archive(output_file, 'zip', target_dir)


if __name__ == "__main__":
    import os

    test_dir = Path("test_flatten")
    
    os.makedirs(test_dir / "auto", exist_ok=True)
    os.makedirs(test_dir / "auto/1", exist_ok=True)
    os.makedirs(test_dir / "auto/2", exist_ok=True)
    os.makedirs(test_dir / "auto/3", exist_ok=True)

    flatten_this_level(test_dir)

    print(list(test_dir.iterdir()))

    shutil.rmtree(test_dir)