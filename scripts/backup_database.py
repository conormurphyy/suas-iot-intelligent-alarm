
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# Database locations
BASE_DIR = Path("/home/ubuntu/suas-iot-intelligent-alarm")
DATABASE = BASE_DIR / "data" / "alarm.db"
BACKUP_DIR = BASE_DIR / "data" / "backups"

# Keep backups for 14 days
RETENTION_DAYS = 14


def backup_database():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = BACKUP_DIR / f"alarm-{timestamp}.db"

    # Create a consistent SQLite backup
    with sqlite3.connect(DATABASE) as source:
        with sqlite3.connect(backup_file) as destination:
            source.backup(destination)

    print(f"Database backed up to: {backup_file}")

    # Delete backups older than 14 days
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)

    for old_backup in BACKUP_DIR.glob("alarm-*.db"):
        modified = datetime.fromtimestamp(old_backup.stat().st_mtime)

        if modified < cutoff:
            old_backup.unlink()
            print(f"Deleted old backup: {old_backup}")


if __name__ == "__main__":
    backup_database()
