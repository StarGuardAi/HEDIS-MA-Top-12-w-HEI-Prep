"""
Content Migration and Cleanup Tool
Segments 1A-1F: Progressive migration from StarGuardAI to sentinel-analytics

This script handles:
- File discovery and analysis
- Content replacement (organization names, contact info)
- Markdown cleanup and standardization
- Link validation and fixing
- Documentation updates
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class MigrationConfig:
    """Configuration for migration process"""
    def __init__(self):
        self.source_org = 'StarGuardAI'
        self.target_org = 'sentinel-analytics'
        self.new_email = 'reichert.sentinel.ai@gmail.com'
        self.new_linkedin = 'www.linkedin.com/in/sentinel-analytics'


class ContentMigrator:
    """Handles content migration from source to target organization"""
    
    # Domain hashtag mappings
    DOMAIN_HASHTAGS = {
        'procurement-fraud': [
            '#procurementfraud', '#contractfraud', '#bidrigging'
        ],
        'big-data-fusion': [
            '#bigdatafusion', '#lawenforcementanalytics', '#intelligencefusion'
        ],
        'criminal-networks': [
            '#criminalnetworks', '#networkmapping', '#organizedcrime'
        ],
        'financial-fraud': [
            '#financialfraud', '#frauddetection', '#AML'
        ],
        'homeland-security': [
            '#homelandsecurity', '#nationalsecurity', '#threatintelligence'
        ],
        'default': [
            '#lawenforcement', '#intelligence', '#analytics'
        ]
    }
    
    OLD_HASHTAGS = [
        '#healthcare', '#HEDIS', '#qualitymeasures',
        '#healthinsurance', '#compliance', '#populationhealth'
    ]
    
    GLOSSARY_REPLACEMENTS = {
        # Healthcare → Law Enforcement/Intelligence
        'HEDIS': 'Criminal Intelligence Database',
        'quality measures': 'performance metrics',
        'quality measure': 'performance metric',
        'patient': 'subject',
        'patients': 'subjects',
        'healthcare provider': 'law enforcement agency',
        'healthcare providers': 'law enforcement agencies',
        'medical record': 'case file',
        'medical records': 'case files',
        'diagnosis': 'threat assessment',
        'diagnoses': 'threat assessments',
        'treatment plan': 'investigative strategy',
        'treatment plans': 'investigative strategies',
        'care coordination': 'inter-agency coordination',
        'population health': 'community safety',
        'risk stratification': 'risk profiling',
        'claims data': 'incident data',
        'member': 'individual',
        'members': 'individuals',
        'provider network': 'agency network',
        'provider networks': 'agency networks',
    }
    
    FOOTER_TEMPLATE = """

