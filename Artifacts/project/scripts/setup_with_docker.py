#!/usr/bin/env python3
"""
Docker-based PostgreSQL Setup and Phase 1 Runner
Automatically starts PostgreSQL in Docker and runs all Phase 1 scripts.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
import subprocess
import time
from pathlib import Path

def check_docker():
    """Check if Docker is installed and running."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[OK] Docker found: {result.stdout.strip()}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("[FAIL] Docker not found or not running")
    print("  Please install Docker Desktop: https://www.docker.com/products/docker-desktop")
    return False

def start_postgres():
    """Start PostgreSQL container."""
    scripts_dir = Path(__file__).parent
    compose_file = scripts_dir / "docker-compose-hedis.yml"
    
    print("\n" + "="*80)
    print("Starting PostgreSQL in Docker...")
    print("="*80)
    
    try:
        # Start container
        result = subprocess.run(
            ["docker-compose", "-f", str(compose_file), "up", "-d"],
            cwd=scripts_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"[FAIL] Failed to start container: {result.stderr}")
            return False
        
        print("[OK] PostgreSQL container starting...")
        
        # Wait for PostgreSQL to be ready
        print("Waiting for PostgreSQL to be ready...")
        max_wait = 30
        waited = 0
        
        while waited < max_wait:
            try:
                result = subprocess.run(
                    ["docker", "exec", "hedis_postgres", "pg_isready", "-U", "hedis_api"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print("[OK] PostgreSQL is ready!")
                    time.sleep(2)  # Give it a moment to fully initialize
                    return True
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                pass
            
            time.sleep(2)
            waited += 2
            print(f"  Waiting... ({waited}/{max_wait} seconds)")
        
        print("[WARN] PostgreSQL may not be fully ready, but continuing...")
        return True
        
    except FileNotFoundError:
        print("[FAIL] docker-compose not found")
        print("  Try: docker compose (without hyphen) or install docker-compose")
        return False
    except Exception as e:
        print(f"[FAIL] Error starting PostgreSQL: {e}")
        return False

def stop_postgres():
    """Stop PostgreSQL container."""
    scripts_dir = Path(__file__).parent
    compose_file = scripts_dir / "docker-compose-hedis.yml"
    
    print("\nStopping PostgreSQL container...")
    try:
        subprocess.run(
            ["docker-compose", "-f", str(compose_file), "down"],
            cwd=scripts_dir,
            capture_output=True,
            timeout=30
        )
        print("[OK] PostgreSQL container stopped")
    except Exception as e:
        print(f"[WARN] Could not stop container: {e}")

def main():
    """Main entry point."""
    print("="*80)
    print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
    print("Docker-based PostgreSQL Setup")
    print("="*80)
    
    if not check_docker():
        return 1
    
    try:
        if not start_postgres():
            return 1
        
        # Wait a moment for connection to stabilize
        time.sleep(3)
        
        # Now run the Phase 1 scripts
        print("\n" + "="*80)
        print("Running Phase 1 Setup Scripts...")
        print("="*80)
        
        scripts_dir = Path(__file__).parent
        runner_script = scripts_dir / "run_all_phase1.py"
        
        result = subprocess.run(
            [sys.executable, str(runner_script)],
            cwd=scripts_dir
        )
        
        if result.returncode == 0:
            print("\n" + "="*80)
            print("[SUCCESS] Phase 1 Setup Complete!")
            print("="*80)
            print("\nPostgreSQL is running in Docker.")
            print("To stop it later, run: docker-compose -f docker-compose-hedis.yml down")
            print("\nNext steps:")
            print("  1. Run validation: python run_validation.py")
            print("  2. Review data quality reports")
            print("  3. Proceed to Phase 2")
            return 0
        else:
            print("\n[FAIL] Phase 1 setup encountered errors")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        stop_postgres()
        return 1
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        stop_postgres()
        return 1

if __name__ == "__main__":
    sys.exit(main())

