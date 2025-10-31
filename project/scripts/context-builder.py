#!/usr/bin/env python3
"""
Context Builder for HEDIS GSD Project
Builds comprehensive context for AI assistants
"""
import os
import json
from pathlib import Path
from datetime import datetime

def build_project_context():
    """Build comprehensive project context"""
    context = {
        'project_name': 'HEDIS GSD Prediction Engine',
        'description': 'AI system for predicting diabetic patients at risk of poor glycemic control',
        'timestamp': datetime.now().isoformat(),
        'phase': 'Phase 1: Foundation & Code Reconstruction',
        'current_task': 'Setting up code review integration',
        'key_files': [],
        'recent_changes': [],
        'next_steps': []
    }
    
    # Key project files
    key_files = [
        'PLAN.md',
        '.cursorrules',
        'docs/healthcare-glossary.md',
        'docs/PROJECT_CONTEXT.md',
        'scripts/hipaa-scanner.py',
        'scripts/pre-commit-checks.sh',
        'tasks/todo.md'
    ]
    
    for file_path in key_files:
        if Path(file_path).exists():
            context['key_files'].append(file_path)
    
    # Recent changes (last 5 commits)
    try:
        import subprocess
        result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            context['recent_changes'] = result.stdout.strip().split('\n')
    except:
        pass
    
    # Next steps based on current phase
    context['next_steps'] = [
        'Complete Phase 1.1: Data Pipeline Reconstruction',
        'Create src/data/ module with data_loader.py',
        'Implement feature_engineering.py',
        'Set up comprehensive testing framework',
        'Begin API development (Phase 2)'
    ]
    
    return context

def save_context(context):
    """Save context to file"""
    with open('docs/ai-context.json', 'w') as f:
        json.dump(context, f, indent=2)

if __name__ == '__main__':
    print("🔧 Building project context...")
    context = build_project_context()
    save_context(context)
    print("✅ Context saved to docs/ai-context.json")
    print(f"📋 Current phase: {context['phase']}")
    print(f"🎯 Current task: {context['current_task']}")
