"""
Blockchain-based eKYC Verification System
Implements decentralized identity with credential reuse
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import os

class BlockchainCredential:
    """Represents a verified eKYC credential on blockchain"""
    
    def __init__(self, user_id: str, document_hash: str, verification_data: dict):
        self.user_id = user_id
        self.document_hash = document_hash
        self.verification_data = verification_data
        self.timestamp = datetime.now().isoformat()
        self.credential_hash = self._generate_credential_hash()
    
    def _generate_credential_hash(self) -> str:
        """Generate unique hash for credential (simulates blockchain address)"""
        data = f"{self.user_id}{self.document_hash}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "document_hash": self.document_hash,
            "verification_data": self.verification_data,
            "timestamp": self.timestamp,
            "credential_hash": self.credential_hash
        }

class BlockchainVerifier:
    """Blockchain-based verification system for eKYC"""
    
    def __init__(self, storage_path: str = "blockchain_credentials.json"):
        self.storage_path = storage_path
        self.credentials: Dict[str, BlockchainCredential] = {}
        self.metrics = {
            "total_verifications": 0,
            "reused_verifications": 0,
            "new_verifications": 0,
            "total_verification_time": 0,
            "total_reuse_time": 0,
            "verification_cycles": [],
            "audit_times": []
        }
        self._load_credentials()
    
    def _load_credentials(self):
        """Load existing credentials from storage"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for cred_data in data.get('credentials', []):
                        cred = BlockchainCredential(
                            cred_data['user_id'],
                            cred_data['document_hash'],
                            cred_data['verification_data']
                        )
                        cred.timestamp = cred_data['timestamp']
                        cred.credential_hash = cred_data['credential_hash']
                        self.credentials[cred.credential_hash] = cred
                    self.metrics = data.get('metrics', self.metrics)
            except Exception as e:
                print(f"Warning: Could not load credentials: {e}")
    
    def _save_credentials(self):
        """Save credentials to storage"""
        data = {
            'credentials': [c.to_dict() for c in self.credentials.values()],
            'metrics': self.metrics
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _calculate_document_hash(self, ocr_result: str) -> str:
        """Calculate hash of document content"""
        # Normalize text (remove extra spaces, lowercase)
        normalized = ' '.join(ocr_result.lower().split())
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def check_credential_exists(self, user_id: str, ocr_result: str) -> Optional[BlockchainCredential]:
        """
        Check if credential already exists (VERIFICATION REUSE)
        
        Returns:
            BlockchainCredential if exists, None otherwise
        """
        start_time = time.time()
        
        doc_hash = self._calculate_document_hash(ocr_result)
        
        # Search for existing credential
        for credential in self.credentials.values():
            if credential.user_id == user_id and credential.document_hash == doc_hash:
                elapsed = time.time() - start_time
                self.metrics['total_reuse_time'] += elapsed
                return credential
        
        return None
    
    def verify_and_store(self, user_id: str, ocr_result: str, 
                        verification_data: dict, force_new: bool = False) -> dict:
        """
        Main verification function with blockchain credential management
        
        Args:
            user_id: Unique user identifier
            ocr_result: OCR extracted text
            verification_data: Additional verification data (accuracy, entities, etc.)
            force_new: Force new verification even if credential exists
        
        Returns:
            dict with verification result and metrics
        """
        start_time = time.time()
        self.metrics['total_verifications'] += 1
        
        # Check if credential already exists (REUSE SCENARIO)
        if not force_new:
            existing = self.check_credential_exists(user_id, ocr_result)
            if existing:
                elapsed = time.time() - start_time
                self.metrics['reused_verifications'] += 1
                self.metrics['verification_cycles'].append(0)  # 0 cycles for reuse
                
                print(f"✅ Credential REUSED for {user_id}")
                print(f"   Hash: {existing.credential_hash[:16]}...")
                print(f"   Original timestamp: {existing.timestamp}")
                print(f"   Reuse time: {elapsed*1000:.2f}ms")
                
                self._save_credentials()
                
                return {
                    "status": "REUSED",
                    "credential_hash": existing.credential_hash,
                    "verification_time": elapsed,
                    "original_timestamp": existing.timestamp,
                    "verification_cycles": 0,
                    "verification_data": existing.verification_data
                }
        
        # NEW VERIFICATION (Full processing required)
        doc_hash = self._calculate_document_hash(ocr_result)
        
        # Simulate verification processing cycles
        processing_start = time.time()
        # In real system: OCR processing, entity extraction, validation, etc.
        time.sleep(0.01)  # Simulate minimal processing
        processing_end = time.time()
        
        # Create new credential
        credential = BlockchainCredential(user_id, doc_hash, verification_data)
        self.credentials[credential.credential_hash] = credential
        
        elapsed = time.time() - start_time
        self.metrics['new_verifications'] += 1
        self.metrics['total_verification_time'] += elapsed
        self.metrics['verification_cycles'].append(1)  # 1 cycle for new verification
        
        print(f"🆕 NEW credential created for {user_id}")
        print(f"   Hash: {credential.credential_hash[:16]}...")
        print(f"   Verification time: {elapsed*1000:.2f}ms")
        
        self._save_credentials()
        
        return {
            "status": "NEW",
            "credential_hash": credential.credential_hash,
            "verification_time": elapsed,
            "timestamp": credential.timestamp,
            "verification_cycles": 1,
            "verification_data": verification_data
        }
    
    def audit_credential(self, credential_hash: str) -> dict:
        """
        Audit verification (AUDIT VERIFICATION TIME metric)
        
        This is FAST - just hash verification, no document reprocessing
        """
        start_time = time.time()
        
        credential = self.credentials.get(credential_hash)
        
        elapsed = time.time() - start_time
        self.metrics['audit_times'].append(elapsed)
        
        if credential:
            return {
                "valid": True,
                "audit_time": elapsed,
                "user_id": credential.user_id,
                "timestamp": credential.timestamp,
                "verification_data": credential.verification_data
            }
        else:
            return {
                "valid": False,
                "audit_time": elapsed,
                "error": "Credential not found"
            }
    
    def get_metrics(self) -> dict:
        """
        Calculate blockchain verification metrics for paper
        
        Returns EASR-grade metrics:
        - Verification Reuse Rate
        - Redundant Verification Reduction
        - Effective Latency Reduction
        - Audit Verification Time
        """
        total = self.metrics['total_verifications']
        reused = self.metrics['reused_verifications']
        new = self.metrics['new_verifications']
        
        # A. Verification Reuse Rate
        reuse_rate = (reused / total * 100) if total > 0 else 0
        
        # B. Redundant Verification Reduction
        baseline_cycles = total  # Without blockchain: all requests need full processing
        blockchain_cycles = new  # With blockchain: only new ones need processing
        reduction = baseline_cycles - blockchain_cycles
        reduction_percentage = (reduction / baseline_cycles * 100) if baseline_cycles > 0 else 0
        
        # C. Effective Latency Reduction
        avg_new_latency = (self.metrics['total_verification_time'] / new) if new > 0 else 0
        avg_reuse_latency = (self.metrics['total_reuse_time'] / reused) if reused > 0 else 0
        latency_reduction = avg_new_latency - avg_reuse_latency
        latency_reduction_percentage = (latency_reduction / avg_new_latency * 100) if avg_new_latency > 0 else 0
        
        # D. Audit Verification Time
        avg_audit_time = sum(self.metrics['audit_times']) / len(self.metrics['audit_times']) if self.metrics['audit_times'] else 0
        
        return {
            "total_verifications": total,
            "new_verifications": new,
            "reused_verifications": reused,
            
            # A. Verification Reuse Rate (EASR Priority)
            "verification_reuse_rate_percent": round(reuse_rate, 2),
            
            # B. Redundant Verification Reduction
            "baseline_processing_cycles": baseline_cycles,
            "blockchain_processing_cycles": blockchain_cycles,
            "cycles_eliminated": reduction,
            "reduction_percentage": round(reduction_percentage, 2),
            
            # C. Effective Latency Reduction
            "avg_new_verification_latency_ms": round(avg_new_latency * 1000, 2),
            "avg_reuse_verification_latency_ms": round(avg_reuse_latency * 1000, 2),
            "latency_reduction_ms": round(latency_reduction * 1000, 2),
            "latency_reduction_percentage": round(latency_reduction_percentage, 2),
            
            # D. Audit Verification Time
            "avg_audit_time_ms": round(avg_audit_time * 1000, 2),
            "audit_speedup_vs_full_verification": round(avg_new_latency / avg_audit_time, 2) if avg_audit_time > 0 else 0,
            
            # Storage efficiency
            "unique_credentials_stored": len(self.credentials),
            "storage_efficiency_percent": round((len(self.credentials) / total * 100), 2) if total > 0 else 0
        }
    
    def print_metrics_report(self):
        """Print comprehensive metrics report"""
        metrics = self.get_metrics()
        
        print("\n" + "="*80)
        print("BLOCKCHAIN eKYC VERIFICATION METRICS (EASR-GRADE)")
        print("="*80)
        
        print(f"\n📊 OVERVIEW")
        print(f"  Total Verification Requests: {metrics['total_verifications']}")
        print(f"  New Verifications (Full Processing): {metrics['new_verifications']}")
        print(f"  Reused Verifications (Blockchain): {metrics['reused_verifications']}")
        print(f"  Unique Credentials Stored: {metrics['unique_credentials_stored']}")
        
        print(f"\n✅ A. VERIFICATION REUSE RATE (Primary Metric)")
        print(f"  Reuse Rate: {metrics['verification_reuse_rate_percent']}%")
        print(f"  Formula: ({metrics['reused_verifications']} / {metrics['total_verifications']}) × 100")
        print(f"  Interpretation: {metrics['verification_reuse_rate_percent']}% of verifications avoided full processing")
        
        print(f"\n🔄 B. REDUNDANT VERIFICATION REDUCTION")
        print(f"  Baseline Processing Cycles: {metrics['baseline_processing_cycles']}")
        print(f"  Blockchain-Enabled Cycles: {metrics['blockchain_processing_cycles']}")
        print(f"  Cycles Eliminated: {metrics['cycles_eliminated']}")
        print(f"  Reduction: {metrics['reduction_percentage']}%")
        
        print(f"\n⚡ C. EFFECTIVE LATENCY REDUCTION")
        print(f"  Avg New Verification Latency: {metrics['avg_new_verification_latency_ms']}ms")
        print(f"  Avg Reuse Verification Latency: {metrics['avg_reuse_verification_latency_ms']}ms")
        print(f"  Latency Reduction: {metrics['latency_reduction_ms']}ms ({metrics['latency_reduction_percentage']}%)")
        
        print(f"\n🔍 D. AUDIT VERIFICATION TIME")
        print(f"  Avg Audit Time: {metrics['avg_audit_time_ms']}ms")
        print(f"  Speedup vs Full Verification: {metrics['audit_speedup_vs_full_verification']}x faster")
        
        print(f"\n💾 STORAGE EFFICIENCY")
        print(f"  Storage Efficiency: {metrics['storage_efficiency_percent']}%")
        print(f"  ({metrics['unique_credentials_stored']} credentials for {metrics['total_verifications']} requests)")
        
        print("="*80)

# Example usage function
def demonstrate_blockchain_verification():
    """Demonstrate blockchain verification with sample data"""
    
    print("Initializing Blockchain Verification System...")
    verifier = BlockchainVerifier()
    
    # Sample verification scenarios
    scenarios = [
        # First-time verifications
        ("USER001", "Receipt from Store A Total: RM 100.50", {"accuracy": 85.2, "entities": 5}),
        ("USER002", "Invoice #INV123 Amount: $250.00", {"accuracy": 92.1, "entities": 8}),
        ("USER003", "Receipt Store B Total: RM 75.25", {"accuracy": 78.5, "entities": 4}),
        
        # Repeat verifications (should be REUSED)
        ("USER001", "Receipt from Store A Total: RM 100.50", {"accuracy": 85.2, "entities": 5}),  # REUSE
        ("USER002", "Invoice #INV123 Amount: $250.00", {"accuracy": 92.1, "entities": 8}),  # REUSE
        
        # New verification for existing user
        ("USER001", "Different receipt Total: RM 200.00", {"accuracy": 88.0, "entities": 6}),
        
        # More reuses
        ("USER003", "Receipt Store B Total: RM 75.25", {"accuracy": 78.5, "entities": 4}),  # REUSE
        ("USER001", "Receipt from Store A Total: RM 100.50", {"accuracy": 85.2, "entities": 5}),  # REUSE
    ]
    
    print("\nProcessing verification requests...\n")
    
    for i, (user_id, ocr_text, verification_data) in enumerate(scenarios, 1):
        print(f"Request {i}: {user_id}")
        result = verifier.verify_and_store(user_id, ocr_text, verification_data)
        print()
    
    # Demonstrate audit
    print("\n" + "="*80)
    print("AUDIT DEMONSTRATION")
    print("="*80)
    
    # Get first credential hash
    first_credential_hash = list(verifier.credentials.keys())[0]
    print(f"\nAuditing credential: {first_credential_hash[:16]}...")
    
    audit_result = verifier.audit_credential(first_credential_hash)
    print(f"Audit result: {'✅ VALID' if audit_result['valid'] else '❌ INVALID'}")
    print(f"Audit time: {audit_result['audit_time']*1000:.2f}ms")
    
    # Print comprehensive metrics
    verifier.print_metrics_report()
    
    return verifier

if __name__ == "__main__":
    verifier = demonstrate_blockchain_verification()
