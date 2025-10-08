#!/usr/bin/env python3
"""
GIFT Agents Setup Script

This script sets up the GIFT maintenance agents system.
It initializes the database, creates necessary directories,
and performs initial configuration.

Author: GIFT Framework Maintenance System
Version: 1.0
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

def setup_agents():
    """Setup the GIFT agents system."""
    print("GIFT Agents Setup")
    print("=" * 40)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    agents_dir = project_root / "agents"
    
    print(f"Project root: {project_root}")
    print(f"Agents directory: {agents_dir}")
    
    # Create necessary directories
    directories = [
        "logs",
        "reports", 
        "backups",
        "backups/daily",
        "backups/weekly",
        "backups/monthly",
        "backups/canonical"
    ]
    
    for directory in directories:
        dir_path = agents_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    # Initialize agent databases
    print("\nInitializing agent databases...")
    
    # Canonical documents database
    canonical_db = {
        "canonical_documents": {},
        "last_scan": None,
        "version": "1.0"
    }
    
    canonical_db_path = agents_dir / "canonical_database.json"
    with open(canonical_db_path, 'w', encoding='utf-8') as f:
        json.dump(canonical_db, f, indent=2)
    print(f"Initialized: {canonical_db_path}")
    
    # Version database
    version_db = {
        "versions": [],
        "last_updated": None,
        "schema_version": "1.0"
    }
    
    version_db_path = agents_dir / "version_database.json"
    with open(version_db_path, 'w', encoding='utf-8') as f:
        json.dump(version_db, f, indent=2)
    print(f"Initialized: {version_db_path}")
    
    # Validation database
    validation_db = {
        "validation_history": [],
        "last_validation": None,
        "schema_version": "1.0"
    }
    
    validation_db_path = agents_dir / "validation_database.json"
    with open(validation_db_path, 'w', encoding='utf-8') as f:
        json.dump(validation_db, f, indent=2)
    print(f"Initialized: {validation_db_path}")
    
    # Backup configuration
    backup_config = {
        "retention_days": {
            "daily": 30,
            "weekly": 90,
            "monthly": 365
        },
        "backup_schedule": {
            "daily": "02:00",
            "weekly": "sunday@02:00",
            "monthly": "1@02:00"
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
    
    backup_config_path = agents_dir / "backup_config.json"
    with open(backup_config_path, 'w', encoding='utf-8') as f:
        json.dump(backup_config, f, indent=2)
    print(f"Initialized: {backup_config_path}")
    
    # Maintenance configuration
    maintenance_config = {
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
    
    maintenance_config_path = agents_dir / "maintenance_config.json"
    with open(maintenance_config_path, 'w', encoding='utf-8') as f:
        json.dump(maintenance_config, f, indent=2)
    print(f"Initialized: {maintenance_config_path}")
    
    # Create initial canonical documents scan
    print("\nPerforming initial canonical documents scan...")
    try:
        from canonical_documents_agent import CanonicalDocumentsAgent
        canonical_agent = CanonicalDocumentsAgent(str(project_root))
        canonical_docs = canonical_agent.scan_canonical_documents()
        print(f"Found {len(canonical_docs)} canonical documents")
        
        # Generate initial report
        report = canonical_agent.generate_canonical_report()
        report_path = agents_dir / "reports" / f"initial_canonical_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Initial canonical report saved: {report_path}")
        
    except Exception as e:
        print(f"Warning: Could not perform initial canonical scan: {e}")
    
    # Create setup completion marker
    setup_marker = {
        "setup_date": datetime.now().isoformat(),
        "setup_version": "1.0",
        "project_root": str(project_root),
        "agents_directory": str(agents_dir)
    }
    
    setup_marker_path = agents_dir / "setup_complete.json"
    with open(setup_marker_path, 'w', encoding='utf-8') as f:
        json.dump(setup_marker, f, indent=2)
    
    print("\n" + "=" * 40)
    print("GIFT Agents Setup Complete!")
    print("=" * 40)
    print(f"Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project root: {project_root}")
    print(f"Agents directory: {agents_dir}")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r agents/requirements.txt")
    print("2. Run initial maintenance: python agents/gift_maintenance_agent.py")
    print("3. Setup automated maintenance: python agents/gift_maintenance_agent.py --setup")
    print("4. Run as daemon: python agents/gift_maintenance_agent.py --daemon")


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        requirements_path = Path(__file__).parent / "requirements.txt"
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)], 
                      check=True)
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True


def main():
    """Main setup function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--install-deps":
        if install_dependencies():
            setup_agents()
        else:
            print("Setup failed due to dependency installation error")
            sys.exit(1)
    else:
        setup_agents()
        print("\nTo install dependencies, run: python setup_agents.py --install-deps")


if __name__ == "__main__":
    main()

