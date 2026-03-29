from supabase import create_client

url = "https://bdzbweytmejqiajnvuea.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkemJ3ZXl0bWVqcWlham52dWVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI4NDQ1MDYsImV4cCI6MjA4ODQyMDUwNn0.B2T4sXA32QGv-hDEvga52iubxF2QZ637IJt9Ao5gL2E"

print("Testing Supabase connection...")
try:
    client = create_client(url, key)
    response = client.table('hazard_events').select('*').limit(1).execute()
    print(f"✅ SUCCESS! Connected to hazard_events table")
    print(f"Found {len(response.data)} events")
    if response.data:
        print("Sample event:", response.data[0])
    else:
        print("Table is empty")
except Exception as e:
    print(f"❌ Error: {e}")