---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
"""
    
    def __init__(self, config: MigrationConfig):
        self.config = config
        self.changes_log = []
    
    def find_all_markdown_files(self, directory: str) -> List[Path]:
        """
        Recursively find all .md files in the specified directory.
        
        Args:
            directory: Root directory to search
            
        Returns:
            List of Path objects for all .md files found
        """
        if not os.path.exists(directory):
            raise ValueError(f"Directory does not exist: {directory}")
        
        if not os.path.isdir(directory):
            raise ValueError(f"Path is not a directory: {directory}")
        
        markdown_files = []
        base_path = Path(directory).resolve()
        
        # Recursively walk through all directories
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    full_path = Path(root) / file
                    markdown_files.append(full_path.resolve())
        
        # Sort files for consistent output
        markdown_files.sort()
        return markdown_files
    
    def display_file_tree(self, files: List[Path], base_dir: str) -> None:
        """
        Display found files in a tree format relative to base directory.
        
        Args:
            files: List of file paths to display
            base_dir: Base directory to use for relative paths
        """
        if not files:
            print("  (no markdown files found)")
            return
        
        base_path = Path(base_dir).resolve()
        
        # Group files by directory for tree display
        file_tree: Dict[Path, List[Path]] = {}
        
        for file_path in files:
            # Get relative path from base
            try:
                rel_path = file_path.relative_to(base_path)
            except ValueError:
                # File is outside base directory, show absolute path
                rel_path = file_path
            
            # Get directory part
            if rel_path.parent == Path('.'):
                directory = Path('.')
            else:
                directory = rel_path.parent
            
            if directory not in file_tree:
                file_tree[directory] = []
            file_tree[directory].append(rel_path.name)
        
        # Display tree structure
        sorted_dirs = sorted(file_tree.keys())
        
        for directory in sorted_dirs:
            # Display directory
            if directory == Path('.'):
                dir_display = "."
            else:
                dir_display = str(directory)
            print(f"\n📁 {dir_display}")
            
            # Display files in this directory
            files_in_dir = sorted(file_tree[directory])
            for filename in files_in_dir:
                print(f"   ├── {filename}")
        
        # Also show a flat list for quick reference
        print(f"\n[INFO] Flat list ({len(files)} files):")
        for file_path in files:
            try:
                rel_path = file_path.relative_to(base_path)
                print(f"   {rel_path}")
            except ValueError:
                print(f"   {file_path}")
    
    def create_backup(self, source_dir: str) -> str:
        """
        Create timestamped backup of source directory.
        
        Args:
            source_dir: Source directory to backup
            
        Returns:
            Path to the created backup directory
        """
        source_path = Path(source_dir).resolve()
        if not source_path.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")
        
        # Create backup directory name with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir_name = f"{source_path.name}_backup_{timestamp}"
        backup_path = source_path.parent / backup_dir_name
        
        # Check if backup already exists (unlikely but possible)
        if backup_path.exists():
            raise ValueError(f"Backup directory already exists: {backup_path}")
        
        print(f"[INFO] Creating backup: {backup_path}")
        
        try:
            # Copy entire directory tree
            shutil.copytree(source_path, backup_path, dirs_exist_ok=False)
            print(f"[OK] Backup created successfully: {backup_path}")
            return str(backup_path)
        except Exception as e:
            # Clean up partial backup if it exists
            if backup_path.exists():
                try:
                    shutil.rmtree(backup_path)
                except:
                    pass
            raise Exception(f"Failed to create backup: {e}")
    
    def check_disk_space(self, directory: str, required_size: int) -> bool:
        """
        Check if sufficient disk space is available.
        
        Args:
            directory: Directory to check space for
            required_size: Required size in bytes
            
        Returns:
            True if sufficient space available, False otherwise
        """
        try:
            stat = shutil.disk_usage(directory)
            available = stat.free
            # Require at least 2x the size for safety
            required = required_size * 2
            return available >= required
        except Exception:
            # If we can't check, assume it's okay (user can proceed)
            return True
    
    def copy_markdown_files(self, source_dir: str, target_dir: str, 
                           dry_run: bool = False) -> List[Path]:
        """
        Copy markdown files from source to target, preserving directory structure.
        
        Args:
            source_dir: Source directory containing markdown files
            target_dir: Target directory for copied files
            dry_run: If True, show what would be copied without copying
            
        Returns:
            List of Path objects for copied files
        """
        source_path = Path(source_dir).resolve()
        target_path = Path(target_dir).resolve()
        
        # Validate source
        if not source_path.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")
        if not source_path.is_dir():
            raise ValueError(f"Source path is not a directory: {source_dir}")
        
        # Check if target exists and handle creation
        if not target_path.exists():
            if dry_run:
                print(f"[DRY-RUN] Would create target directory: {target_dir}")
            else:
                target_path.mkdir(parents=True, exist_ok=False)
                print(f"[INFO] Created target directory: {target_dir}")
        else:
            if target_path.is_file():
                raise ValueError(f"Target path is a file, not a directory: {target_dir}")
            
            # Check if target has any files
            if any(target_path.iterdir()):
                print(f"[WARN] Warning: Target directory is not empty: {target_dir}")
                response = input("   Continue anyway? (yes/no): ")
                if response.lower() not in ('yes', 'y'):
                    raise ValueError("Copy operation cancelled by user")
        
        # Find all markdown files
        source_files = self.find_all_markdown_files(str(source_path))
        
        if not source_files:
            print("[WARN] No markdown files found in source directory")
            return []
        
        # Calculate total size for disk space check
        total_size = sum(f.stat().st_size for f in source_files)
        
        if not dry_run:
            # Check disk space
            if not self.check_disk_space(str(target_path.parent), total_size):
                raise ValueError(
                    f"Insufficient disk space. Required: {total_size / 1024 / 1024:.2f} MB"
                )
            
            # Create target directory if it doesn't exist
            target_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Target directory: {target_path}")
        
        copied_files = []
        source_base = source_path.resolve()
        
        if dry_run:
            print(f"\n[DRY-RUN] Would copy {len(source_files)} files:")
            print("=" * 60)
        else:
            print(f"\n[INFO] Copying {len(source_files)} files...")
            print("=" * 60)
        
        for i, source_file in enumerate(source_files, 1):
            try:
                # Get relative path from source root
                rel_path = source_file.relative_to(source_base)
                
                # Construct target path
                target_file = target_path / rel_path
                
                # Create target directory structure
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                if dry_run:
                    print(f"[{i}/{len(source_files)}] Would copy: {rel_path}")
                    print(f"    └─> {target_file}")
                else:
                    # Copy file, preserving metadata
                    shutil.copy2(source_file, target_file)
                    
                    # Progress indicator
                    if len(source_files) > 10:
                        if i % max(1, len(source_files) // 10) == 0 or i == len(source_files):
                            progress = (i / len(source_files)) * 100
                            print(f"[{i}/{len(source_files)}] {progress:.0f}% - {rel_path}")
                    else:
                        print(f"[{i}/{len(source_files)}] {rel_path}")
                    
                    copied_files.append(target_file)
                    self.changes_log.append({
                        'operation': 'copy',
                        'source': str(source_file),
                        'target': str(target_file),
                        'timestamp': datetime.now().isoformat()
                    })
            
            except PermissionError as e:
                error_msg = f"Permission denied copying {rel_path}: {e}"
                if dry_run:
                    print(f"[WARN] {error_msg}")
                else:
                    raise PermissionError(error_msg)
            except Exception as e:
                error_msg = f"Error copying {rel_path}: {e}"
                if dry_run:
                    print(f"[WARN] {error_msg}")
                else:
                    raise Exception(error_msg)
        
        if dry_run:
            print("=" * 60)
            print(f"[DONE] Dry run complete - no files were copied")
        else:
            print("=" * 60)
            print(f"[OK] Successfully copied {len(copied_files)} files")
        
        return copied_files
    
    def update_organization_references(self, file_path: Path, 
                                      dry_run: bool = False) -> List[Dict]:
        """
        Update organization name references in a file.
        
        Args:
            file_path: Path to the file to update
            dry_run: If True, show changes without modifying file
            
        Returns:
            List of dictionaries describing each change
        """
        changes = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Define replacements (order matters - most specific first)
            replacements = [
                ('StarGuardAI', 'sentinel-analytics'),
                ('StarGuard AI', 'Sentinel Analytics'),
                ('starguardai', 'sentinel-analytics'),
                ('StarGuard', 'Sentinel'),  # Handle partial matches carefully
            ]
            
            # Apply replacements and track changes
            for old_text, new_text in replacements:
                if old_text in content:
                    # Split into lines for accurate line number tracking
                    lines = content.split('\n')
                    
                    # Track each occurrence with line numbers
                    for line_num, line in enumerate(lines, 1):
                        if old_text in line:
                            # Count occurrences in this line
                            count = line.count(old_text)
                            new_line = line.replace(old_text, new_text)
                            
                            # Log the change
                            change = {
                                'file': str(file_path),
                                'line': line_num,
                                'old': old_text,
                                'new': new_text,
                                'original_line': line.strip(),
                                'new_line': new_line.strip(),
                                'count': count
                            }
                            changes.append(change)
                            
                            # Update the line in the list
                            lines[line_num - 1] = new_line
                    
                    # Rebuild content from updated lines for next iteration
                    content = '\n'.join(lines)
            
            # Write file only if not dry-run and changes were made
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes
            
        except UnicodeDecodeError as e:
            # Handle files that aren't UTF-8 (skip them)
            if dry_run:
                print(f"[WARN] Warning: Cannot read {file_path} (encoding issue): {e}")
            return []
        except PermissionError as e:
            error_msg = f"Permission denied reading {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise Exception(error_msg)
        
        return changes
    
    def process_organization_updates(self, target_dir: str, 
                                     dry_run: bool = False) -> Dict:
        """
        Process all files for organization name updates.
        
        Args:
            target_dir: Directory containing files to update
            dry_run: If True, show changes without modifying files
            
        Returns:
            Dictionary with statistics about the operation
        """
        if not os.path.exists(target_dir):
            raise ValueError(f"Target directory does not exist: {target_dir}")
        
        files = self.find_all_markdown_files(target_dir)
        
        results = {
            'files_processed': 0,
            'files_modified': 0,
            'total_changes': 0,
            'changes_by_file': {},
            'errors': []
        }
        
        print(f"\n[INFO] Processing {len(files)} files for organization updates...")
        print("=" * 60)
        
        for i, file_path in enumerate(files, 1):
            try:
                changes = self.update_organization_references(file_path, dry_run)
                results['files_processed'] += 1
                
                if changes:
                    results['files_modified'] += 1
                    results['total_changes'] += len(changes)
                    results['changes_by_file'][str(file_path)] = changes
                    
                    # Add to master change log
                    if not dry_run:
                        self._add_changes_to_log(changes, 'organization_update')
                    
                    if dry_run:
                        print(f"[{i}/{len(files)}] Would update: {file_path.name}")
                        for change in changes:
                            print(f"    Line {change['line']}: '{change['old']}' → '{change['new']}'")
                    else:
                        print(f"[{i}/{len(files)}] Updated: {file_path.name} ({len(changes)} changes)")
                
                # Progress indicator for large batches
                if len(files) > 20:
                    if i % max(1, len(files) // 10) == 0 or i == len(files):
                        progress = (i / len(files)) * 100
                        print(f"[{i}/{len(files)}] {progress:.0f}% processed")
                        
            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                results['errors'].append(error_msg)
                print(f"[WARN] {error_msg}")
        
        print("=" * 60)
        
        if dry_run:
            print(f"[DONE] Dry run complete: {results['files_modified']} files would be modified")
            print(f"   Total changes: {results['total_changes']}")
        else:
            print(f"[OK] Update complete: {results['files_modified']} files modified")
            print(f"   Total changes: {results['total_changes']}")
        
        return results
    
    def update_urls(self, file_path: Path, dry_run: bool = False) -> List[Dict]:
        """
        Update GitHub URLs and links in a file.
        
        Args:
            file_path: Path to the file to update
            dry_run: If True, show changes without modifying file
            
        Returns:
            List of dictionaries describing each change
        """
        changes = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # GitHub URL patterns (case-insensitive)
            github_patterns = [
                (r'github\.com/StarGuardAI', 'github.com/sentinel-analytics'),
                (r'StarGuardAI\.github\.io', 'sentinel-analytics.github.io'),
                (r'github\.com/starguardai', 'github.com/sentinel-analytics'),  # lowercase variant
            ]
            
            # Apply patterns with regex and track changes
            for pattern, replacement in github_patterns:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                
                # Check if pattern exists in content
                if compiled_pattern.search(content):
                    # Split into lines for accurate line number tracking
                    lines = content.split('\n')
                    
                    # Process line by line to track line numbers
                    new_lines = []
                    for line_num, line in enumerate(lines, 1):
                        original_line = line
                        new_line = compiled_pattern.sub(replacement, line)
                        
                        if original_line != new_line:
                            # Find all matches in the line for logging
                            matches = list(compiled_pattern.finditer(original_line))
                            for match in matches:
                                change = {
                                    'file': str(file_path),
                                    'line': line_num,
                                    'type': 'url',
                                    'old': match.group(0),
                                    'new': replacement,
                                    'original_line': original_line.strip(),
                                    'new_line': new_line.strip(),
                                    'pattern': pattern
                                }
                                changes.append(change)
                            
                            new_lines.append(new_line)
                        else:
                            new_lines.append(line)
                    
                    # Update lines and rebuild content for next iteration
                    content = '\n'.join(new_lines)
            
            # Write file only if not dry-run and changes were made
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes
            
        except UnicodeDecodeError as e:
            if dry_run:
                print(f"[WARN] Warning: Cannot read {file_path} (encoding issue): {e}")
            return []
        except PermissionError as e:
            error_msg = f"Permission denied reading {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise Exception(error_msg)
        
        return changes
    
    def update_contact_info(self, file_path: Path, 
                           dry_run: bool = False) -> List[Dict]:
        """
        Update email and LinkedIn references in a file.
        
        Args:
            file_path: Path to the file to update
            dry_run: If True, show changes without modifying file
            
        Returns:
            List of dictionaries describing each change
        """
        changes = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Email patterns - only match organization emails, not personal ones
            # Include both old domain (starguardai) and new domain (sentinel-analytics)
            # to catch emails that may have been partially updated by org name replacement
            email_patterns = [
                (r'[\w\.-]+@starguardai\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                (r'contact@starguardai\.dev', 'reichert.sentinel.ai@gmail.com'),
                (r'info@starguardai\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                (r'hello@starguardai\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                (r'team@starguardai\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                # Patterns for already-updated domain (sentinel-analytics)
                (r'[\w\.-]+@sentinel-analytics\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                (r'contact@sentinel-analytics\.dev', 'reichert.sentinel.ai@gmail.com'),
                (r'info@sentinel-analytics\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                (r'hello@sentinel-analytics\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
                (r'team@sentinel-analytics\.[\w\.]+', 'reichert.sentinel.ai@gmail.com'),
            ]
            
            # LinkedIn patterns - include both old and new organization names
            linkedin_patterns = [
                (r'linkedin\.com/company/starguardai', 'www.linkedin.com/in/sentinel-analytics'),
                (r'linkedin\.com/in/starguardai', 'www.linkedin.com/in/sentinel-analytics'),
                (r'linkedin\.com/company/StarGuardAI', 'www.linkedin.com/in/sentinel-analytics'),
                # Patterns for already-updated organization name
                (r'linkedin\.com/company/sentinel-analytics', 'www.linkedin.com/in/sentinel-analytics'),
            ]
            
            # Apply email patterns
            for pattern, replacement in email_patterns:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                
                if compiled_pattern.search(content):
                    # Split into lines for accurate line number tracking
                    lines = content.split('\n')
                    
                    new_lines = []
                    for line_num, line in enumerate(lines, 1):
                        original_line = line
                        new_line = compiled_pattern.sub(replacement, line)
                        
                        if original_line != new_line:
                            matches = list(compiled_pattern.finditer(original_line))
                            for match in matches:
                                change = {
                                    'file': str(file_path),
                                    'line': line_num,
                                    'type': 'email',
                                    'old': match.group(0),
                                    'new': replacement,
                                    'original_line': original_line.strip(),
                                    'new_line': new_line.strip(),
                                    'pattern': pattern
                                }
                                changes.append(change)
                            
                            new_lines.append(new_line)
                        else:
                            new_lines.append(line)
                    
                    # Rebuild content for next iteration
                    content = '\n'.join(new_lines)
            
            # Apply LinkedIn patterns
            for pattern, replacement in linkedin_patterns:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                
                if compiled_pattern.search(content):
                    # Split into lines for accurate line number tracking
                    lines = content.split('\n')
                    
                    new_lines = []
                    for line_num, line in enumerate(lines, 1):
                        original_line = line
                        new_line = compiled_pattern.sub(replacement, line)
                        
                        if original_line != new_line:
                            matches = list(compiled_pattern.finditer(original_line))
                            for match in matches:
                                change = {
                                    'file': str(file_path),
                                    'line': line_num,
                                    'type': 'linkedin',
                                    'old': match.group(0),
                                    'new': replacement,
                                    'original_line': original_line.strip(),
                                    'new_line': new_line.strip(),
                                    'pattern': pattern
                                }
                                changes.append(change)
                            
                            new_lines.append(new_line)
                        else:
                            new_lines.append(line)
                    
                    # Rebuild content for next iteration
                    content = '\n'.join(new_lines)
            
            # Write file only if not dry-run and changes were made
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes
            
        except UnicodeDecodeError as e:
            if dry_run:
                print(f"[WARN] Warning: Cannot read {file_path} (encoding issue): {e}")
            return []
        except PermissionError as e:
            error_msg = f"Permission denied reading {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise Exception(error_msg)
        
        return changes
    
    def process_url_and_contact_updates(self, target_dir: str, 
                                         dry_run: bool = False) -> Dict:
        """
        Process all files for URL and contact information updates.
        
        Args:
            target_dir: Directory containing files to update
            dry_run: If True, show changes without modifying files
            
        Returns:
            Dictionary with statistics about the operation
        """
        if not os.path.exists(target_dir):
            raise ValueError(f"Target directory does not exist: {target_dir}")
        
        files = self.find_all_markdown_files(target_dir)
        
        results = {
            'files_processed': 0,
            'files_modified': 0,
            'total_changes': 0,
            'url_changes': 0,
            'email_changes': 0,
            'linkedin_changes': 0,
            'changes_by_file': {},
            'errors': []
        }
        
        print(f"\n[INFO] Processing {len(files)} files for URL and contact updates...")
        print("=" * 60)
        
        for i, file_path in enumerate(files, 1):
            try:
                # Process URL updates
                url_changes = self.update_urls(file_path, dry_run)
                
                # Process contact info updates
                contact_changes = self.update_contact_info(file_path, dry_run)
                
                all_changes = url_changes + contact_changes
                results['files_processed'] += 1
                
                if all_changes:
                    results['files_modified'] += 1
                    results['total_changes'] += len(all_changes)
                    results['url_changes'] += len([c for c in all_changes if c.get('type') == 'url'])
                    results['email_changes'] += len([c for c in all_changes if c.get('type') == 'email'])
                    results['linkedin_changes'] += len([c for c in all_changes if c.get('type') == 'linkedin'])
                    results['changes_by_file'][str(file_path)] = all_changes
                    
                    # Add to master change log
                    if not dry_run:
                        self._add_changes_to_log(all_changes, 'url_contact_update')
                    
                    if dry_run:
                        print(f"[{i}/{len(files)}] Would update: {file_path.name}")
                        for change in all_changes:
                            change_type = change.get('type', 'unknown')
                            print(f"    Line {change['line']} [{change_type}]: '{change['old']}' → '{change['new']}'")
                    else:
                        print(f"[{i}/{len(files)}] Updated: {file_path.name} ({len(all_changes)} changes)")
                
                # Progress indicator for large batches
                if len(files) > 20:
                    if i % max(1, len(files) // 10) == 0 or i == len(files):
                        progress = (i / len(files)) * 100
                        print(f"[{i}/{len(files)}] {progress:.0f}% processed")
                        
            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                results['errors'].append(error_msg)
                print(f"[WARN] {error_msg}")
        
        print("=" * 60)
        
        if dry_run:
            print(f"[DONE] Dry run complete: {results['files_modified']} files would be modified")
            print(f"   Total changes: {results['total_changes']}")
            print(f"   URLs: {results['url_changes']}, Emails: {results['email_changes']}, LinkedIn: {results['linkedin_changes']}")
        else:
            print(f"[OK] Update complete: {results['files_modified']} files modified")
            print(f"   Total changes: {results['total_changes']}")
            print(f"   URLs: {results['url_changes']}, Emails: {results['email_changes']}, LinkedIn: {results['linkedin_changes']}")
        
        return results
    
    def detect_primary_domain(self, content: str) -> str:
        """
        Detect which domain this content relates to based on keywords.
        
        Args:
            content: File content to analyze
            
        Returns:
            Domain name (e.g., 'financial-fraud', 'criminal-networks')
        """
        # Normalize content to lowercase for matching
        content_lower = content.lower()
        
        domain_keywords = {
            'procurement-fraud': [
                'procurement', 'contract', 'bidding', 'vendor',
                'bid rigging', 'kickback', 'phantom vendor'
            ],
            'big-data-fusion': [
                'data fusion', 'integration', 'cad', 'rms',
                'multiple sources', 'interoperability', 'system integration'
            ],
            'criminal-networks': [
                'network', 'organized crime', 'gang', 'cartel',
                'trafficking', 'link analysis', 'associate', 'criminal network'
            ],
            'financial-fraud': [
                'fraud', 'transaction', 'money laundering',
                'aml', 'suspicious activity', 'sar', 'financial crime'
            ],
            'homeland-security': [
                'homeland', 'security', 'terrorism', 'threat',
                'infrastructure', 'intelligence', 'attribution', 'national security'
            ]
        }
        
        # Score each domain based on keyword frequency
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences (case-insensitive)
                score += content_lower.count(keyword.lower())
            domain_scores[domain] = score
        
        # Return highest scoring domain, or default if no matches
        if domain_scores and max(domain_scores.values()) > 0:
            return max(domain_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'default'
    
    def update_hashtags(self, file_path: Path, 
                       dry_run: bool = False) -> List[Dict]:
        """
        Replace old healthcare hashtags with domain-appropriate ones.
        
        Args:
            file_path: Path to the file to update
            dry_run: If True, show changes without modifying file
            
        Returns:
            List of dictionaries describing each change
        """
        changes = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Detect primary domain
            domain = self.detect_primary_domain(content)
            new_hashtags = self.DOMAIN_HASHTAGS.get(domain, self.DOMAIN_HASHTAGS['default'])[:3]
            
            # Find hashtag sections (usually 2+ hashtags together)
            # Pattern: one or more #hashtag followed by optional whitespace
            hashtag_pattern = r'((?:#\w+\s*){2,})'
            
            # Process line by line for more reliable replacement
            lines = content.split('\n')
            new_lines = []
            
            for line_num, line in enumerate(lines, 1):
                matches = list(re.finditer(hashtag_pattern, line))
                
                if not matches:
                    new_lines.append(line)
                    continue
                
                # Process matches in reverse to preserve positions
                updated_line = line
                line_changes = []
                
                for match in reversed(matches):
                    old_hashtags_text = match.group(0).strip()
                    start_pos = match.start()
                    end_pos = match.end()
                    
                    # Extract hashtags from the matched text
                    old_hashtags_list = re.findall(r'#\w+', old_hashtags_text)
                    
                    # Check if contains old healthcare hashtags
                    has_old_hashtags = any(
                        any(old_tag.lower() == tag.lower() for old_tag in self.OLD_HASHTAGS)
                        for tag in old_hashtags_list
                    )
                    
                    if has_old_hashtags:
                        # Separate old healthcare hashtags from technical hashtags
                        old_healthcare_hashtags = [
                            tag for tag in old_hashtags_list
                            if any(old_tag.lower() == tag.lower() for old_tag in self.OLD_HASHTAGS)
                        ]
                        technical_hashtags = [
                            tag for tag in old_hashtags_list
                            if not any(old_tag.lower() == tag.lower() for old_tag in self.OLD_HASHTAGS)
                        ]
                        
                        # Create new hashtag string
                        # Keep technical hashtags, replace healthcare with domain hashtags
                        new_hashtags_list = technical_hashtags + new_hashtags
                        # Remove duplicates while preserving order
                        seen = set()
                        unique_hashtags = []
                        for tag in new_hashtags_list:
                            tag_lower = tag.lower()
                            if tag_lower not in seen:
                                seen.add(tag_lower)
                                unique_hashtags.append(tag)
                        
                        new_hashtags_text = ' '.join(unique_hashtags[:6])  # Limit to 6 hashtags
                        
                        # Replace the hashtag section in the line
                        updated_line = updated_line[:start_pos] + new_hashtags_text + updated_line[end_pos:]
                        
                        # Log the change
                        change = {
                            'file': str(file_path),
                            'line': line_num,
                            'type': 'hashtag',
                            'domain': domain,
                            'old': old_hashtags_text.strip(),
                            'new': new_hashtags_text.strip(),
                            'old_healthcare': old_healthcare_hashtags,
                            'kept_technical': technical_hashtags,
                            'added_domain': new_hashtags,
                            'original_line': line.strip(),
                            'new_line': updated_line.strip()
                        }
                        line_changes.append(change)
                
                new_lines.append(updated_line)
                changes.extend(line_changes)
            
            # Rebuild content
            content = '\n'.join(new_lines)
            
            # Write file only if not dry-run and changes were made
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes
            
        except UnicodeDecodeError as e:
            if dry_run:
                print(f"[WARN] Warning: Cannot read {file_path} (encoding issue): {e}")
            return []
        except PermissionError as e:
            error_msg = f"Permission denied reading {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise Exception(error_msg)
        
        return changes
    
    def process_hashtag_updates(self, target_dir: str, 
                               dry_run: bool = False) -> Dict:
        """
        Process all files for hashtag updates.
        
        Args:
            target_dir: Directory containing files to update
            dry_run: If True, show changes without modifying files
            
        Returns:
            Dictionary with statistics about the operation
        """
        if not os.path.exists(target_dir):
            raise ValueError(f"Target directory does not exist: {target_dir}")
        
        files = self.find_all_markdown_files(target_dir)
        
        results = {
            'files_processed': 0,
            'files_modified': 0,
            'total_changes': 0,
            'domain_distribution': {},
            'changes_by_file': {},
            'errors': []
        }
        
        print(f"\n[INFO] Processing {len(files)} files for hashtag updates...")
        print("=" * 60)
        
        for i, file_path in enumerate(files, 1):
            try:
                hashtag_changes = self.update_hashtags(file_path, dry_run)
                results['files_processed'] += 1
                
                if hashtag_changes:
                    results['files_modified'] += 1
                    results['total_changes'] += len(hashtag_changes)
                    results['changes_by_file'][str(file_path)] = hashtag_changes
                    
                    # Add to master change log
                    if not dry_run:
                        self._add_changes_to_log(hashtag_changes, 'hashtag_update')
                    
                    # Track domain distribution
                    for change in hashtag_changes:
                        domain = change.get('domain', 'unknown')
                        results['domain_distribution'][domain] = \
                            results['domain_distribution'].get(domain, 0) + 1
                    
                    if dry_run:
                        print(f"[{i}/{len(files)}] Would update: {file_path.name}")
                        for change in hashtag_changes:
                            print(f"    Line {change['line']} [{change['domain']}]: '{change['old']}' → '{change['new']}'")
                    else:
                        print(f"[{i}/{len(files)}] Updated: {file_path.name} ({len(hashtag_changes)} changes)")
                
                # Progress indicator for large batches
                if len(files) > 20:
                    if i % max(1, len(files) // 10) == 0 or i == len(files):
                        progress = (i / len(files)) * 100
                        print(f"[{i}/{len(files)}] {progress:.0f}% processed")
                        
            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                results['errors'].append(error_msg)
                print(f"[WARN] {error_msg}")
        
        print("=" * 60)
        
        if dry_run:
            print(f"[DONE] Dry run complete: {results['files_modified']} files would be modified")
            print(f"   Total changes: {results['total_changes']}")
            if results['domain_distribution']:
                print(f"   Domain distribution: {results['domain_distribution']}")
        else:
            print(f"[OK] Update complete: {results['files_modified']} files modified")
            print(f"   Total changes: {results['total_changes']}")
            if results['domain_distribution']:
                print(f"   Domain distribution: {results['domain_distribution']}")
        
        return results
    
    def _is_in_code_block(self, content: str, position: int) -> bool:
        """
        Check if position is inside a code block (fenced with ``` or ```).
        
        Args:
            content: Full file content
            position: Character position to check
            
        Returns:
            True if inside code block, False otherwise
        """
        # Find all code block delimiters
        code_block_pattern = r'```[^\n]*\n'
        block_starts = []
        block_ends = []
        
        for match in re.finditer(code_block_pattern, content):
            start_pos = match.start()
            # Find the closing delimiter
            remaining_content = content[start_pos + 3:]
            close_match = re.search(r'```', remaining_content)
            
            if close_match:
                end_pos = start_pos + 3 + close_match.end()
                block_starts.append(start_pos)
                block_ends.append(end_pos)
        
        # Check if position is within any code block
        for start, end in zip(block_starts, block_ends):
            if start <= position < end:
                return True
        
        return False
    
    def _is_in_inline_code(self, content: str, position: int) -> bool:
        """
        Check if position is inside inline code (wrapped with `).
        
        Args:
            content: Full file content
            position: Character position to check
            
        Returns:
            True if inside inline code, False otherwise
        """
        # Find all inline code markers before position
        before_position = content[:position]
        # Count backticks - odd number means we're inside inline code
        backtick_count = before_position.count('`')
        
        # Also check if position is between backticks on same line
        line_start = before_position.rfind('\n') + 1
        line_end = content.find('\n', position)
        if line_end == -1:
            line_end = len(content)
        
        line_content = content[line_start:line_end]
        pos_in_line = position - line_start
        
        # Check if position is between backticks on this line
        backtick_positions = [i for i, char in enumerate(line_content) if char == '`']
        
        for i in range(0, len(backtick_positions), 2):
            if i + 1 < len(backtick_positions):
                start = backtick_positions[i]
                end = backtick_positions[i + 1]
                if start < pos_in_line < end:
                    return True
        
        return False
    
    def update_glossary_terms(self, file_path: Path,
                             dry_run: bool = False) -> List[Dict]:
        """
        Update glossary terms with context awareness.
        
        Args:
            file_path: Path to the file to update
            dry_run: If True, show changes without modifying file
            
        Returns:
            List of dictionaries describing each change
        """
        changes = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Sort replacements by length (longest first) to avoid partial matches
            sorted_replacements = sorted(
                self.GLOSSARY_REPLACEMENTS.items(),
                key=lambda x: len(x[0]),
                reverse=True
            )
            
            # Split into lines for line number tracking
            lines = content.split('\n')
            
            # Process each replacement
            for old_term, new_term in sorted_replacements:
                # Use word boundaries to avoid partial matches
                # For multi-word terms, we need to be careful with boundaries
                if ' ' in old_term:
                    # Multi-word term: match as phrase
                    pattern = re.escape(old_term)
                else:
                    # Single word: use word boundaries
                    pattern = r'\b' + re.escape(old_term) + r'\b'
                
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                
                # Find all matches in content
                matches = list(compiled_pattern.finditer(content))
                
                if matches:
                    # Process matches in reverse to preserve positions
                    for match in reversed(matches):
                        start_pos = match.start()
                        end_pos = match.end()
                        
                        # Check if in code block or inline code
                        if self._is_in_code_block(content, start_pos):
                            continue  # Skip code blocks
                        
                        if self._is_in_inline_code(content, start_pos):
                            continue  # Skip inline code
                        
                        # Calculate line number
                        line_num = content[:start_pos].count('\n') + 1
                        line = lines[line_num - 1]
                        
                        # Find position within line
                        line_start = content.rfind('\n', 0, start_pos) + 1
                        pos_in_line = start_pos - line_start
                        
                        # Get matched text
                        matched_text = match.group(0)
                        
                        # Preserve case of first letter
                        if matched_text[0].isupper():
                            new_term_cased = new_term[0].upper() + new_term[1:] if new_term else new_term
                        else:
                            new_term_cased = new_term.lower()
                        
                        # Replace in line
                        new_line = (line[:pos_in_line] + 
                                   new_term_cased + 
                                   line[pos_in_line + len(matched_text):])
                        
                        # Log the change
                        change = {
                            'file': str(file_path),
                            'line': line_num,
                            'type': 'glossary',
                            'old': matched_text,
                            'new': new_term_cased,
                            'original_line': line.strip(),
                            'new_line': new_line.strip()
                        }
                        changes.append(change)
                        
                        # Update the line
                        lines[line_num - 1] = new_line
                        
                        # Rebuild content for next iteration
                        content = '\n'.join(lines)
            
            # Write file only if not dry-run and changes were made
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes
            
        except UnicodeDecodeError as e:
            if dry_run:
                print(f"[WARN] Warning: Cannot read {file_path} (encoding issue): {e}")
            return []
        except PermissionError as e:
            error_msg = f"Permission denied reading {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise Exception(error_msg)
        
        return changes
    
    def verify_glossary_updates(self, file_path: Path) -> Dict:
        """
        Verify no healthcare terms remain in the file.
        
        Args:
            file_path: Path to the file to verify
            
        Returns:
            Dictionary with verification results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            remaining_terms = []
            
            for old_term in self.GLOSSARY_REPLACEMENTS.keys():
                # Use word boundaries for single words
                if ' ' in old_term:
                    pattern = re.escape(old_term)
                else:
                    pattern = r'\b' + re.escape(old_term) + r'\b'
                
                if re.search(pattern, content, re.IGNORECASE):
                    # Check if it's in a code block (these are acceptable)
                    matches = list(re.finditer(pattern, content, re.IGNORECASE))
                    for match in matches:
                        if not self._is_in_code_block(content, match.start()):
                            if not self._is_in_inline_code(content, match.start()):
                                remaining_terms.append(old_term)
                                break
            
            return {
                'file': str(file_path),
                'remaining_healthcare_terms': list(set(remaining_terms)),
                'verification_passed': len(remaining_terms) == 0
            }
        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e),
                'verification_passed': False
            }
    
    def process_glossary_updates(self, target_dir: str,
                                dry_run: bool = False) -> Dict:
        """
        Process all files for glossary term updates.
        
        Args:
            target_dir: Directory containing files to update
            dry_run: If True, show changes without modifying files
            
        Returns:
            Dictionary with statistics about the operation
        """
        if not os.path.exists(target_dir):
            raise ValueError(f"Target directory does not exist: {target_dir}")
        
        files = self.find_all_markdown_files(target_dir)
        
        results = {
            'files_processed': 0,
            'files_modified': 0,
            'total_changes': 0,
            'changes_by_file': {},
            'verification_results': {},
            'errors': []
        }
        
        print(f"\n[INFO] Processing {len(files)} files for glossary updates...")
        print("=" * 60)
        
        for i, file_path in enumerate(files, 1):
            try:
                glossary_changes = self.update_glossary_terms(file_path, dry_run)
                results['files_processed'] += 1
                
                if glossary_changes:
                    results['files_modified'] += 1
                    results['total_changes'] += len(glossary_changes)
                    results['changes_by_file'][str(file_path)] = glossary_changes
                    
                    # Add to master change log
                    if not dry_run:
                        self._add_changes_to_log(glossary_changes, 'glossary_update')
                    
                    if dry_run:
                        print(f"[{i}/{len(files)}] Would update: {file_path.name}")
                        for change in glossary_changes[:5]:  # Show first 5 changes
                            print(f"    Line {change['line']}: '{change['old']}' → '{change['new']}'")
                        if len(glossary_changes) > 5:
                            print(f"    ... and {len(glossary_changes) - 5} more changes")
                    else:
                        print(f"[{i}/{len(files)}] Updated: {file_path.name} ({len(glossary_changes)} changes)")
                
                # Run verification if not dry-run
                if not dry_run:
                    verification = self.verify_glossary_updates(file_path)
                    results['verification_results'][str(file_path)] = verification
                    
                    if not verification.get('verification_passed', False):
                        remaining = verification.get('remaining_healthcare_terms', [])
                        if remaining:
                            print(f"    [WARN] Warning: {len(remaining)} healthcare terms still present")
                
                # Progress indicator for large batches
                if len(files) > 20:
                    if i % max(1, len(files) // 10) == 0 or i == len(files):
                        progress = (i / len(files)) * 100
                        print(f"[{i}/{len(files)}] {progress:.0f}% processed")
                        
            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                results['errors'].append(error_msg)
                print(f"[WARN] {error_msg}")
        
        print("=" * 60)
        
        if dry_run:
            print(f"[DONE] Dry run complete: {results['files_modified']} files would be modified")
            print(f"   Total changes: {results['total_changes']}")
        else:
            print(f"[OK] Update complete: {results['files_modified']} files modified")
            print(f"   Total changes: {results['total_changes']}")
            
            # Summary of verification
            passed = sum(1 for v in results['verification_results'].values() 
                        if v.get('verification_passed', False))
            total_verified = len(results['verification_results'])
            if total_verified > 0:
                print(f"   Verification: {passed}/{total_verified} files passed")
        
        return results
    
    def add_footer(self, file_path: Path, dry_run: bool = False) -> bool:
        """
        Add standard footer to markdown file.
        
        Args:
            file_path: Path to the file to update
            dry_run: If True, show changes without modifying file
            
        Returns:
            True if footer was added, False if already had footer
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if footer already exists
            if 'maintained by Sentinel Analytics' in content:
                return False  # Already has footer
            
            # Check if file ends with newline
            if not content.endswith('\n'):
                content += '\n'
            
            # Add footer
            new_content = content + self.FOOTER_TEMPLATE
            
            # Write if not dry-run
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            return True  # Footer added
            
        except UnicodeDecodeError as e:
            if dry_run:
                print(f"[WARN] Warning: Cannot read {file_path} (encoding issue): {e}")
            return False
        except PermissionError as e:
            error_msg = f"Permission denied reading {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise PermissionError(error_msg)
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            if dry_run:
                print(f"[WARN] {error_msg}")
            else:
                raise Exception(error_msg)
        
        return False
    
    def process_footer_additions(self, target_dir: str,
                                 dry_run: bool = False,
                                 verbose: bool = False) -> Dict:
        """
        Add footers to all markdown files.
        
        Args:
            target_dir: Directory containing files to update
            dry_run: If True, show changes without modifying files
            verbose: If True, show detailed output including files that already have footers
            
        Returns:
            Dictionary with statistics about the operation
        """
        if not os.path.exists(target_dir):
            raise ValueError(f"Target directory does not exist: {target_dir}")
        
        files = self.find_all_markdown_files(target_dir)
        
        results = {
            'files_processed': 0,
            'footers_added': 0,
            'already_had_footer': 0,
            'errors': []
        }
        
        print(f"\n[INFO] Processing {len(files)} files for footer additions...")
        print("=" * 60)
        
        for i, file_path in enumerate(files, 1):
            try:
                added = self.add_footer(file_path, dry_run)
                results['files_processed'] += 1
                
                if added:
                    results['footers_added'] += 1
                    if dry_run:
                        print(f"[{i}/{len(files)}] Would add footer: {file_path.name}")
                    else:
                        print(f"[{i}/{len(files)}] Footer added: {file_path.name}")
                else:
                    results['already_had_footer'] += 1
                    if verbose:
                        print(f"[{i}/{len(files)}] Already has footer: {file_path.name}")
                
                # Progress indicator for large batches
                if len(files) > 20:
                    if i % max(1, len(files) // 10) == 0 or i == len(files):
                        progress = (i / len(files)) * 100
                        print(f"[{i}/{len(files)}] {progress:.0f}% processed")
                        
            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                results['errors'].append(error_msg)
                print(f"[WARN] {error_msg}")
        
        print("=" * 60)
        
        if dry_run:
            print(f"[DONE] Dry run complete: {results['footers_added']} files would get footers")
            print(f"   {results['already_had_footer']} files already have footers")
        else:
            print(f"[OK] Footer addition complete: {results['footers_added']} footers added")
            print(f"   {results['already_had_footer']} files already had footers")
        
        return results
    
    def generate_contact_info_content(self) -> str:
        """
        Generate contact info file content.
        
        Returns:
            Formatted markdown content for org-contact-info.md
        """
        content = f"""## Sentinel Analytics Contact Info

- **Organization:** Sentinel Analytics
- **LinkedIn:** [www.linkedin.com/in/sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics)
- **Email:** reichert.sentinel.ai@gmail.com
- **GitHub:** [github.com/sentinel-analytics](https://github.com/sentinel-analytics)

### Focus Areas

#### 1. Procurement Fraud Detection
Identifying fraudulent procurement activities in government contracts, including bid rigging, phantom vendors, and kickback schemes.

#### 2. Big Data Fusion for Law Enforcement
Integrating disparate data sources (CAD, RMS, NIBRS, OSINT) for comprehensive intelligence analysis.

#### 3. Criminal Network Mapping
Visualizing and analyzing organized crime structures, gang affiliations, and trafficking networks.

#### 4. Financial Fraud Detection
Real-time monitoring and prediction of financial crimes, money laundering, and suspicious activities.

#### 5. Homeland Security Intelligence
Threat analysis, attribution, and risk assessment for national security and critical infrastructure.

### Domain Expertise
- Machine Learning & AI for Law Enforcement
- Graph Analytics for Criminal Networks
- Time-Series Forecasting for Crime Prediction
- Geospatial Analysis & Hotspot Detection
- Cyber Threat Intelligence & Attribution
- Anti-Money Laundering (AML) Analytics
- Fraud Detection & Prevention Systems

### Technology Stack
**Languages:** Python, SQL, TypeScript, JavaScript  
**ML/AI:** scikit-learn, XGBoost, PyTorch, Prophet, TensorFlow  
**Databases:** PostgreSQL, Neo4j, Redis, Elasticsearch  
**Visualization:** D3.js, Mapbox, Plotly, Recharts  
**Backend:** FastAPI, Flask, Django  
**Frontend:** React, Next.js, Tailwind CSS  
**DevOps:** Docker, Kubernetes, AWS, GitHub Actions  

---
*Last Updated: {datetime.now().strftime('%Y-%m-%d')}*

---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
"""
        return content
    
    def create_contact_info_file(self, target_dir: str,
                                 dry_run: bool = False,
                                 verbose: bool = False) -> bool:
        """
        Create org-contact-info.md file in target directory.
        
        Args:
            target_dir: Directory where file should be created
            dry_run: If True, show what would be created without creating file
            verbose: If True, show preview of content in dry-run mode
            
        Returns:
            True if file was created (or would be created in dry-run), False otherwise
        """
        target_path = Path(target_dir)
        if not target_path.exists():
            if dry_run:
                print(f"[DRY-RUN] Would create target directory: {target_dir}")
            else:
                target_path.mkdir(parents=True, exist_ok=False)
                print(f"[INFO] Created target directory: {target_dir}")
        
        file_path = target_path / 'org-contact-info.md'
        
        # Check if file already exists
        if file_path.exists():
            if dry_run:
                print(f"[DRY-RUN] [WARN] {file_path} already exists (would prompt for overwrite)")
                return False
            
            try:
                response = input(f"\n[WARN] {file_path} already exists. Overwrite? (yes/no): ")
                if response.lower() not in ['yes', 'y']:
                    print("   Skipped contact info file creation.")
                    return False
            except (EOFError, KeyboardInterrupt):
                # Handle non-interactive environments
                print("\n   Skipped contact info file creation (non-interactive mode).")
                return False
        
        # Generate content
        content = self.generate_contact_info_content()
        
        # Write file if not dry-run
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Created: {file_path}")
        else:
            print(f"[DRY-RUN] Would create: {file_path}")
            if verbose:
                print("\nPreview of content:")
                print("=" * 60)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("=" * 60)
        
        return True
    
    def _add_changes_to_log(self, changes: List[Dict], change_type: str) -> None:
        """
        Add changes to the master change log with consistent formatting.
        
        Args:
            changes: List of change dictionaries from update methods
            change_type: Type of change (e.g., 'organization_update', 'hashtag_update')
        """
        for change in changes:
            # Standardize change format
            standardized_change = {
                'file': change.get('file', 'unknown'),
                'line': change.get('line', 0),
                'type': change_type,
                'original': change.get('old', change.get('original', '')),
                'updated': change.get('new', change.get('new_line', '')),
                'timestamp': change.get('timestamp', datetime.now().isoformat())
            }
            
            # Add additional context if available
            if 'domain' in change:
                standardized_change['domain'] = change['domain']
            if 'type' in change and change['type'] in ['url', 'email', 'linkedin']:
                standardized_change['subtype'] = change['type']
            
            self.changes_log.append(standardized_change)
    
    def generate_change_log(self, output_path: str) -> None:
        """
        Generate detailed markdown change log.
        
        Args:
            output_path: Path where change log file should be written
        """
        # Ensure output directory exists
        output_file = Path(output_path)
        output_dir = output_file.parent
        if output_dir and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"[INFO] Created output directory: {output_dir}")
        
        if not self.changes_log:
            log_content = f"""# Migration Change Log
## Organization: StarGuardAI → sentinel-analytics
## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

- **Total files processed:** 0
- **Total changes made:** 0

No changes were made during this migration run.

---
*This log was generated automatically by the migration script.*
"""
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            print(f"[INFO] Generated empty change log: {output_path}")
            return
        
        # Count changes by type (support both 'type' and 'operation')
        change_types = {}
        for change in self.changes_log:
            change_type = change.get('type') or change.get('operation', 'unknown')
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        # Get unique files (support entries without explicit 'file')
        unique_files = set(
            (c.get('file') or c.get('target') or c.get('source') or 'unknown')
            for c in self.changes_log
        )
        
        log_content = f"""# Migration Change Log
## Organization: StarGuardAI → sentinel-analytics
## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

- **Total files processed:** {len(unique_files)}
- **Total changes made:** {len(self.changes_log)}
- **Change types:**
"""
        
        for change_type, count in sorted(change_types.items()):
            log_content += f"  - `{change_type}`: {count}\n"
        
        log_content += "\n---\n\n## Detailed Changes\n\n"
        
        # Group changes by file (derive best-available path key)
        files = {}
        for change in self.changes_log:
            file_path = change.get('file') or change.get('target') or change.get('source') or 'unknown'
            if file_path not in files:
                files[file_path] = []
            files[file_path].append(change)
        
        # Format changes by file
        for file_path, changes in sorted(files.items()):
            file_name = Path(file_path).name
            log_content += f"\n### `{file_name}`\n\n"
            log_content += f"**Full Path:** `{file_path}`\n\n"
            log_content += f"**Total Changes:** {len(changes)}\n\n"
            
            # Sort by line number
            changes_sorted = sorted(changes, key=lambda x: x.get('line', 0))
            
            # Group by change type for readability
            changes_by_type = {}
            for change in changes_sorted:
                change_type = change.get('type') or change.get('operation', 'update')
                if change_type not in changes_by_type:
                    changes_by_type[change_type] = []
                changes_by_type[change_type].append(change)
            
            for change_type in sorted(changes_by_type.keys()):
                type_changes = changes_by_type[change_type]
                log_content += f"#### {change_type.replace('_', ' ').title()}\n\n"
                
                for i, change in enumerate(type_changes, 1):
                    # If this is a copy operation, render copy-specific details
                    if (change.get('operation') == 'copy') and ('source' in change or 'target' in change):
                        src = change.get('source', '')
                        tgt = change.get('target', '')
                        ts = change.get('timestamp', '')
                        log_content += f"{i}. Copied file\n"
                        log_content += f"   - **Source:** `{src}`\n"
                        log_content += f"   - **Target:** `{tgt}`\n"
                        if ts:
                            log_content += f"   - **When:** `{ts}`\n"
                        log_content += "\n"
                        continue

                    line = change.get('line', 'N/A')
                    original = change.get('original', '')
                    updated = change.get('updated', '')

                    # Escape markdown special characters in values
                    original_escaped = str(original).replace('|', '\\|').replace('`', '\\`')
                    updated_escaped = str(updated).replace('|', '\\|').replace('`', '\\`')

                    log_content += f"{i}. **Line {line}**\n"
                    log_content += f"   - **Original:** `{original_escaped[:100]}{'...' if len(str(original)) > 100 else ''}`\n"
                    log_content += f"   - **Updated:** `{updated_escaped[:100]}{'...' if len(str(updated)) > 100 else ''}`\n"

                    # Add domain/subtype if available
                    if 'domain' in change:
                        log_content += f"   - **Domain:** `{change['domain']}`\n"
                    if 'subtype' in change:
                        log_content += f"   - **Subtype:** `{change['subtype']}`\n"

                    log_content += "\n"
        
        log_content += "\n---\n"
        log_content += f"\n*This log was generated automatically by the migration script on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.*\n"
        
        # Write log file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"[OK] Generated change log: {output_path}")
    
    def print_summary(self) -> None:
        """
        Print summary statistics to console.
        """
        if not self.changes_log:
            print("\n[STATS] No changes made.")
            return
        
        print("\n" + "="*60)
        print("MIGRATION SUMMARY")
        print("="*60)
        
        files_modified = len(set(c['file'] for c in self.changes_log))
        total_changes = len(self.changes_log)
        
        print(f"\n[OK] Files modified: {files_modified}")
        print(f"[OK] Total changes: {total_changes}")
        
        # Break down by change type
        change_types = {}
        for change in self.changes_log:
            change_type = change.get('type', 'unknown')
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        print("\n[STATS] Changes by type:")
        for change_type, count in sorted(change_types.items()):
            print(f"   - {change_type}: {count}")
        
        print("\n" + "="*60)
    
    def generate_change_summary(self, results: Dict, output_file: Optional[str] = None) -> str:
        """
        Generate human-readable summary of changes.
        
        Args:
            results: Results dictionary from process_organization_updates
            output_file: Optional file path to write summary
            
        Returns:
            Formatted summary string
        """
        summary_parts = []
        summary_parts.append("# Organization Name Migration Summary\n")
        summary_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        summary_parts.append("## Overview\n\n")
        summary_parts.append(f"- **Files Processed:** {results['files_processed']}\n")
        summary_parts.append(f"- **Files Modified:** {results['files_modified']}\n")
        summary_parts.append(f"- **Total Changes:** {results['total_changes']}\n\n")
        
        if results['errors']:
            summary_parts.append("## Errors\n\n")
            for error in results['errors']:
                summary_parts.append(f"- [WARN] {error}\n")
            summary_parts.append("\n")
        
        if results['changes_by_file']:
            summary_parts.append("## Changes by File\n\n")
            
            for file_path, changes in sorted(results['changes_by_file'].items()):
                rel_path = Path(file_path).name
                summary_parts.append(f"### {rel_path}\n\n")
                summary_parts.append(f"**Path:** `{file_path}`\n\n")
                summary_parts.append(f"**Changes:** {len(changes)}\n\n")
                
                # Group changes by line for readability
                changes_by_line = {}
                for change in changes:
                    line_num = change['line']
                    if line_num not in changes_by_line:
                        changes_by_line[line_num] = []
                    changes_by_line[line_num].append(change)
                
                summary_parts.append("| Line | Old Text | New Text |\n")
                summary_parts.append("|------|----------|----------|\n")
                
                for line_num in sorted(changes_by_line.keys()):
                    for change in changes_by_line[line_num]:
                        old_text = change['old'].replace('|', '\\|')
                        new_text = change['new'].replace('|', '\\|')
                        summary_parts.append(f"| {line_num} | `{old_text}` | `{new_text}` |\n")
                
                summary_parts.append("\n")
                
                # Show context for each change
                summary_parts.append("<details>\n<summary>View line context</summary>\n\n")
                for line_num in sorted(changes_by_line.keys()):
                    for change in changes_by_line[line_num]:
                        summary_parts.append(f"**Line {line_num}:**\n")
                        summary_parts.append(f"- Before: `{change['original_line'][:80]}...`\n")
                        summary_parts.append(f"- After:  `{change['new_line'][:80]}...`\n\n")
                summary_parts.append("</details>\n\n")
        
        summary_text = ''.join(summary_parts)
        
        # Write to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(summary_text)
            print(f"[INFO] Change summary written to: {output_file}")
        
        return summary_text
    
    def verify_migration(self, target_dir: str) -> Dict:
        """
        Run verification checks on migrated content.
        
        Args:
            target_dir: Directory containing migrated files
            
        Returns:
            Dictionary with verification results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'target_directory': str(Path(target_dir).resolve()),
            'checks': []
        }
        
        files = self.find_all_markdown_files(target_dir)
        
        # Check 1: No old organization references
        old_org_refs = self._check_old_org_references(files)
        results['checks'].append({
            'name': 'Old Organization References',
            'passed': len(old_org_refs) == 0,
            'details': old_org_refs
        })
        
        # Check 2: No old hashtags
        old_hashtags = self._check_old_hashtags(files)
        results['checks'].append({
            'name': 'Healthcare Hashtags Removed',
            'passed': len(old_hashtags) == 0,
            'details': old_hashtags
        })
        
        # Check 3: Footers present
        missing_footers = self._check_footers(files)
        results['checks'].append({
            'name': 'Footers Added',
            'passed': len(missing_footers) == 0,
            'details': missing_footers
        })
        
        # Check 4: Contact info file exists
        contact_file = Path(target_dir) / 'org-contact-info.md'
        results['checks'].append({
            'name': 'Contact Info File',
            'passed': contact_file.exists(),
            'details': str(contact_file) if contact_file.exists() else f'Missing: {contact_file}'
        })
        
        return results
    
    def _check_old_org_references(self, files: List[Path]) -> List[Dict]:
        """
        Check for remaining old organization references.
        
        Args:
            files: List of markdown files to check
            
        Returns:
            List of dictionaries describing issues found
        """
        problems = []
        # Order matters - check more specific patterns first
        patterns = ['StarGuardAI', 'StarGuard AI', 'starguardai', 'StarGuard']
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it's in a code block
                lines = content.split('\n')
                in_code_block = False
                reported_lines = set()  # Track lines already reported
                
                for line_num, line in enumerate(lines, 1):
                    if line.strip().startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    
                    if in_code_block:
                        continue  # Skip code blocks
                    
                    # Check if it's part of a URL (should be okay if it's a reference to old repo)
                    if 'github.com' in line or 'http' in line.lower():
                        continue  # Skip URL references
                    
                    # Check each pattern (most specific first)
                    for pattern in patterns:
                        if pattern in line and line_num not in reported_lines:
                            # Make sure it's not a substring of a longer matched pattern
                            # (e.g., don't report 'StarGuard' if 'StarGuardAI' was already found)
                            if any(longer_pattern in line and pattern != longer_pattern 
                                   for longer_pattern in patterns 
                                   if patterns.index(longer_pattern) < patterns.index(pattern)):
                                continue
                            
                            problems.append({
                                'file': str(file_path),
                                'line': line_num,
                                'issue': f'Contains "{pattern}"'
                            })
                            reported_lines.add(line_num)
                            break  # Only report one pattern per line
            except Exception as e:
                problems.append({
                    'file': str(file_path),
                    'issue': f'Error reading file: {e}'
                })
        
        return problems
    
    def _check_old_hashtags(self, files: List[Path]) -> List[Dict]:
        """
        Check for remaining healthcare hashtags.
        
        Args:
            files: List of markdown files to check
            
        Returns:
            List of dictionaries describing issues found
        """
        problems = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check lines for old hashtags
                lines = content.split('\n')
                line_hashtags = {}  # Track hashtags found per line: {line_num: [hashtags]}
                
                for line_num, line in enumerate(lines, 1):
                    found_hashtags = []
                    for old_hashtag in self.OLD_HASHTAGS:
                        if old_hashtag in line:
                            found_hashtags.append(old_hashtag)
                    
                    if found_hashtags:
                        line_hashtags[line_num] = found_hashtags
                
                # Report issues grouped by line
                for line_num, hashtags in line_hashtags.items():
                    if len(hashtags) == 1:
                        problems.append({
                            'file': str(file_path),
                            'line': line_num,
                            'issue': f'Contains old hashtag "{hashtags[0]}"'
                        })
                    else:
                        # Multiple hashtags on same line
                        hashtag_list = ', '.join(f'"{h}"' for h in hashtags)
                        problems.append({
                            'file': str(file_path),
                            'line': line_num,
                            'issue': f'Contains old hashtags: {hashtag_list}'
                        })
            except Exception as e:
                problems.append({
                    'file': str(file_path),
                    'issue': f'Error reading file: {e}'
                })
        
        return problems
    
    def _check_footers(self, files: List[Path]) -> List[Dict]:
        """
        Check if required footers are present.
        
        Args:
            files: List of markdown files to check
            
        Returns:
            List of files missing footers
        """
        missing = []
        footer_marker = "This file is maintained by Sentinel Analytics"
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if footer_marker not in content:
                    missing.append({
                        'file': str(file_path),
                        'issue': 'Missing standard footer'
                    })
            except Exception as e:
                missing.append({
                    'file': str(file_path),
                    'issue': f'Error reading file: {e}'
                })
        
        return missing
    
    def generate_verification_report(self, target_dir: str,
                                     output_path: str) -> None:
        """
        Generate verification report in markdown format.
        
        Args:
            target_dir: Directory containing migrated files
            output_path: Path where report should be written
        """
        results = self.verify_migration(target_dir)
        
        # Ensure output directory exists
        output_file = Path(output_path)
        output_dir = output_file.parent
        if output_dir and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"[INFO] Created output directory: {output_dir}")
        
        report = f"""# Migration Verification Report

**Date:** {results['timestamp']}  
**Directory:** {results['target_directory']}

---

## Summary

"""
        
        passed_checks = sum(1 for c in results['checks'] if c['passed'])
        total_checks = len(results['checks'])
        
        if passed_checks == total_checks:
            report += "[OK] **All checks passed!**\n\n"
        else:
            failed_count = total_checks - passed_checks
            report += f"[WARN] **{passed_checks}/{total_checks} checks passed** ({failed_count} failed)\n\n"
        
        report += "## Detailed Results\n\n"
        
        for check in results['checks']:
            status = "[OK] PASS" if check['passed'] else "[ERROR] FAIL"
            report += f"### {status}: {check['name']}\n\n"
            
            if not check['passed'] and check['details']:
                report += "**Issues found:**\n\n"
                if isinstance(check['details'], list):
                    # Group by file for readability
                    issues_by_file = {}
                    for detail in check['details']:
                        if isinstance(detail, dict):
                            file_path = detail.get('file', 'unknown')
                            if file_path not in issues_by_file:
                                issues_by_file[file_path] = []
                            
                            line_info = f"Line {detail.get('line', '?')}: " if 'line' in detail else ""
                            issues_by_file[file_path].append(f"{line_info}{detail['issue']}")
                        else:
                            report += f"- {detail}\n"
                    
                    for file_path, issues in issues_by_file.items():
                        report += f"**`{Path(file_path).name}`** ({file_path})\n"
                        for issue in issues:
                            report += f"  - {issue}\n"
                        report += "\n"
                else:
                    report += f"- {check['details']}\n"
            
            if check['passed']:
                report += "No issues found.\n"
            
            report += "\n"
        
        # Add footer
        report += "---\n\n"
        report += f"*This report was generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.*\n"
        
        # Add standard organization footer
        report += self.FOOTER_TEMPLATE
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[OK] Generated verification report: {output_path}")


def main():
    """Main entry point for migration script"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Sentinel Analytics Content Migration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full migration with all operations
  python migrate_and_cleanup.py --source /path/to/StarGuardAI \\
      --target /path/to/sentinel-analytics --all
  
  # Specific operations only
  python migrate_and_cleanup.py --target /path/to/sentinel-analytics \\
      --update-org --update-hashtags --add-footers
  
  # Dry run to preview changes
  python migrate_and_cleanup.py --target /path/to/sentinel-analytics \\
      --all --dry-run
  
  # Verification only
  python migrate_and_cleanup.py --target /path/to/sentinel-analytics \\
      --verify
  
  # With backup and change log
  python migrate_and_cleanup.py --source /path/to/StarGuardAI \\
      --target /path/to/sentinel-analytics --all --backup \\
      --change-log reports/MIGRATION_LOG.md --summary
        """
    )
    parser.add_argument(
        '--source',
        required=False,
        help='Source directory to process (e.g., path to StarGuardAI repository). Required for most operations except --verify.'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode - only discover and display files without modifying'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output with additional details'
    )
    parser.add_argument(
        '--target',
        required=False,
        help='Target directory for copied files (required for most operations)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be copied without copying'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup of source directory before copying'
    )
    parser.add_argument(
        '--update-org',
        action='store_true',
        help='Update organization names in files (use with --target or standalone)'
    )
    parser.add_argument(
        '--change-log',
        help='Path to write detailed change log file (default: MIGRATION_CHANGELOG.md)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Print summary statistics after migration'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Run verification checks on migrated content (use with --target)'
    )
    parser.add_argument(
        '--update-urls',
        action='store_true',
        help='Update URLs and contact information (use with --target or standalone)'
    )
    parser.add_argument(
        '--update-hashtags',
        action='store_true',
        help='Update hashtags from healthcare to domain-specific (use with --target or standalone)'
    )
    parser.add_argument(
        '--update-glossary',
        action='store_true',
        help='Update glossary terms from healthcare to law enforcement (use with --target or standalone)'
    )
    parser.add_argument(
        '--add-footers',
        action='store_true',
        help='Add standard footer to all markdown files (use with --target or standalone)'
    )
    parser.add_argument(
        '--create-contact-info',
        action='store_true',
        help='Create org-contact-info.md file (use with --target or standalone)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all migration operations: update-org, update-urls, update-hashtags, update-glossary, add-footers, create-contact-info'
    )
    
    args = parser.parse_args()
    
    # Initialize configuration and migrator
    config = MigrationConfig()
    migrator = ContentMigrator(config)
    
    # Handle --all flag
    if args.all:
        args.update_org = True
        args.update_urls = True
        args.update_hashtags = True
        args.update_glossary = True
        args.add_footers = True
        args.create_contact_info = True
    
    # Validate source directory (not required for --verify)
    if not args.verify and not args.source:
        # Most operations require source, except --verify
        print("[ERROR] --source is required for this operation")
        print("[INFO] Use --source to specify source directory or --verify to check existing migration")
        return 1
    
    # Validate source if provided
    if args.source:
        if not os.path.exists(args.source):
            print(f"[ERROR] Source directory does not exist: {args.source}")
            return 1
        if not os.path.isdir(args.source):
            print(f"[ERROR] Source path is not a directory: {args.source}")
            return 1
    
    # Validate target if required
    needs_target = (
        args.target or args.update_org or args.update_urls or
        args.update_hashtags or args.update_glossary or args.add_footers or
        args.create_contact_info or args.verify
    )
    if needs_target and not args.target:
        print("[ERROR] --target is required for this operation")
        print("[INFO] Use --target to specify where files should be created/updated")
        return 1
    
    print(f"[INFO] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if args.all:
        print("[INFO] Running ALL migration operations (--all flag enabled)")
    
    try:
        # Print source info if available
        if args.source:
            print(f"[INFO] Searching for markdown files in: {args.source}")
        
        # Find all markdown files (only if source is provided)
        files = []
        if args.source:
            files = migrator.find_all_markdown_files(args.source)
        
        if args.test:
            # Test mode: only display discovered files
            print(f"\n[OK] Found {len(files)} markdown files:")
            print("=" * 60)
            migrator.display_file_tree(files, args.source)
            print("=" * 60)
            print(f"\n[DONE] Test mode complete - no files were modified")
            if args.verbose:
                print(f"\n[STATS] Statistics:")
                print(f"   Total files: {len(files)}")
                if files:
                    total_size = sum(f.stat().st_size for f in files)
                    print(f"   Total size: {total_size:,} bytes ({total_size / 1024:.2f} KB)")
        
        elif args.verify:
            # Verification mode
            if not args.target:
                print("[ERROR] --verify requires --target to specify directory to verify")
                return 1
            
            target_dir = args.target
            
            try:
                # Generate verification report
                output_path = Path(target_dir) / 'VERIFICATION_REPORT.md'
                if args.change_log:
                    output_path = Path(args.change_log)
                
                migrator.generate_verification_report(target_dir, str(output_path))
                
                # Print summary to console
                results = migrator.verify_migration(target_dir)
                passed_checks = sum(1 for c in results['checks'] if c['passed'])
                total_checks = len(results['checks'])
                
                print("\n" + "=" * 60)
                print("VERIFICATION SUMMARY")
                print("=" * 60)
                print(f"\n[STATS] Checks passed: {passed_checks}/{total_checks}")
                
                for check in results['checks']:
                    status = "[OK] PASS" if check['passed'] else "[ERROR] FAIL"
                    print(f"  {status}: {check['name']}")
                
                if passed_checks < total_checks:
                    print("\n[WARN] Some checks failed. See report for details.")
                else:
                    print("\n[OK] All checks passed!")
                
                print("=" * 60)
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Verification failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.target:
            # Copy mode: copy files to target directory, then apply updates
            # This must be checked before standalone flags to ensure files are copied first
            if not args.dry_run and args.backup:
                # Create backup before copying
                try:
                    backup_path = migrator.create_backup(args.source)
                    print(f"[INFO] Backup available at: {backup_path}\n")
                except Exception as e:
                    print(f"[ERROR] Backup creation failed: {e}")
                    response = input("   Continue without backup? (yes/no): ")
                    if response.lower() not in ('yes', 'y'):
                        print("   Copy operation cancelled")
                        return 1
            
            # Perform copy operation
            try:
                copied_files = migrator.copy_markdown_files(
                    args.source,
                    args.target,
                    dry_run=args.dry_run
                )
                
                # If update-org is also specified, update files after copying
                if args.update_org:
                    print("\n" + "=" * 60)
                    if args.dry_run:
                        print("[INFO] Previewing organization name updates (analyzing source files)...")
                    else:
                        print("[INFO] Updating organization names in copied files...")
                    print("=" * 60)
                    # In dry-run, analyze source files since target doesn't have files yet
                    analysis_dir = args.source if args.dry_run else args.target
                    update_results = migrator.process_organization_updates(
                        analysis_dir,
                        dry_run=args.dry_run
                    )
                    
                    if args.change_log:
                        summary = migrator.generate_change_summary(update_results, args.change_log)
                    elif args.verbose:
                        summary = migrator.generate_change_summary(update_results)
                        print("\n" + summary)
                
                # If update-urls is also specified, update files after copying
                if args.update_urls:
                    print("\n" + "=" * 60)
                    if args.dry_run:
                        print("[INFO] Previewing URL and contact updates (analyzing source files)...")
                    else:
                        print("[INFO] Updating URLs and contact information in copied files...")
                    print("=" * 60)
                    # In dry-run, analyze source files since target doesn't have files yet
                    analysis_dir = args.source if args.dry_run else args.target
                    url_results = migrator.process_url_and_contact_updates(
                        analysis_dir,
                        dry_run=args.dry_run
                    )
                    
                    if args.change_log:
                        summary = migrator.generate_change_summary(url_results, args.change_log)
                    elif args.verbose:
                        summary = migrator.generate_change_summary(url_results)
                        print("\n" + summary)
                
                # If update-hashtags is also specified, update files after copying
                if args.update_hashtags:
                    print("\n" + "=" * 60)
                    if args.dry_run:
                        print("[INFO] Previewing hashtag updates (analyzing source files)...")
                    else:
                        print("[INFO] Updating hashtags in copied files...")
                    print("=" * 60)
                    # In dry-run, analyze source files since target doesn't have files yet
                    analysis_dir = args.source if args.dry_run else args.target
                    hashtag_results = migrator.process_hashtag_updates(
                        analysis_dir,
                        dry_run=args.dry_run
                    )
                    
                    if args.change_log:
                        summary = migrator.generate_change_summary(hashtag_results, args.change_log)
                    elif args.verbose:
                        summary = migrator.generate_change_summary(hashtag_results)
                        print("\n" + summary)
                
                # If update-glossary is also specified, update files after copying
                if args.update_glossary:
                    print("\n" + "=" * 60)
                    if args.dry_run:
                        print("[INFO] Previewing glossary term updates (analyzing source files)...")
                    else:
                        print("[INFO] Updating glossary terms in copied files...")
                    print("=" * 60)
                    # In dry-run, analyze source files since target doesn't have files yet
                    analysis_dir = args.source if args.dry_run else args.target
                    glossary_results = migrator.process_glossary_updates(
                        analysis_dir,
                        dry_run=args.dry_run
                    )
                    
                    if args.change_log:
                        summary = migrator.generate_change_summary(glossary_results, args.change_log)
                    elif args.verbose:
                        summary = migrator.generate_change_summary(glossary_results)
                        print("\n" + summary)
                
                # If add-footers is also specified, add footers after copying
                if args.add_footers:
                    print("\n" + "=" * 60)
                    if args.dry_run:
                        print("[INFO] Previewing footer additions (analyzing source files)...")
                    else:
                        print("[INFO] Adding footers to copied files...")
                    print("=" * 60)
                    # In dry-run, analyze source files since target doesn't have files yet
                    analysis_dir = args.source if args.dry_run else args.target
                    footer_results = migrator.process_footer_additions(
                        analysis_dir,
                        dry_run=args.dry_run,
                        verbose=args.verbose
                    )
                
                # If create-contact-info is also specified, create file after copying
                if args.create_contact_info:
                    print("\n" + "=" * 60)
                    print("[INFO] Creating contact info file...")
                    print("=" * 60)
                    migrator.create_contact_info_file(
                        args.target,
                        dry_run=args.dry_run,
                        verbose=args.verbose
                    )
                
                if args.verbose and copied_files:
                    print(f"\n[STATS] Copy Statistics:")
                    print(f"   Files copied: {len(copied_files)}")
                    total_size = sum(f.stat().st_size for f in copied_files)
                    print(f"   Total size: {total_size:,} bytes ({total_size / 1024:.2f} KB)")
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Copy operation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.create_contact_info:
            # Contact info file creation mode (standalone, without --target copy)
            target_dir = args.target if args.target else args.source
            
            try:
                created = migrator.create_contact_info_file(
                    target_dir,
                    dry_run=args.dry_run,
                    verbose=args.verbose
                )
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                if created:
                    return 0
                else:
                    return 0  # File already exists or skipped
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Contact info file creation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.add_footers:
            # Footer addition mode
            target_dir = args.target if args.target else args.source
            
            try:
                results = migrator.process_footer_additions(
                    target_dir,
                    dry_run=args.dry_run,
                    verbose=args.verbose
                )
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Footer addition failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.update_glossary:
            # Glossary update mode
            target_dir = args.target if args.target else args.source
            
            try:
                results = migrator.process_glossary_updates(
                    target_dir,
                    dry_run=args.dry_run
                )
                
                # Generate change summary if requested
                if args.change_log:
                    summary = migrator.generate_change_summary(results, args.change_log)
                elif args.verbose:
                    summary = migrator.generate_change_summary(results)
                    print("\n" + summary)
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Update operation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.update_hashtags:
            # Hashtag update mode
            target_dir = args.target if args.target else args.source
            
            try:
                results = migrator.process_hashtag_updates(
                    target_dir,
                    dry_run=args.dry_run
                )
                
                # Generate change summary if requested
                if args.change_log:
                    summary = migrator.generate_change_summary(results, args.change_log)
                elif args.verbose:
                    summary = migrator.generate_change_summary(results)
                    print("\n" + summary)
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Update operation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.update_urls:
            # URL and contact info update mode
            target_dir = args.target if args.target else args.source
            
            try:
                results = migrator.process_url_and_contact_updates(
                    target_dir,
                    dry_run=args.dry_run
                )
                
                # Generate change summary if requested
                if args.change_log:
                    summary = migrator.generate_change_summary(results, args.change_log)
                elif args.verbose:
                    summary = migrator.generate_change_summary(results)
                    print("\n" + summary)
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Update operation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        elif args.update_org:
            # Organization update mode: update organization names
            target_dir = args.target if args.target else args.source
            
            try:
                results = migrator.process_organization_updates(
                    target_dir,
                    dry_run=args.dry_run
                )
                
                # Generate change summary if requested
                if args.change_log:
                    summary = migrator.generate_change_summary(results, args.change_log)
                elif args.verbose:
                    summary = migrator.generate_change_summary(results)
                    print("\n" + summary)
                
                # Generate detailed change log if changes were made
                if not args.dry_run and migrator.changes_log:
                    log_path = args.change_log if args.change_log else 'MIGRATION_CHANGELOG.md'
                    migrator.generate_change_log(log_path)
                
                # Print summary if requested
                if args.summary:
                    migrator.print_summary()
                
                return 0
            except ValueError as e:
                print(f"[ERROR] Validation error: {e}")
                return 1
            except PermissionError as e:
                print(f"[ERROR] Permission error: {e}")
                print("   Check file permissions and try again")
                return 1
            except Exception as e:
                print(f"[ERROR] Update operation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        else:
            # No operation specified
            print(f"\n[OK] Found {len(files)} markdown files")
            print("\nUsage:")
            print("  --test          : Discover and display files only")
            print("  --target DIR    : Copy files to target directory")
            print("  --dry-run       : Show what would happen without doing it")
            print("  --backup        : Create backup before copying (use with --target)")
            print("  --update-org    : Update organization names (use with --target or standalone)")
            print("  --update-urls   : Update URLs and contact info (use with --target or standalone)")
            print("  --update-hashtags : Update hashtags domain-specific (use with --target or standalone)")
            print("  --update-glossary : Update glossary terms (use with --target or standalone)")
            print("  --add-footers   : Add standard footer to files (use with --target or standalone)")
            print("  --create-contact-info : Create org-contact-info.md (use with --target or standalone)")
            print("  --change-log    : Path to write change summary log file")
            if args.verbose:
                print(f"\n[STATS] Statistics:")
                print(f"   Total files: {len(files)}")
                if files:
                    total_size = sum(f.stat().st_size for f in files)
                    print(f"   Total size: {total_size:,} bytes ({total_size / 1024:.2f} KB)")
            return 0
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] Error during file discovery: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())

