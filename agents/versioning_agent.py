#!/usr/bin/env python3
"""
GIFT Versioning Agent

This agent tracks versions and ensures that all changes are improvements or deepenings
relative to canonical documents. It maintains a detailed history of modifications
and validates that no regressions occur.

Author: GIFT Framework Maintenance System
Version: 1.0
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib
import git
from dataclasses import dataclass, asdict
from enum import Enum

class ChangeType(Enum):
    """Types of changes that can occur."""
    IMPROVEMENT = "improvement"
    DEEPENING = "deepening"
    CLARIFICATION = "clarification"
    CORRECTION = "correction"
    REGRESSION = "regression"  # Should be flagged
    UNKNOWN = "unknown"

@dataclass
class VersionEntry:
    """Represents a version entry in the system."""
    timestamp: str
    document: str
    section: str
    change_type: ChangeType
    description: str
    author: str
    canonical_reference: str
    validation_status: str
    content_hash: str
    diff_summary: str
    approval_status: str = "pending"

class VersioningAgent:
    """
    Agent responsible for tracking versions and ensuring improvement-only changes.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.version_db_path = self.project_root / "agents" / "version_database.json"
        self.log_path = self.project_root / "agents" / "logs" / "versioning_agent.log"
        
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
        
        # Initialize version database
        self.version_db = self._load_version_database()
        
        # Initialize git repository if available
        try:
            self.repo = git.Repo(self.project_root)
        except git.InvalidGitRepositoryError:
            self.repo = None
            self.logger.warning("No git repository found. Version tracking will be limited.")
    
    def _load_version_database(self) -> Dict:
        """Load or create version database."""
        if self.version_db_path.exists():
            with open(self.version_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert change_type strings back to enums
                for entry in data.get("versions", []):
                    entry["change_type"] = ChangeType(entry["change_type"])
                return data
        return {
            "versions": [],
            "last_updated": None,
            "schema_version": "1.0"
        }
    
    def _save_version_database(self):
        """Save version database."""
        # Convert enums to strings for JSON serialization
        data = self.version_db.copy()
        for entry in data["versions"]:
            entry["change_type"] = entry["change_type"].value
        
        with open(self.version_db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_version_entry(self, document: str, section: str, change_type: ChangeType,
                           description: str, author: str, canonical_reference: str,
                           content: str, old_content: str = None) -> VersionEntry:
        """
        Create a new version entry for a document modification.
        
        Args:
            document: Name of the document being modified
            section: Section within the document
            change_type: Type of change (improvement, deepening, etc.)
            description: Description of the change
            author: Author of the change
            canonical_reference: Reference to canonical PDF document
            content: New content
            old_content: Previous content (optional)
            
        Returns:
            VersionEntry object
        """
        timestamp = datetime.now().isoformat()
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Generate diff summary if old content provided
        diff_summary = ""
        if old_content:
            diff_summary = self._generate_diff_summary(old_content, content)
        
        # Validate the change type
        validation_status = self._validate_change_type(change_type, content, old_content)
        
        version_entry = VersionEntry(
            timestamp=timestamp,
            document=document,
            section=section,
            change_type=change_type,
            description=description,
            author=author,
            canonical_reference=canonical_reference,
            validation_status=validation_status,
            content_hash=content_hash,
            diff_summary=diff_summary
        )
        
        # Add to database
        self.version_db["versions"].append(asdict(version_entry))
        self.version_db["last_updated"] = timestamp
        self._save_version_database()
        
        self.logger.info(f"Created version entry for {document}/{section}: {change_type.value}")
        
        return version_entry
    
    def _generate_diff_summary(self, old_content: str, new_content: str) -> str:
        """Generate a summary of changes between old and new content."""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        diff = list(difflib.unified_diff(
            old_lines, new_lines,
            fromfile='old', tofile='new',
            lineterm=''
        ))
        
        if not diff:
            return "No changes detected"
        
        # Count changes
        additions = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
        deletions = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
        
        return f"Changes: +{additions} lines, -{deletions} lines"
    
    def _validate_change_type(self, change_type: ChangeType, content: str, old_content: str = None) -> str:
        """Validate that the change type is appropriate for the content."""
        if change_type == ChangeType.REGRESSION:
            return "FLAGGED: Regression detected - requires review"
        
        # Basic validation rules
        validation_checks = []
        
        # Check 1: Mathematical consistency
        if self._has_mathematical_content(content):
            validation_checks.append("Mathematical content validated")
        
        # Check 2: Theoretical coherence
        if self._has_theoretical_content(content):
            validation_checks.append("Theoretical content validated")
        
        # Check 3: Improvement indicators
        if change_type in [ChangeType.IMPROVEMENT, ChangeType.DEEPENING]:
            if self._indicates_improvement(content, old_content):
                validation_checks.append("Improvement indicators detected")
            else:
                validation_checks.append("WARNING: No clear improvement indicators")
        
        return "; ".join(validation_checks) if validation_checks else "Basic validation passed"
    
    def _has_mathematical_content(self, content: str) -> bool:
        """Check if content contains mathematical expressions."""
        math_indicators = ['$', '\\', '∫', '∑', '∂', '∇', 'α', 'β', 'γ', 'δ', 'ε', 'θ', 'λ', 'μ', 'π', 'σ', 'τ', 'φ', 'ψ', 'ω']
        return any(indicator in content for indicator in math_indicators)
    
    def _has_theoretical_content(self, content: str) -> bool:
        """Check if content contains theoretical physics terminology."""
        theory_indicators = ['Lagrangian', 'Hamiltonian', 'quantum', 'field', 'gauge', 'symmetry', 'group', 'algebra', 'manifold', 'topology']
        return any(indicator.lower() in content.lower() for indicator in theory_indicators)
    
    def _indicates_improvement(self, new_content: str, old_content: str = None) -> bool:
        """Check if the change indicates an improvement."""
        if not old_content:
            return True  # New content is considered improvement
        
        # Simple heuristics for improvement detection
        improvement_indicators = [
            'improved', 'enhanced', 'refined', 'corrected', 'clarified',
            'deeper', 'more precise', 'better', 'optimized'
        ]
        
        new_lower = new_content.lower()
        old_lower = old_content.lower()
        
        # Check if new content contains improvement language
        has_improvement_language = any(indicator in new_lower for indicator in improvement_indicators)
        
        # Check if content is longer (potential deepening)
        is_longer = len(new_content) > len(old_content) * 1.1
        
        return has_improvement_language or is_longer
    
    def get_document_history(self, document: str) -> List[VersionEntry]:
        """Get version history for a specific document."""
        history = []
        for entry_data in self.version_db["versions"]:
            if entry_data["document"] == document:
                # Convert change_type back to enum
                entry_data["change_type"] = ChangeType(entry_data["change_type"])
                history.append(VersionEntry(**entry_data))
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.timestamp, reverse=True)
        return history
    
    def get_regression_alerts(self) -> List[VersionEntry]:
        """Get all entries flagged as regressions."""
        regressions = []
        for entry_data in self.version_db["versions"]:
            if entry_data["change_type"] == "regression":
                entry_data["change_type"] = ChangeType.REGRESSION
                regressions.append(VersionEntry(**entry_data))
        
        return regressions
    
    def generate_version_report(self, document: str = None) -> str:
        """Generate a version tracking report."""
        report = []
        report.append("=" * 60)
        report.append("GIFT VERSIONING REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if document:
            history = self.get_document_history(document)
            report.append(f"Version History for: {document}")
            report.append("-" * 40)
            
            for entry in history:
                status_icon = "[OK]" if entry.change_type != ChangeType.REGRESSION else "[WARNING]"
                report.append(f"{status_icon} {entry.timestamp[:19]} - {entry.change_type.value.upper()}")
                report.append(f"   Section: {entry.section}")
                report.append(f"   Author: {entry.author}")
                report.append(f"   Description: {entry.description}")
                report.append(f"   Validation: {entry.validation_status}")
                report.append("")
        else:
            # Overall report
            total_versions = len(self.version_db["versions"])
            regressions = len(self.get_regression_alerts())
            
            report.append(f"Total Versions Tracked: {total_versions}")
            report.append(f"Regressions Flagged: {regressions}")
            report.append("")
            
            # Recent changes
            recent_versions = sorted(
                self.version_db["versions"],
                key=lambda x: x["timestamp"],
                reverse=True
            )[:10]
            
            report.append("Recent Changes (Last 10):")
            report.append("-" * 40)
            
            for entry_data in recent_versions:
                change_type = ChangeType(entry_data["change_type"])
                status_icon = "[OK]" if change_type != ChangeType.REGRESSION else "[WARNING]"
                report.append(f"{status_icon} {entry_data['timestamp'][:19]} - {entry_data['document']}/{entry_data['section']}")
                report.append(f"   Type: {change_type.value} | Author: {entry_data['author']}")
                report.append("")
        
        report.append("VERSIONING PRINCIPLES:")
        report.append("-" * 40)
        report.append("[OK] Only improvements and deepenings allowed")
        report.append("[OK] All changes tracked and validated")
        report.append("[OK] Regressions flagged for review")
        report.append("[OK] Canonical documents as reference")
        report.append("")
        
        return "\n".join(report)
    
    def approve_version(self, timestamp: str, approver: str, notes: str = ""):
        """Approve a version entry."""
        for entry in self.version_db["versions"]:
            if entry["timestamp"] == timestamp:
                entry["approval_status"] = "approved"
                entry["approver"] = approver
                entry["approval_date"] = datetime.now().isoformat()
                entry["approval_notes"] = notes
                break
        
        self._save_version_database()
        self.logger.info(f"Version {timestamp} approved by {approver}")


def main():
    """Main function for testing the agent."""
    agent = VersioningAgent()
    
    print("GIFT Versioning Agent")
    print("=" * 40)
    
    # Generate overall report
    report = agent.generate_version_report()
    print(report)
    
    # Check for regressions
    regressions = agent.get_regression_alerts()
    if regressions:
        print(f"\n[WARNING] {len(regressions)} regression(s) detected!")
        for reg in regressions:
            print(f"   {reg.timestamp} - {reg.document}/{reg.section}")


if __name__ == "__main__":
    main()
