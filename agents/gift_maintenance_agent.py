#!/usr/bin/env python3
"""
GIFT Main Maintenance Agent

This is the main orchestrating agent that coordinates all maintenance tasks
for the GIFT framework. It manages canonical documents, versioning, backup,
and validation processes.

Author: GIFT Framework Maintenance System
Version: 1.0
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import schedule
import time

# Import other agents
from canonical_documents_agent import CanonicalDocumentsAgent
from versioning_agent import VersioningAgent, ChangeType
from backup_agent import BackupAgent
from validation_agent import ValidationAgent

class GIFTMaintenanceAgent:
    """
    Main orchestrating agent for GIFT framework maintenance.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.config_path = self.project_root / "agents" / "maintenance_config.json"
        self.log_path = self.project_root / "agents" / "logs" / "maintenance_agent.log"
        
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
        
        # Initialize sub-agents
        self.canonical_agent = CanonicalDocumentsAgent(project_root)
        self.versioning_agent = VersioningAgent(project_root)
        self.backup_agent = BackupAgent(project_root)
        self.validation_agent = ValidationAgent(project_root)
        
        # Load configuration
        self.config = self._load_configuration()
        
    def _load_configuration(self) -> Dict:
        """Load maintenance configuration."""
        default_config = {
            "maintenance_schedule": {
                "canonical_scan": "daily@06:00",
                "validation": "daily@07:00", 
                "backup": "daily@02:00",
                "cleanup": "weekly@sunday@04:00"
            },
            "notification_settings": {
                "email_alerts": False,
                "log_level": "INFO",
                "report_recipients": []
            },
            "validation_settings": {
                "strict_mode": True,
                "auto_fix": False,
                "require_approval": True
            },
            "backup_settings": {
                "auto_backup": True,
                "include_legacy": False,
                "retention_days": 90
            }
        }
        
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        # Save config for reference
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def run_daily_maintenance(self):
        """Run daily maintenance tasks."""
        self.logger.info("Starting daily maintenance routine...")
        
        try:
            # 1. Scan canonical documents
            self.logger.info("Scanning canonical documents...")
            canonical_docs = self.canonical_agent.scan_canonical_documents()
            self.logger.info(f"Found {len(canonical_docs)} canonical documents")
            
            # 2. Run validation
            self.logger.info("Running framework validation...")
            validation_issues = self.validation_agent.validate_framework()
            critical_issues = [i for i in validation_issues if i.severity.value == "critical"]
            
            if critical_issues:
                self.logger.error(f"Found {len(critical_issues)} critical validation issues")
                self._send_alert(f"Critical validation issues found: {len(critical_issues)}")
            else:
                self.logger.info(f"Validation completed. Found {len(validation_issues)} total issues")
            
            # 3. Create backup
            if self.config["backup_settings"]["auto_backup"]:
                self.logger.info("Creating daily backup...")
                backup_path = self.backup_agent.create_backup("daily")
                self.logger.info(f"Daily backup created: {backup_path}")
            
            # 4. Generate maintenance report
            report = self.generate_maintenance_report()
            self._save_daily_report(report)
            
            self.logger.info("Daily maintenance completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during daily maintenance: {e}")
            self._send_alert(f"Daily maintenance failed: {e}")
    
    def run_weekly_maintenance(self):
        """Run weekly maintenance tasks."""
        self.logger.info("Starting weekly maintenance routine...")
        
        try:
            # 1. Create weekly backup (including legacy)
            self.logger.info("Creating weekly backup...")
            backup_path = self.backup_agent.create_backup("weekly", include_legacy=True)
            self.logger.info(f"Weekly backup created: {backup_path}")
            
            # 2. Backup canonical documents
            self.logger.info("Creating canonical backup...")
            canonical_path = self.backup_agent.backup_canonical_documents()
            self.logger.info(f"Canonical backup created: {canonical_path}")
            
            # 3. Cleanup old backups
            self.logger.info("Cleaning up old backups...")
            self.backup_agent.cleanup_old_backups()
            
            # 4. Generate weekly report
            report = self.generate_weekly_report()
            self._save_weekly_report(report)
            
            self.logger.info("Weekly maintenance completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during weekly maintenance: {e}")
            self._send_alert(f"Weekly maintenance failed: {e}")
    
    def validate_modification(self, document: str, section: str, content: str, 
                           author: str, description: str) -> Dict:
        """
        Validate a modification against canonical documents.
        
        Args:
            document: Document being modified
            section: Section within document
            content: New content
            author: Author of modification
            description: Description of change
            
        Returns:
            Validation result dictionary
        """
        self.logger.info(f"Validating modification to {document}/{section} by {author}")
        
        # Determine change type (placeholder - would use AI/NLP in full implementation)
        change_type = ChangeType.IMPROVEMENT  # Default assumption
        
        # Validate against canonical documents
        canonical_doc = self._find_canonical_reference(document)
        if canonical_doc:
            is_valid, reason, details = self.canonical_agent.validate_modification(
                content, canonical_doc, section
            )
        else:
            is_valid, reason, details = True, "No canonical reference found", {}
        
        # Create version entry
        if is_valid:
            version_entry = self.versioning_agent.create_version_entry(
                document=document,
                section=section,
                change_type=change_type,
                description=description,
                author=author,
                canonical_reference=canonical_doc or "unknown",
                content=content
            )
            
            self.logger.info(f"Modification validated and version entry created")
        else:
            self.logger.warning(f"Modification validation failed: {reason}")
        
        return {
            "is_valid": is_valid,
            "reason": reason,
            "details": details,
            "version_entry": version_entry if is_valid else None,
            "requires_approval": self.config["validation_settings"]["require_approval"]
        }
    
    def _find_canonical_reference(self, document: str) -> Optional[str]:
        """Find canonical reference for a document."""
        # Simple mapping - in full implementation would be more sophisticated
        canonical_mapping = {
            "preprint": "gift-main.pdf",
            "technical_supplement": "gift_technical.pdf",
            "tutorial": "gift_tutorial_e8_to_sm.ipynb"
        }
        
        for key, value in canonical_mapping.items():
            if key in document.lower():
                return value
        
        return None
    
    def generate_maintenance_report(self) -> str:
        """Generate daily maintenance report."""
        report = []
        report.append("=" * 60)
        report.append("GIFT DAILY MAINTENANCE REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Canonical documents status
        canonical_report = self.canonical_agent.generate_canonical_report()
        report.append("CANONICAL DOCUMENTS STATUS:")
        report.append("-" * 40)
        report.append(canonical_report)
        report.append("")
        
        # Validation status
        validation_issues = self.validation_agent.validate_framework()
        critical_count = len([i for i in validation_issues if i.severity.value == "critical"])
        warning_count = len([i for i in validation_issues if i.severity.value == "warning"])
        
        report.append("VALIDATION STATUS:")
        report.append("-" * 40)
        report.append(f"Total Issues: {len(validation_issues)}")
        report.append(f"Critical: {critical_count}")
        report.append(f"Warnings: {warning_count}")
        report.append("")
        
        # Backup status
        backup_report = self.backup_agent.generate_backup_report()
        report.append("BACKUP STATUS:")
        report.append("-" * 40)
        report.append(backup_report)
        report.append("")
        
        return "\n".join(report)
    
    def generate_weekly_report(self) -> str:
        """Generate weekly maintenance report."""
        report = []
        report.append("=" * 60)
        report.append("GIFT WEEKLY MAINTENANCE REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Version history summary
        version_report = self.versioning_agent.generate_version_report()
        report.append("VERSION HISTORY:")
        report.append("-" * 40)
        report.append(version_report)
        report.append("")
        
        # Backup summary
        backup_report = self.backup_agent.generate_backup_report()
        report.append("BACKUP SUMMARY:")
        report.append("-" * 40)
        report.append(backup_report)
        report.append("")
        
        return "\n".join(report)
    
    def _save_daily_report(self, report: str):
        """Save daily maintenance report."""
        report_path = self.project_root / "agents" / "reports" / f"daily_{datetime.now().strftime('%Y%m%d')}.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def _save_weekly_report(self, report: str):
        """Save weekly maintenance report."""
        report_path = self.project_root / "agents" / "reports" / f"weekly_{datetime.now().strftime('%Y%m%d')}.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def _send_alert(self, message: str):
        """Send alert notification."""
        if self.config["notification_settings"]["email_alerts"]:
            # In full implementation, would send email
            pass
        
        self.logger.warning(f"ALERT: {message}")
    
    def setup_automated_maintenance(self):
        """Setup automated maintenance scheduling."""
        self.logger.info("Setting up automated maintenance schedule...")
        
        # Daily maintenance
        schedule.every().day.at("06:00").do(self.run_daily_maintenance)
        
        # Weekly maintenance
        schedule.every().sunday.at("02:00").do(self.run_weekly_maintenance)
        
        self.logger.info("Automated maintenance schedule configured")
    
    def run_manual_maintenance(self, task: str):
        """Run manual maintenance task."""
        if task == "daily":
            self.run_daily_maintenance()
        elif task == "weekly":
            self.run_weekly_maintenance()
        elif task == "canonical":
            self.canonical_agent.scan_canonical_documents()
        elif task == "validation":
            issues = self.validation_agent.validate_framework()
            print(f"Found {len(issues)} validation issues")
        elif task == "backup":
            self.backup_agent.create_backup("manual")
        else:
            print(f"Unknown maintenance task: {task}")


def main():
    """Main function for the maintenance agent."""
    parser = argparse.ArgumentParser(description="GIFT Maintenance Agent")
    parser.add_argument("--task", choices=["daily", "weekly", "canonical", "validation", "backup"], 
                       help="Manual maintenance task to run")
    parser.add_argument("--setup", action="store_true", help="Setup automated maintenance")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    agent = GIFTMaintenanceAgent(args.project_root)
    
    if args.setup:
        agent.setup_automated_maintenance()
        print("Automated maintenance setup completed")
    elif args.task:
        agent.run_manual_maintenance(args.task)
        print(f"Manual task '{args.task}' completed")
    elif args.daemon:
        agent.setup_automated_maintenance()
        print("GIFT Maintenance Agent running as daemon...")
        print("Press Ctrl+C to stop")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("Maintenance agent stopped")
    else:
        # Default: run daily maintenance
        agent.run_daily_maintenance()
        print("Daily maintenance completed")


if __name__ == "__main__":
    main()

