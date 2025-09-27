import schedule
import sys
import time
import pyttsx3
from plyer import notification

engine = pyttsx3.init()

def speak(text):
    """Function to make agent speak."""
    print(f"Agent says: {text}")
    engine.say(text)
    engine.runAndWait()
    
def show_notification(title, message):
    """Function to show desktop notification."""
    notification.notify(
        title=title,
        message=message,
        app_name="Agent",
        timeout=10
    )
    
def morning_routine():
    """Task to be run in the morning."""
    speak("Good morning Bunny! Time to wake up and start your day.")
    show_notification("Morning Routine", "Good morning Bunny! Time to wake up and start your day.")
    
    routine_details = [
        "1. Brush your teeth.",
        "2. Wash your face.",
        "3. Have a healthy breakfast.",
        "4. Review your goals for the day."
    ]
    
    print(routine_details)
    speak("Here is your morning routine:",routine_details)
    
def lunch_reminder():
    """Task to remind for lunch."""
    speak("It's time for lunch! Take a break and enjoy your meal.")
    show_notification("Lunch Reminder", "It's time for lunch! Take a break and enjoy your meal.")

def work_reminder():
    """Task to remind for work."""
    speak("Time to get back to work! Stay focused and productive.")
    show_notification("Work Reminder", "Time to get back to work! Stay focused and productive.")

def evening_routine_windup():
    """Task to be run in the evening."""
    speak("Good evening Bunny! Time to wind down and relax.")
    show_notification("Evening Routine", "Good evening Bunny! Time to wind down and relax.")
    
    routine_details = [
        "1. Reflect on your day.",
        "2. Prepare for tomorrow.",
        "3. Engage in a relaxing activity.",
        "4. Have dinner with family or friends."
    ]
    
    print(routine_details)
    speak("Here is your evening routine:")
    
def bedtime_reminder():
    """Task to remind for bedtime."""
    routine_details = [
        "1. Brush your teeth.",
        "2. Change into comfortable sleepwear.",
        "3. Set an alarm for the next day.",
        "4. Sleep tight."
    ]
    speak("It's time to get ready for bed. A good night's sleep is important!")
    show_notification("Bedtime Reminder", "It's time to get ready for bed. A good night's sleep is important!")
    
def water_remainder():
    """Task to remind for water intake."""
    speak("Remember to drink water regularly to stay hydrated.")
    show_notification("Water Reminder", "Remember to drink water regularly to stay hydrated.")
    
def show_routine():
    """Function to show the entire routine."""
    routine = [
        "Morning Routine at 7:00 AM",
        "Lunch Reminder at 12:30 PM",
        "Work Reminder at 1:30 PM",
        "Evening Routine at 6:00 PM",
        "Bedtime Reminder at 10:30 PM",
        "Water Reminder every hour"
    ]
    return routine

# Schedule tasks
print("your routine Agent is running...")    
speak("Bunny, routine agent is activated. I will notify about your routines.")

# Display today's routine
todays_routine_list = show_routine() 
details_string = "\n".join(todays_routine_list)
print("Your Daily Routine:")
print(details_string)
speak("Here is your daily routine. I have printed the details for you.")

#speaks Tasks according to given time
schedule.every().day.at("07:00").do(morning_routine)
schedule.every().day.at("12:30").do(lunch_reminder)
schedule.every().day.at("13:30").do(work_reminder)
schedule.every().day.at("18:00").do(evening_routine_windup)
schedule.every().day.at("22:30").do(bedtime_reminder)
schedule.every(1).hours.do(water_remainder)

try:
    speak("Agent is now active. Press Ctrl+C to deactivate.")
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    speak("Agent deactivating. Goodbye!")
    print("\nAgent deactivated by user. Goodbye!")
    sys.exit(0)