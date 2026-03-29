# fix_tabs.py
import os
import re

def fix_tab_file(filepath):
    """Fix a single tab file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove use_container_width=True from plotly_chart
        # Pattern: st.plotly_chart(..., use_container_width=True) or use_container_width=True)
        content = re.sub(
            r'st\.plotly_chart\(([^,)]+),\s*use_container_width\s*=\s*True\s*\)',
            r'st.plotly_chart(\1)',
            content
        )
        
        # Pattern: use_container_width=True as the only parameter or last parameter
        content = re.sub(
            r',\s*use_container_width\s*=\s*True\s*\)',
            r')',
            content
        )
        
        # Fix 2: Replace use_container_width=True with width='stretch' for buttons
        content = re.sub(
            r'st\.button\(([^,)]+),\s*use_container_width\s*=\s*True\s*\)',
            r'st.button(\1, width="stretch")',
            content
        )
        
        content = re.sub(
            r',\s*use_container_width\s*=\s*True\s*\)',
            r', width="stretch")',
            content
        )
        
        # Fix 3: Fix st.form_submit_button (doesn't need width parameter, just remove use_container_width)
        content = re.sub(
            r'st\.form_submit_button\(([^,)]+),\s*use_container_width\s*=\s*True\s*\)',
            r'st.form_submit_button(\1)',
            content
        )
        
        # Fix 4: Fix st.dataframe (just remove use_container_width)
        content = re.sub(
            r'st\.dataframe\(([^,)]+),\s*use_container_width\s*=\s*True\s*\)',
            r'st.dataframe(\1)',
            content
        )
        
        # Fix 5: Fix st.expander (just remove use_container_width if present)
        content = re.sub(
            r'st\.expander\(([^,)]+),\s*use_container_width\s*=\s*True\s*\)',
            r'st.expander(\1)',
            content
        )
        
        # Fix 6: Fix st.columns (doesn't need use_container_width)
        content = re.sub(
            r'st\.columns\(([^,)]+),\s*use_container_width\s*=\s*True\s*\)',
            r'st.columns(\1)',
            content
        )
        
        # Fix 7: Fix st.container (doesn't need use_container_width)
        content = re.sub(
            r'st\.container\([^)]*use_container_width\s*=\s*True[^)]*\)',
            r'st.container()',
            content
        )
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return False


def main():
    """Main function to process all tab files"""
    
    tabs_dir = "tabs"
    
    if not os.path.exists(tabs_dir):
        print(f"Error: {tabs_dir} directory not found!")
        return
    
    # Get all Python files in tabs directory
    tab_files = [f for f in os.listdir(tabs_dir) if f.endswith('.py')]
    
    print(f"Found {len(tab_files)} tab files to process...")
    print("-" * 50)
    
    fixed_count = 0
    for filename in tab_files:
        filepath = os.path.join(tabs_dir, filename)
        print(f"Processing {filename}...")
        
        if fix_tab_file(filepath):
            print(f"  ✅ Fixed")
            fixed_count += 1
        else:
            print(f"  ⏭️ No changes needed")
    
    print("-" * 50)
    print(f"✅ Fixed {fixed_count} files")
    
    # Also fix app.py if needed
    print("\nChecking app.py...")
    if os.path.exists("app.py"):
        if fix_tab_file("app.py"):
            print("✅ Fixed app.py")
        else:
            print("⏭️ No changes needed in app.py")
    else:
        print("⚠️ app.py not found")


if __name__ == "__main__":
    main()