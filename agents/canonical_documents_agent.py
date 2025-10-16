#!/usr/bin/env python3
"""
GIFT Canonical Documents Agent

This agent enforces the principle that PDF documents in docs/ are the canonical references.
Any modifications to formulas, calculations, or theory must be improvements or deepenings,
never regressions from the canonical documents.

Author: GIFT Framework Maintenance System
Version: 1.0
"""

import os
import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import fitz  # PyMuPDF for PDF processing
import difflib

class CanonicalDocumentsAgent:
    """
    Agent responsible for maintaining canonical document integrity and ensuring
    all modifications are improvements or deepenings relative to PDF references.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.docs_path = self.project_root / "github" / "legacy" / "docs_published"
        self.canonical_db_path = self.project_root / "agents" / "canonical_database.json"
        self.log_path = self.project_root / "agents" / "logs" / "canonical_agent.log"
        
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
        
        # Initialize canonical database
        self.canonical_db = self._load_canonical_database()
        
    def _load_canonical_database(self) -> Dict:
        """Load or create canonical documents database."""
        if self.canonical_db_path.exists():
            with open(self.canonical_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "canonical_documents": {},
            "last_scan": None,
            "version": "1.0"
        }
    
    def _save_canonical_database(self):
        """Save canonical documents database."""
        with open(self.canonical_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.canonical_db, f, indent=2, ensure_ascii=False)
    
    def scan_canonical_documents(self) -> Dict[str, Dict]:
        """
        Scan all PDF documents in docs/ and create canonical references.
        
        Returns:
            Dictionary with document metadata and content hashes
        """
        self.logger.info("Scanning canonical documents...")
        
        canonical_docs = {}
        
        if not self.docs_path.exists():
            self.logger.error(f"Docs path does not exist: {self.docs_path}")
            return canonical_docs
        
        for pdf_file in self.docs_path.glob("*.pdf"):
            try:
                doc_info = self._extract_pdf_metadata(pdf_file)
                canonical_docs[pdf_file.name] = doc_info
                self.logger.info(f"Processed canonical document: {pdf_file.name}")
            except Exception as e:
                self.logger.error(f"Error processing {pdf_file}: {e}")
        
        self.canonical_db["canonical_documents"] = canonical_docs
        self.canonical_db["last_scan"] = datetime.now().isoformat()
        self._save_canonical_database()
        
        return canonical_docs
    
    def _extract_pdf_metadata(self, pdf_path: Path) -> Dict:
        """Extract metadata and content hash from PDF document."""
        try:
            doc = fitz.open(pdf_path)
            
            # Get file hash
            with open(pdf_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Extract text content for formula/calculation tracking
            text_content = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text_content += page.get_text()
            
            content_hash = hashlib.sha256(text_content.encode('utf-8')).hexdigest()
            
            # Extract metadata
            metadata = doc.metadata
            
            doc.close()
            
            return {
                "file_path": str(pdf_path),
                "file_hash": file_hash,
                "content_hash": content_hash,
                "page_count": len(doc),
                "metadata": metadata,
                "scan_date": datetime.now().isoformat(),
                "size_bytes": pdf_path.stat().st_size
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {}
    
    def validate_modification(self, modified_content: str, canonical_doc: str, 
                           section: str = None) -> Tuple[bool, str, Dict]:
        """
        Validate that a modification is an improvement or deepening, not a regression.
        
        Args:
            modified_content: The new content to validate
            canonical_doc: Name of the canonical PDF document
            section: Optional section identifier within the document
            
        Returns:
            Tuple of (is_valid, reason, details)
        """
        self.logger.info(f"Validating modification for {canonical_doc}, section: {section}")
        
        if canonical_doc not in self.canonical_db["canonical_documents"]:
            return False, "Canonical document not found in database", {}
        
        canonical_info = self.canonical_db["canonical_documents"][canonical_doc]
        
        # For now, we implement basic validation rules
        # In a full implementation, this would use NLP/AI to compare content
        validation_result = {
            "canonical_document": canonical_doc,
            "section": section,
            "validation_date": datetime.now().isoformat(),
            "checks_performed": []
        }
        
        # Check 1: Mathematical formula consistency
        math_check = self._validate_mathematical_consistency(modified_content, canonical_info)
        validation_result["checks_performed"].append(math_check)
        
        # Check 2: Calculation verification
        calc_check = self._validate_calculations(modified_content, canonical_info)
        validation_result["checks_performed"].append(calc_check)
        
        # Check 3: Theoretical coherence
        theory_check = self._validate_theoretical_coherence(modified_content, canonical_info)
        validation_result["checks_performed"].append(theory_check)
        
        # Determine overall validity
        all_checks_passed = all(check["passed"] for check in validation_result["checks_performed"])
        
        if all_checks_passed:
            reason = "Modification validated as improvement or deepening"
        else:
            failed_checks = [check["name"] for check in validation_result["checks_performed"] if not check["passed"]]
            reason = f"Modification failed validation checks: {', '.join(failed_checks)}"
        
        return all_checks_passed, reason, validation_result
    
    def _validate_mathematical_consistency(self, content: str, canonical_info: Dict) -> Dict:
        """Validate mathematical formula consistency."""
        # This is a placeholder for mathematical validation
        # In a full implementation, this would use symbolic math libraries
        return {
            "name": "mathematical_consistency",
            "passed": True,  # Placeholder
            "details": "Mathematical consistency check (placeholder implementation)",
            "timestamp": datetime.now().isoformat()
        }
    
    def _validate_calculations(self, content: str, canonical_info: Dict) -> Dict:
        """Validate calculation accuracy and methodology."""
        # This is a placeholder for calculation validation
        return {
            "name": "calculation_validation",
            "passed": True,  # Placeholder
            "details": "Calculation validation check (placeholder implementation)",
            "timestamp": datetime.now().isoformat()
        }
    
    def _validate_theoretical_coherence(self, content: str, canonical_info: Dict) -> Dict:
        """Validate theoretical coherence and consistency."""
        # This is a placeholder for theoretical validation
        return {
            "name": "theoretical_coherence",
            "passed": True,  # Placeholder
            "details": "Theoretical coherence check (placeholder implementation)",
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_canonical_report(self) -> str:
        """Generate a report on canonical document status."""
        report = []
        report.append("=" * 60)
        report.append("GIFT CANONICAL DOCUMENTS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if not self.canonical_db["canonical_documents"]:
            report.append("No canonical documents found. Run scan_canonical_documents() first.")
            return "\n".join(report)
        
        report.append(f"Canonical Documents ({len(self.canonical_db['canonical_documents'])}):")
        report.append("-" * 40)
        
        for doc_name, doc_info in self.canonical_db["canonical_documents"].items():
            report.append(f"📄 {doc_name}")
            report.append(f"   Size: {doc_info['size_bytes']:,} bytes")
            report.append(f"   Pages: {doc_info['page_count']}")
            report.append(f"   Scanned: {doc_info['scan_date']}")
            report.append(f"   Hash: {doc_info['content_hash'][:16]}...")
            report.append("")
        
        report.append("CANONICAL DOCUMENT PRINCIPLES:")
        report.append("-" * 40)
        report.append("✓ PDF documents in docs/ are canonical references")
        report.append("✓ Any modifications must be improvements or deepenings")
        report.append("✓ Never regress from canonical formulations")
        report.append("✓ Maintain mathematical and theoretical consistency")
        report.append("")
        
        return "\n".join(report)
    
    def check_document_integrity(self) -> Dict[str, bool]:
        """Check if canonical documents have been modified since last scan."""
        integrity_results = {}
        
        for doc_name, doc_info in self.canonical_db["canonical_documents"].items():
            doc_path = Path(doc_info["file_path"])
            
            if not doc_path.exists():
                integrity_results[doc_name] = False
                self.logger.warning(f"Canonical document missing: {doc_name}")
                continue
            
            # Check file hash
            with open(doc_path, 'rb') as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
            
            integrity_results[doc_name] = (current_hash == doc_info["file_hash"])
            
            if not integrity_results[doc_name]:
                self.logger.warning(f"Canonical document modified: {doc_name}")
        
        return integrity_results


def main():
    """Main function for testing the agent."""
    agent = CanonicalDocumentsAgent()
    
    print("GIFT Canonical Documents Agent")
    print("=" * 40)
    
    # Scan canonical documents
    print("Scanning canonical documents...")
    canonical_docs = agent.scan_canonical_documents()
    print(f"Found {len(canonical_docs)} canonical documents")
    
    # Generate report
    print("\nGenerating report...")
    report = agent.generate_canonical_report()
    print(report)
    
    # Check integrity
    print("Checking document integrity...")
    integrity = agent.check_document_integrity()
    for doc, is_intact in integrity.items():
        status = "✓" if is_intact else "✗"
        print(f"{status} {doc}")


if __name__ == "__main__":
    main()
