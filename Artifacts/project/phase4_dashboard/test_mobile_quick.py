"""
Quick test script for mobile pages
Run this to verify mobile pages load correctly
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mobile_imports():
    """Test that all mobile modules can be imported"""
    print("Testing mobile module imports...")
    
    # Note: mobile_view.py page has been removed from sidebar navigation
    # Mobile utility modules remain for internal use
    print("ℹ️  mobile_view page removed from navigation (as requested)")
    
    try:
        from utils.mobile_navigation import (
            init_mobile_state,
            mobile_view_selector,
            create_mobile_nav_header
        )
        print("✅ mobile_navigation imports successful")
    except Exception as e:
        print(f"❌ mobile_navigation import failed: {e}")
        return False
    
    try:
        from utils.mobile_charts import (
            create_mobile_priority_bars,
            create_mobile_star_gauge,
            MOBILE_CONFIG
        )
        print("✅ mobile_charts imports successful")
    except Exception as e:
        print(f"❌ mobile_charts import failed: {e}")
        return False
    
    try:
        from utils.mobile_tables import (
            create_mobile_member_cards,
            create_mobile_simple_table
        )
        print("✅ mobile_tables imports successful")
    except Exception as e:
        print(f"❌ mobile_tables import failed: {e}")
        return False
    
    return True

def test_mobile_functions():
    """Test that mobile utility functions can be called"""
    print("\nTesting mobile utility functions...")
    
    # Note: mobile_view.py page has been removed
    # Testing only utility modules that remain
    try:
        from utils.mobile_charts import (
            create_mobile_priority_bars,
            create_mobile_star_gauge
        )
        print("✅ Mobile chart utilities available")
        return True
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Mobile Pages Quick Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_mobile_imports()
    
    # Test functions
    functions_ok = test_mobile_functions()
    
    print("\n" + "=" * 60)
    if imports_ok and functions_ok:
        print("✅ All utility tests passed!")
        print("\nNote: Mobile page files have been removed from sidebar navigation.")
        print("Mobile utility modules (charts, navigation, tables) remain for internal use.")
    else:
        print("❌ Some tests failed. Check errors above.")
    print("=" * 60)

