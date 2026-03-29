# fix_charts.py
import os
import re

def fix_chart_width(filepath):
    """Fix width='stretch' for plotly charts and dataframes"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Fix 1: st.plotly_chart(..., width='stretch') -> st.plotly_chart(...)
        pattern1 = r'st\.plotly_chart\(([^,)]+),\s*width\s*=\s*[\'"]stretch[\'"]\s*\)'
        if re.search(pattern1, content):
            content = re.sub(pattern1, r'st.plotly_chart(\1)', content)
            changes_made = True
            print(f"    Fixed plotly_chart")
        
        # Fix 2: st.plotly_chart(..., width='stretch') with multiple params
        pattern2 = r',\s*width\s*=\s*[\'"]stretch[\'"]\s*\)'
        if re.search(pattern2, content):
            # Only apply to plotly_chart lines
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if 'plotly_chart' in line and "width='stretch'" in line:
                    line = re.sub(r',\s*width\s*=\s*[\'"]stretch[\'"]\s*\)', r')', line)
                    changes_made = True
                new_lines.append(line)
            content = '\n'.join(new_lines)
        
        # Fix 3: st.dataframe(..., width='stretch') -> st.dataframe(...)
        pattern3 = r'st\.dataframe\(([^,)]+),\s*width\s*=\s*[\'"]stretch[\'"]\s*\)'
        if re.search(pattern3, content):
            content = re.sub(pattern3, r'st.dataframe(\1)', content)
            changes_made = True
            print(f"    Fixed dataframe")
        
        # Keep width='stretch' for buttons (that's correct)
        # Buttons should have width='stretch'
        
        if changes_made:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    """Main function"""
    
    tabs_dir = "tabs"
    
    print("Fixing chart widths in tab files...")
    print("-" * 50)
    
    fixed_count = 0
    for filename in os.listdir(tabs_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(tabs_dir, filename)
            print(f"\nProcessing {filename}...")
            if fix_chart_width(filepath):
                print(f"  ✅ Fixed")
                fixed_count += 1
            else:
                print(f"  ⏭️ No changes needed")
    
    print("\n" + "-" * 50)
    print(f"✅ Fixed {fixed_count} files")
    
    # Also fix app.py
    if os.path.exists("app.py"):
        print("\nProcessing app.py...")
        if fix_chart_width("app.py"):
            print("✅ Fixed app.py")


if __name__ == "__main__":
    main()