#!/usr/bin/env python3
"""
Quick test script - Creates a simple appointment without questions
"""

import sys
import os
from datetime import datetime, timedelta, timezone

# Add parent directory to path to import calendar_app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import calendar_app

def quick_test():
    """Quick test: creates an appointment for tomorrow at 10:00 AM"""
    
    print("⚡ QUICK TEST - Creating test appointment...")
    
    # Configure appointment for tomorrow at 10:00 AM
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    start = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)
    
    print(f"📅 Date: {start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}")
    print("👤 Client: John Doe")
    print("🛠️  Service: Haircut")
    print()
    
    try:
        print("🔄 Creating appointment...")
        
        link = calendar_app.create_appointment(
            client_name="John Doe",
            phone_number="+1 555 987 6543",
            service_type="Haircut",
            start_time=start.isoformat(),
            end_time=end.isoformat(),
            additional_notes="System test appointment"
        )
        
        if link:
            print("✅ Success!")
            print(f"🔗 {link}")
        else:
            print("❌ Error creating appointment")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()