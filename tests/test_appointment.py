#!/usr/bin/env python3
"""
Test script to create an appointment using calendar_app.py
"""

import sys, os
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import calendar_app

def create_test_appointment():
    """Creates a test appointment"""
    
    print("🚀 Starting test script to create appointment...")
    print("-" * 50)
    
    try:
        # Configure appointment time (tomorrow at 2:00 PM)
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)  # 1 hour duration
        
        # Appointment data
        client_name = "Maria Gonzalez"
        phone_number = "+1 555 123 4567"
        service_type = "Haircut and styling"
        additional_notes = "Regular client, prefers modern cut. First appointment of the month."
        
        print("📋 Appointment details:")
        print(f"   👤 Client: {client_name}")
        print(f"   📞 Phone: {phone_number}")
        print(f"   🛠️  Service: {service_type}")
        print(f"   📅 Date: {start_time.strftime('%Y-%m-%d')}")
        print(f"   🕐 Time: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
        print(f"   📝 Notes: {additional_notes}")
        print()
        
        print("🔄 Creating appointment in Google Calendar...")
        
        # Create the appointment
        appointment_link = calendar_app.create_appointment(
            client_name=client_name,
            phone_number=phone_number,
            service_type=service_type,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            additional_notes=additional_notes
        )
        
        if appointment_link:
            print("✅ Appointment created successfully!")
            print(f"🔗 Link: {appointment_link}")
            print()
            print("📱 You can share this link with the client")
            print("📅 The appointment will appear in Google Calendar with blue color")
        else:
            print("❌ Error: Could not create appointment")
            
    except Exception as e:
        print(f"❌ Error creating appointment: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        print()
        print("🔧 Possible solutions:")
        print("   - Verify that credentials.json exists and is valid")
        print("   - Verify that CALENDAR_ID is correct")
        print("   - Check your internet connection")

def create_custom_appointment():
    """Creates a custom appointment"""
    
    print("\n" + "="*60)
    print("📝 CUSTOM APPOINTMENT CREATOR")
    print("="*60)
    
    try:
        # Request data from user
        print("Enter appointment details:")
        client_name = input("👤 Client name: ").strip()
        phone_number = input("📞 Phone: ").strip()
        service_type = input("🛠️  Service type: ").strip()
        
        # Date and time
        print("\n📅 When do you want the appointment?")
        days_ahead = input("Days from today (1 for tomorrow, 2 for day after, etc.): ").strip()
        try:
            days_ahead = int(days_ahead)
        except ValueError:
            days_ahead = 1
            print("   Using 1 day (tomorrow) by default")
        
        hour = input("🕐 Hour (24h format, e.g.: 14 for 2:00 PM): ").strip()
        try:
            hour = int(hour)
        except ValueError:
            hour = 10
            print("   Using 10:00 AM by default")
        
        duration = input("⏱️  Duration in minutes (e.g.: 60): ").strip()
        try:
            duration = int(duration)
        except ValueError:
            duration = 60
            print("   Using 60 minutes by default")
        
        additional_notes = input("📝 Additional notes (optional): ").strip()
        
        # Calculate dates
        appointment_date = datetime.now(timezone.utc) + timedelta(days=days_ahead)
        start_time = appointment_date.replace(hour=hour, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=duration)
        
        print(f"\n🔄 Creating appointment for {client_name}...")
        print(f"📅 {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}")
        
        # Create the appointment
        appointment_link = calendar_app.create_appointment(
            client_name=client_name,
            phone_number=phone_number,
            service_type=service_type,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            additional_notes=additional_notes
        )
        
        if appointment_link:
            print("\n✅ Custom appointment created successfully!")
            print(f"🔗 Link: {appointment_link}")
        else:
            print("\n❌ Error: Could not create custom appointment")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Main script function"""
    
    print("🎯 TEST SCRIPT - APPOINTMENT CALENDAR")
    print("="*50)
    print()
    print("Select an option:")
    print("1️⃣  Create automatic test appointment")
    print("2️⃣  Create custom appointment")
    print("0️⃣  Exit")
    print()
    
    while True:
        choice = input("👉 Choose an option (1, 2, or 0): ").strip()
        
        if choice == "1":
            create_test_appointment()
            break
        elif choice == "2":
            create_custom_appointment()
            break
        elif choice == "0":
            print("👋 See you later!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()