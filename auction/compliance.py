"""Compliance verification for robot operators.

Stores and checks operator compliance documents: FAA Part 107,
insurance COI, PLS license, SAM.gov registration, DOT prequalification,
and DBE certification.
"""

from __future__ import annotations

from datetime import datetime, timezone
from dataclasses import asdict

from auction.core import ComplianceRecord


VALID_DOC_TYPES = frozenset([
    "faa_part_107",
    "insurance_coi",
    "pls_license",
    "sam_registration",
    "dot_prequalification",
    "dbe_certification",
])

VALID_STATUSES = frozenset(["VERIFIED", "MISSING", "EXPIRED", "NOT_REQUIRED"])


class ComplianceChecker:
    """Manages operator compliance documents and verification checks."""

    def __init__(self) -> None:
        self._records: dict[str, dict[str, ComplianceRecord]] = {}  # robot_id -> {doc_type -> record}

    def upload_document(
        self,
        robot_id: str,
        doc_type: str,
        content: str,
        expires_at: datetime | None = None,
        details: dict | None = None,
    ) -> ComplianceRecord:
        """Store a compliance document for an operator.

        The document is marked as VERIFIED upon upload. In a production system,
        this would trigger async verification against external APIs.
        """
        if doc_type not in VALID_DOC_TYPES:
            raise ValueError(f"doc_type must be one of {sorted(VALID_DOC_TYPES)}, got {doc_type!r}")

        record = ComplianceRecord(
            robot_id=robot_id,
            doc_type=doc_type,
            status="VERIFIED",
            verified_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            details=details or {"content_length": len(content), "uploaded": True},
        )

        if robot_id not in self._records:
            self._records[robot_id] = {}
        self._records[robot_id][doc_type] = record
        return record

    def verify_operator(self, robot_id: str) -> dict:
        """Run all compliance checks for an operator.

        Returns a checklist with status for each document type.
        """
        records = self._records.get(robot_id, {})
        now = datetime.now(timezone.utc)

        checklist = []
        for doc_type in sorted(VALID_DOC_TYPES):
            record = records.get(doc_type)
            if record is None:
                checklist.append({
                    "doc_type": doc_type,
                    "status": "MISSING",
                    "verified_at": None,
                    "expires_at": None,
                    "details": {},
                })
            else:
                # Check expiration
                status = record.status
                if record.expires_at is not None and record.expires_at < now:
                    status = "EXPIRED"
                checklist.append({
                    "doc_type": record.doc_type,
                    "status": status,
                    "verified_at": record.verified_at.isoformat() if record.verified_at else None,
                    "expires_at": record.expires_at.isoformat() if record.expires_at else None,
                    "details": record.details,
                })

        verified_count = sum(1 for c in checklist if c["status"] == "VERIFIED")

        return {
            "robot_id": robot_id,
            "total_checks": len(checklist),
            "verified": verified_count,
            "missing": sum(1 for c in checklist if c["status"] == "MISSING"),
            "expired": sum(1 for c in checklist if c["status"] == "EXPIRED"),
            "compliant": verified_count == len(checklist),
            "checklist": checklist,
        }

    def get_record(self, robot_id: str, doc_type: str) -> ComplianceRecord | None:
        """Get a specific compliance record."""
        return self._records.get(robot_id, {}).get(doc_type)
