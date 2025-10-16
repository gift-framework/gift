#!/usr/bin/env python3
"""
GIFT Backup Agent

This agent handles automated backup, archiving, and recovery of the GIFT project.
It ensures data integrity and provides version-controlled backups with
canonical document preservation.

Author: GIFT Framework Maintenance System
Version: 1.0
"""

import os
import json
import logging
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib
import schedule
import time

class BackupAgent:
    """
    Agent responsible for automated backup and archival of the GIFT project.
    """
    
    def __init__(self, project_root: str = ".", backup_root: str = "./backups"):
        self.project_root = Path(project_root)
        self.backup_root = Path(backup_root)
        self.log_path = self.project_root / "agents" / "logs" / "backup_agent.log"
        
        # Create backup directory structure
        self.backup_root.mkdir(parents=True, exist_ok=True)
        (self.backup_root / "daily").mkdir(exist_ok=True)
        (self.backup_root / "weekly").mkdir(exist_ok=True)
        (self.backup_root / "monthly").mkdir(exist_ok=True)
        (self.backup_root / "canonical").mkdir(exist_ok=True)
        
        # Ensure logs directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load backup configuration
        self.config = self._load_backup_config()
        
    def _load_backup_config(self) -> Dict:
        """Load backup configuration."""
        config_path = self.project_root / "agents" / "backup_config.json"
        
        default_config = {
            "retention_days": {
                "daily": 30,
                "weekly": 90,
                "monthly": 365
            },
            "backup_schedule": {
                "daily": "02:00",  # 2 AM daily
                "weekly": "sunday@02:00",  # Sunday 2 AM
                "monthly": "1@02:00"  # 1st of month 2 AM
            },
            "include_patterns": [
                "github/**",
                "new_work/**",
                "wip_research/**",
                "agents/**",
                "README.md"
            ],
            "exclude_patterns": [
                "legacy/**",
                "backups/**",
                "**/__pycache__/**",
                "**/*.pyc",
                "**/.git/**"
            ],
            "canonical_docs_only": False,
            "compression": True,
            "encryption": False
        }
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        # Save config for reference
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def create_backup(self, backup_type: str = "daily", include_legacy: bool = False) -> str:
        """
        Create a backup of the project.
        
        Args:
            backup_type: Type of backup (daily, weekly, monthly, canonical)
            include_legacy: Whether to include legacy directory
            
        Returns:
            Path to created backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"gift_backup_{backup_type}_{timestamp}"
        backup_path = self.backup_root / backup_type / f"{backup_name}.zip"
        
        self.logger.info(f"Creating {backup_type} backup: {backup_name}")
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                files_added = 0
                
                for pattern in self.config["include_patterns"]:
                    if pattern == "github/**":
                        files_added += self._add_directory_to_zip(
                            zipf, self.project_root / "github", "github", include_legacy
                        )
                    elif pattern == "new_work/**":
                        files_added += self._add_directory_to_zip(
                            zipf, self.project_root / "new_work", "new_work", include_legacy
                        )
                    elif pattern == "wip_research/**":
                        files_added += self._add_directory_to_zip(
                            zipf, self.project_root / "wip_research", "wip_research", include_legacy
                        )
                    elif pattern == "agents/**":
                        files_added += self._add_directory_to_zip(
                            zipf, self.project_root / "agents", "agents", include_legacy
                        )
                    elif pattern == "README.md":
                        readme_path = self.project_root / "README.md"
                        if readme_path.exists():
                            zipf.write(readme_path, "README.md")
                            files_added += 1
                
                # Add legacy if requested
                if include_legacy:
                    files_added += self._add_directory_to_zip(
                        zipf, self.project_root / "legacy", "legacy", include_legacy
                    )
            
            # Create backup metadata
            metadata = {
                "backup_name": backup_name,
                "backup_type": backup_type,
                "timestamp": timestamp,
                "created_date": datetime.now().isoformat(),
                "files_count": files_added,
                "size_bytes": backup_path.stat().st_size,
                "checksum": self._calculate_file_checksum(backup_path),
                "include_legacy": include_legacy,
                "config_used": self.config
            }
            
            metadata_path = self.backup_root / backup_type / f"{backup_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Backup created successfully: {backup_path} ({files_added} files)")
            return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            raise
    
    def _add_directory_to_zip(self, zipf: zipfile.ZipFile, source_dir: Path, 
                            arcname_prefix: str, include_legacy: bool) -> int:
        """Add directory contents to zip file."""
        files_added = 0
        
        if not source_dir.exists():
            return files_added
        
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                # Check exclude patterns
                if self._should_exclude_file(file_path, include_legacy):
                    continue
                
                # Calculate relative path for archive
                rel_path = file_path.relative_to(source_dir)
                arcname = f"{arcname_prefix}/{rel_path}"
                
                try:
                    zipf.write(file_path, arcname)
                    files_added += 1
                except Exception as e:
                    self.logger.warning(f"Could not add file {file_path}: {e}")
        
        return files_added
    
    def _should_exclude_file(self, file_path: Path, include_legacy: bool) -> bool:
        """Check if file should be excluded from backup."""
        file_str = str(file_path)
        
        # Check exclude patterns
        for pattern in self.config["exclude_patterns"]:
            if pattern.replace("**", "").replace("*", "") in file_str:
                return True
        
        # Special handling for legacy
        if "legacy" in file_str and not include_legacy:
            return True
        
        return False
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def restore_backup(self, backup_path: str, restore_location: str = None) -> bool:
        """
        Restore a backup.
        
        Args:
            backup_path: Path to backup file
            restore_location: Where to restore (default: project_root)
            
        Returns:
            True if successful
        """
        backup_file = Path(backup_path)
        if not backup_file.exists():
            self.logger.error(f"Backup file not found: {backup_path}")
            return False
        
        if restore_location is None:
            restore_location = self.project_root / "restored"
        
        restore_path = Path(restore_location)
        restore_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Restoring backup {backup_file.name} to {restore_path}")
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(restore_path)
            
            # Verify backup integrity
            metadata_file = backup_file.parent / f"{backup_file.stem}_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Verify checksum
                current_checksum = self._calculate_file_checksum(backup_file)
                if current_checksum != metadata.get("checksum"):
                    self.logger.warning("Backup checksum verification failed")
            
            self.logger.info(f"Backup restored successfully to {restore_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove old backups according to retention policy."""
        self.logger.info("Cleaning up old backups...")
        
        for backup_type, retention_days in self.config["retention_days"].items():
            backup_dir = self.backup_root / backup_type
            if not backup_dir.exists():
                continue
            
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            removed_count = 0
            
            for backup_file in backup_dir.glob("*.zip"):
                try:
                    # Extract date from filename
                    date_str = backup_file.stem.split("_")[-2]  # YYYYMMDD
                    backup_date = datetime.strptime(date_str, "%Y%m%d")
                    
                    if backup_date < cutoff_date:
                        backup_file.unlink()
                        # Remove associated metadata
                        metadata_file = backup_file.parent / f"{backup_file.stem}_metadata.json"
                        if metadata_file.exists():
                            metadata_file.unlink()
                        removed_count += 1
                        
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"Could not parse date from {backup_file.name}: {e}")
            
            if removed_count > 0:
                self.logger.info(f"Removed {removed_count} old {backup_type} backups")
    
    def backup_canonical_documents(self) -> str:
        """Create a special backup of only canonical documents."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"gift_canonical_{timestamp}"
        backup_path = self.backup_root / "canonical" / f"{backup_name}.zip"
        
        self.logger.info(f"Creating canonical documents backup: {backup_name}")
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add PDF documents from github/legacy/docs_published
                docs_dir = self.project_root / "github" / "legacy" / "docs_published"
                if docs_dir.exists():
                    for pdf_file in docs_dir.glob("*.pdf"):
                        zipf.write(pdf_file, f"canonical/{pdf_file.name}")
                
                # Add canonical database if exists
                canonical_db = self.project_root / "agents" / "canonical_database.json"
                if canonical_db.exists():
                    zipf.write(canonical_db, "canonical/canonical_database.json")
            
            # Create metadata
            metadata = {
                "backup_name": backup_name,
                "backup_type": "canonical",
                "timestamp": timestamp,
                "created_date": datetime.now().isoformat(),
                "size_bytes": backup_path.stat().st_size,
                "checksum": self._calculate_file_checksum(backup_path),
                "description": "Canonical documents and reference database backup"
            }
            
            metadata_path = self.backup_root / "canonical" / f"{backup_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Canonical backup created: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"Error creating canonical backup: {e}")
            raise
    
    def generate_backup_report(self) -> str:
        """Generate a backup status report."""
        report = []
        report.append("=" * 60)
        report.append("GIFT BACKUP REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        total_backups = 0
        total_size = 0
        
        for backup_type in ["daily", "weekly", "monthly", "canonical"]:
            backup_dir = self.backup_root / backup_type
            if not backup_dir.exists():
                continue
            
            backups = list(backup_dir.glob("*.zip"))
            type_size = sum(b.stat().st_size for b in backups)
            
            report.append(f"{backup_type.upper()} Backups:")
            report.append(f"  Count: {len(backups)}")
            report.append(f"  Total Size: {self._format_size(type_size)}")
            report.append("")
            
            total_backups += len(backups)
            total_size += type_size
            
            # Show recent backups
            recent_backups = sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
            if recent_backups:
                report.append(f"  Recent {backup_type} backups:")
                for backup in recent_backups:
                    mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                    size = self._format_size(backup.stat().st_size)
                    report.append(f"    {backup.name} ({size}) - {mtime.strftime('%Y-%m-%d %H:%M')}")
                report.append("")
        
        report.append("SUMMARY:")
        report.append("-" * 40)
        report.append(f"Total Backups: {total_backups}")
        report.append(f"Total Size: {self._format_size(total_size)}")
        report.append("")
        
        report.append("BACKUP SCHEDULE:")
        report.append("-" * 40)
        for backup_type, schedule_time in self.config["backup_schedule"].items():
            report.append(f"{backup_type.title()}: {schedule_time}")
        report.append("")
        
        return "\n".join(report)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def setup_automated_backups(self):
        """Setup automated backup scheduling."""
        # Daily backup
        schedule.every().day.at(self.config["backup_schedule"]["daily"].split("@")[1]).do(
            lambda: self.create_backup("daily")
        )
        
        # Weekly backup
        if "sunday" in self.config["backup_schedule"]["weekly"]:
            schedule.every().sunday.at("02:00").do(
                lambda: self.create_backup("weekly")
            )
        
        # Monthly backup
        schedule.every().month.do(
            lambda: self.create_backup("monthly", include_legacy=True)
        )
        
        # Canonical backup (weekly)
        schedule.every().sunday.at("03:00").do(
            self.backup_canonical_documents
        )
        
        # Cleanup (daily)
        schedule.every().day.at("04:00").do(
            self.cleanup_old_backups
        )
        
        self.logger.info("Automated backup schedule configured")


def main():
    """Main function for testing the agent."""
    agent = BackupAgent()
    
    print("GIFT Backup Agent")
    print("=" * 40)
    
    # Create a test backup
    print("Creating test backup...")
    backup_path = agent.create_backup("daily")
    print(f"Backup created: {backup_path}")
    
    # Create canonical backup
    print("Creating canonical backup...")
    canonical_path = agent.backup_canonical_documents()
    print(f"Canonical backup created: {canonical_path}")
    
    # Generate report
    print("\nGenerating backup report...")
    report = agent.generate_backup_report()
    print(report)


if __name__ == "__main__":
    main()
