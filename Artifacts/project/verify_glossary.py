"""Quick script to verify glossary updates"""
from migrate_and_cleanup import ContentMigrator, MigrationConfig
from pathlib import Path
import sys

migrator = ContentMigrator(MigrationConfig())
file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('test_glossary/test_glossary.md')

result = migrator.verify_glossary_updates(file_path)
print(f"Verification passed: {result['verification_passed']}")
print(f"Remaining terms: {result.get('remaining_healthcare_terms', [])}")

