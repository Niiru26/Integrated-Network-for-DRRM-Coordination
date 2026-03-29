# revert_width.py
import os
import re

def revert_file(filepath):
    """Revert width='stretch' back to use_container_width=True for plotly charts"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Revert: st.plotly_chart(fig) back to st.plotly_chart(fig, use_container_width=True)
        # This pattern matches plotly_chart without any width parameter
        pattern1 = r'st\.plotly_chart\(([^)]+)\)'
        
        def add_container_width(match):
            params = match.group(1).strip()
            # Don't add if it already has use_container_width
            if 'use_container_width' not in params and params:
                return f'st.plotly_chart({params}, use_container_width=True)'
            return match.group(0)
        
        # Only apply to lines that don't already have use_container_width
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'st.plotly_chart(' in line and 'use_container_width' not in line and 'width=' not in line:
                # Add use_container_width=True
                match = re.search(r'st\.plotly_chart\(([^)]+)\)', line)
                if match:
                    params = match.group(1).strip()
                    if params and params != '':
                        new_line = line.replace(f'st.plotly_chart({params})', f'st.plotly_chart({params}, use_container_width=True)')
                        new_lines.append(new_line)
                        changes_made = True
                        continue
            new_lines.append(line)
        
        if changes_made:
            content = '\n'.join(new_lines)
        
        # Also revert any width='stretch' back to use_container_width=True for safety
        content = re.sub(r',\s*width\s*=\s*[\'"]stretch[\'"]', ', use_container_width=True', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    tabs_dir = "tabs"
    
    print("Reverting width='stretch' to use_container_width=True...")
    print("-" * 50)
    
    fixed_count = 0
    for filename in os.listdir(tabs_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(tabs_dir, filename)
            print(f"\nProcessing {filename}...")
            if revert_file(filepath):
                print(f"  ✅ Reverted")
                fixed_count += 1
            else:
                print(f"  ⏭️ No changes needed")
    
    print("\n" + "-" * 50)
    print(f"✅ Reverted {fixed_count} files")
    
    # Also fix app.py
    if os.path.exists("app.py"):
        print("\nProcessing app.py...")
        if revert_file("app.py"):
            print("✅ Reverted app.py")


if __name__ == "__main__":
    main()