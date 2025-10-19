import tkinter as tk
from tkinter import ttk, messagebox
import threading
import schedule
import time
import pyttsx3
from plyer import notification
import sys
from datetime import datetime

class StyledRoutineMateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Routine Mate - Your Personal Assistant")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Control variable for agent status
        self.agent_active = False
        self.schedule_thread = None
        
        # Default schedules
        self.schedules = {
            "morning": "07:00",
            "lunch": "12:30",
            "work": "13:30",
            "evening": "18:00",
            "bedtime": "22:30",
            "water_interval": 1
        }
        
        self.setup_ui()
        
    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        
        style.theme_use('clam')
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'dark': '#2C3E50',
            'light': '#ECF0F1',
            'background': '#F8F9FA'
        }
        
        
        style.configure('Primary.TFrame', background=self.colors['background'])
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground=self.colors['dark'])
        style.configure('Accent.TLabel', font=('Arial', 10), foreground=self.colors['secondary'])
        
        
        style.configure('Primary.TButton', 
                       font=('Arial', 10, 'bold'),
                       background=self.colors['primary'],
                       foreground='white',
                       focuscolor=style.lookup('TButton', 'background'))
        
        style.configure('Success.TButton',
                       font=('Arial', 10, 'bold'),
                       background=self.colors['success'],
                       foreground='white')
        
        style.configure('Danger.TButton',
                       font=('Arial', 10, 'bold'),
                       background=self.colors['danger'],
                       foreground='white')
        
        style.configure('Warning.TButton',
                       font=('Arial', 10, 'bold'),
                       background=self.colors['warning'],
                       foreground='white')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['secondary']),
                           ('pressed', self.colors['secondary'])])

        style.map('Success.TButton',
                 background=[('active', '#219955'),
                           ('pressed', '#219955')])
        
        style.map('Danger.TButton',
                 background=[('active', '#C0392B'),
                           ('pressed', '#C0392B')])
        
    def setup_ui(self):
        main_container = ttk.Frame(self.root, style='Primary.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        
        header_frame = ttk.Frame(main_container, style='Card.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(header_frame, 
                               text="🧠 Routine Mate", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Your Personal Productivity Assistant", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 10))
        
        
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        main_tab = ttk.Frame(notebook, style='Primary.TFrame')
        notebook.add(main_tab, text="📊 Dashboard")
        
        settings_tab = ttk.Frame(notebook, style='Primary.TFrame')
        notebook.add(settings_tab, text="⚙️ Schedule Settings")
        
        self.setup_main_tab(main_tab)
        self.setup_settings_tab(settings_tab)
        
    def setup_main_tab(self, parent):
        control_frame = ttk.Frame(parent, style='Card.TFrame')
        control_frame.pack(fill=tk.X, pady=10, padx=10)
        

        status_header = ttk.Label(control_frame, text="Agent Status", style='Subtitle.TLabel')
        status_header.pack(anchor=tk.W, pady=(10, 5))
     
        status_content = ttk.Frame(control_frame, style='Card.TFrame')
        status_content.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_var = tk.StringVar(value="🔴 Agent is inactive")
        status_label = ttk.Label(status_content, textvariable=self.status_var, 
                                font=('Arial', 12, 'bold'), foreground=self.colors['danger'])
        status_label.pack(side=tk.LEFT)
        button_frame = ttk.Frame(status_content, style='Card.TFrame')
        button_frame.pack(side=tk.RIGHT)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Activate Agent", 
                                      command=self.start_agent, style='Success.TButton')
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="🛑 Deactivate Agent", 
                                     command=self.stop_agent, state=tk.DISABLED, style='Danger.TButton')
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        schedule_frame = ttk.Frame(parent, style='Card.TFrame')
        schedule_frame.pack(fill=tk.X, pady=10, padx=10)
    
        schedule_header = ttk.Label(schedule_frame, text="📅 Current Schedule", style='Subtitle.TLabel')
        schedule_header.pack(anchor=tk.W, pady=(10, 5), padx=10)
        
        self.schedule_display = tk.Text(schedule_frame, height=7, wrap=tk.WORD, 
                                       font=('Arial', 10), bg='white', relief='flat',
                                       borderwidth=1, highlightthickness=1,
                                       highlightbackground=self.colors['light'])
        self.schedule_display.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.update_schedule_display()
        self.schedule_display.config(state=tk.DISABLED)
        
        
        manual_frame = ttk.Frame(parent, style='Card.TFrame')
        manual_frame.pack(fill=tk.X, pady=10, padx=10)
        manual_header = ttk.Label(manual_frame, text="🎮 Manual Controls", style='Subtitle.TLabel')
        manual_header.pack(anchor=tk.W, pady=(10, 5), padx=10)
        
        trigger_buttons = [
            ("🌅 Morning Routine", self.morning_routine),
            ("🍽️ Lunch Reminder", self.lunch_reminder),
            ("💼 Work Reminder", self.work_reminder),
            ("🌇 Evening Routine", self.evening_routine_windup),
            ("🌙 Bedtime Reminder", self.bedtime_reminder),
            ("💧 Water Reminder", self.water_remainder)
        ]
        
        manual_content = ttk.Frame(manual_frame, style='Card.TFrame')
        manual_content.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        for i, (text, command) in enumerate(trigger_buttons):
            btn = ttk.Button(manual_content, text=text, command=command, style='Primary.TButton')
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
            manual_content.grid_columnconfigure(i%3, weight=1)
        
        
        log_frame = ttk.Frame(parent, style='Card.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        log_header = ttk.Label(log_frame, text="📋 Activity Log", style='Subtitle.TLabel')
        log_header.pack(anchor=tk.W, pady=(10, 5), padx=10)
        
        log_text_frame = ttk.Frame(log_frame, style='Card.TFrame')
        log_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        log_scrollbar = ttk.Scrollbar(log_text_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_text_frame, height=10, yscrollcommand=log_scrollbar.set, 
                               wrap=tk.WORD, font=('Consolas', 9), bg='#F8F9FA',
                               relief='solid', borderwidth=1)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.config(command=self.log_text.yview)
        self.log("Application started. Configure schedules in Settings tab.")
        
    def setup_settings_tab(self, parent):
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        
        title_label = ttk.Label(header_frame, text="⚙️ Schedule Configuration", style='Subtitle.TLabel')
        title_label.pack(pady=10)
        
        instructions = ttk.Label(header_frame, 
                                text="Set your preferred times for each routine. Times should be in 24-hour format (HH:MM)", 
                                wraplength=600, justify=tk.CENTER, style='Accent.TLabel')
        instructions.pack(pady=(0, 10))
        
       
        settings_frame = ttk.Frame(parent, style='Card.TFrame')
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        form_container = ttk.Frame(settings_frame, style='Card.TFrame')
        form_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        schedule_configs = [
            ("🌅 Morning Routine:", "morning", "07:00", "(e.g., 07:00)"),
            ("🍽️ Lunch Reminder:", "lunch", "12:30", "(e.g., 12:30)"),
            ("💼 Work Reminder:", "work", "13:30", "(e.g., 13:30)"),
            ("🌇 Evening Routine:", "evening", "18:00", "(e.g., 18:00)"),
            ("🌙 Bedtime Reminder:", "bedtime", "22:30", "(e.g., 22:30)"),
            ("💧 Water Interval:", "water", "1", "(hours, e.g., 1)")
        ]
        
        for i, (label, key, default, hint) in enumerate(schedule_configs):
            row_frame = ttk.Frame(form_container, style='Card.TFrame')
            row_frame.pack(fill=tk.X, pady=8)
            
            ttk.Label(row_frame, text=label, style='Accent.TLabel', width=20).pack(side=tk.LEFT)
            
            if key == "water":
                var = tk.StringVar(value=str(self.schedules["water_interval"]))
                self.water_var = var
                entry = ttk.Entry(row_frame, textvariable=var, width=10, 
                                 font=('Arial', 10))
            else:
                var = tk.StringVar(value=self.schedules[key])
                setattr(self, f"{key}_var", var)
                entry = ttk.Entry(row_frame, textvariable=var, width=10,
                                 font=('Arial', 10))
            
            entry.pack(side=tk.LEFT, padx=10)
            ttk.Label(row_frame, text=hint, style='Accent.TLabel', 
                     foreground='gray').pack(side=tk.LEFT)
        
        # Buttons frame
        button_frame = ttk.Frame(parent, style='Card.TFrame')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="💾 Save Schedule", 
                  command=self.save_schedules, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🔄 Reset to Default", 
                  command=self.reset_schedules, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🧪 Test All Notifications", 
                  command=self.test_all_notifications, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
    def update_schedule_display(self):
        """Update the schedule display in the main tab"""
        self.schedule_display.config(state=tk.NORMAL)
        self.schedule_display.delete(1.0, tk.END)
    
        schedule_text = f"""📅 Your Daily Schedule:

        🌅 Morning Routine:   {self.schedules['morning']:>5}
        🍽️ Lunch Reminder:   {self.schedules['lunch']:>5}
        💼 Work Reminder:    {self.schedules['work']:>5}
        🌇 Evening Routine:   {self.schedules['evening']:>5}
        🌙 Bedtime Reminder: {self.schedules['bedtime']:>5}
        💧 Water Reminder:   Every {self.schedules['water_interval']} hour(s)

        All times are in 24-hour format.
        """
        self.schedule_display.insert(tk.END, schedule_text)
    
        
        self.schedule_display.tag_configure("title", foreground=self.colors['primary'], font=('Arial', 10, 'bold'))
        self.schedule_display.tag_add("title", "1.0", "2.0")
        self.schedule_display.config(state=tk.DISABLED)
        
    def validate_time_format(self, time_str):
        """Validate time format (HH:MM)"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
        
    def save_schedules(self):
        """Save the new schedule settings"""
        if self.agent_active:
            messagebox.showwarning("Warning", "⚠️ Please deactivate agent before changing schedules.")
            return
        times = {
            "morning": self.morning_var.get(),
            "lunch": self.lunch_var.get(),
            "work": self.work_var.get(),
            "evening": self.evening_var.get(),
            "bedtime": self.bedtime_var.get()
        }
        
        for name, time_str in times.items():
            if not self.validate_time_format(time_str):
                messagebox.showerror("Error", f"❌ Invalid time format for {name.replace('_', ' ').title()}.\nPlease use HH:MM format (e.g., 07:30).")
                return
        
        
        try:
            water_interval = int(self.water_var.get())
            if water_interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ Water interval must be a positive integer.")
            return
        
        
        self.schedules.update(times)
        self.schedules["water_interval"] = water_interval
        self.update_schedule_display()
        self.log("✅ Schedules updated successfully.")
        messagebox.showinfo("Success", "✅ Schedules updated successfully!")
        
    def reset_schedules(self):
        """Reset schedules to default values"""
        if self.agent_active:
            messagebox.showwarning("Warning", "⚠️ Please deactivate agent before resetting schedules.")
            return
            
        default_schedules = {
            "morning": "07:00",
            "lunch": "12:30",
            "work": "13:30",
            "evening": "18:00",
            "bedtime": "22:30",
            "water_interval": 1
        }
        
        self.schedules = default_schedules
        self.morning_var.set(default_schedules["morning"])
        self.lunch_var.set(default_schedules["lunch"])
        self.work_var.set(default_schedules["work"])
        self.evening_var.set(default_schedules["evening"])
        self.bedtime_var.set(default_schedules["bedtime"])
        self.water_var.set(str(default_schedules["water_interval"]))
        
        self.update_schedule_display()
        self.log("🔄 Schedules reset to default values.")
        messagebox.showinfo("Success", "✅ Schedules reset to default values!")
        
    def test_all_notifications(self):
        """Test all notifications manually"""
        self.log("🧪 Testing all notifications...")
        self.morning_routine()
        time.sleep(1)
        self.lunch_reminder()
        time.sleep(1)
        self.work_reminder()
        time.sleep(1)
        self.evening_routine_windup()
        time.sleep(1)
        self.bedtime_reminder()
        time.sleep(1)
        self.water_remainder()
        self.log("✅ All notifications tested successfully.")
        
    def log(self, message):
        """Add a timestamped message to the log."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        
     
        if message.startswith("✅"):
            tag = "success"
            self.log_text.tag_config(tag, foreground=self.colors['success'])
        elif message.startswith("❌") or message.startswith("Error"):
            tag = "error"
            self.log_text.tag_config(tag, foreground=self.colors['danger'])
        elif message.startswith("⚠️"):
            tag = "warning"
            self.log_text.tag_config(tag, foreground=self.colors['warning'])
        elif message.startswith("🔴"):
            tag = "inactive"
            self.log_text.tag_config(tag, foreground=self.colors['danger'])
        elif message.startswith("🟢"):
            tag = "active"
            self.log_text.tag_config(tag, foreground=self.colors['success'])
        else:
            tag = "normal"
            self.log_text.tag_config(tag, foreground=self.colors['dark'])
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def speak(self, text):
        """Function to make agent speak."""
        self.log(f"🗣️ {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.log(f"❌ Error in speech: {e}")
            
    def show_notification(self, title, message):
        """Function to show desktop notification."""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Routine Mate",
                timeout=10
            )
            self.log(f"📢 {title} - {message}")
        except Exception as e:
            self.log(f"❌ Error showing notification: {e}")
            
    def morning_routine(self):
        """Task to be run in the morning."""
        self.speak("Good morning! Time to wake up and start your day.")
        self.show_notification("🌅 Morning Routine", "Good morning! Time to wake up and start your day.")
        self.log("🌅 Morning routine triggered")
        
    def lunch_reminder(self):
        """Task to remind for lunch."""
        self.speak("It's time for lunch! Take a break and enjoy your meal.")
        self.show_notification("🍽️ Lunch Reminder", "It's time for lunch! Take a break and enjoy your meal.")
        self.log("🍽️ Lunch reminder triggered")
        
    def work_reminder(self):
        """Task to remind for work."""
        self.speak("Time to get back to work! Stay focused and productive.")
        self.show_notification("💼 Work Reminder", "Time to get back to work! Stay focused and productive.")
        self.log("💼 Work reminder triggered")
        
    def evening_routine_windup(self):
        """Task to be run in the evening."""
        self.speak("Good evening! Time to wind down and relax.")
        self.show_notification("🌇 Evening Routine", "Good evening! Time to wind down and relax.")
        self.log("🌇 Evening routine triggered")
        
    def bedtime_reminder(self):
        """Task to remind for bedtime."""
        self.speak("It's time to get ready for bed. A good night's sleep is important!")
        self.show_notification("🌙 Bedtime Reminder", "It's time to get ready for bed. A good night's sleep is important!")
        self.log("🌙 Bedtime reminder triggered")
        
    def water_remainder(self):
        """Task to remind for water intake."""
        self.speak("Remember to drink water regularly to stay hydrated.")
        self.show_notification("💧 Water Reminder", "Remember to drink water regularly to stay hydrated.")
        self.log("💧 Water reminder triggered")
        
    def run_schedule(self):
        """Run the schedule in a separate thread."""
        while self.agent_active:
            schedule.run_pending()
            time.sleep(1)
            
    def start_agent(self):
        """Start the routine agent with current schedules."""
        if self.agent_active:
            return
            
        self.agent_active = True
        self.status_var.set("🟢 Agent is active")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        schedule.clear()
        
        
        schedule.every().day.at(self.schedules["morning"]).do(self.morning_routine)
        schedule.every().day.at(self.schedules["lunch"]).do(self.lunch_reminder)
        schedule.every().day.at(self.schedules["work"]).do(self.work_reminder)
        schedule.every().day.at(self.schedules["evening"]).do(self.evening_routine_windup)
        schedule.every().day.at(self.schedules["bedtime"]).do(self.bedtime_reminder)
        schedule.every(self.schedules["water_interval"]).hours.do(self.water_remainder)
        
        
        self.schedule_thread = threading.Thread(target=self.run_schedule, daemon=True)
        self.schedule_thread.start()
        self.speak(f"Routine agent is activated. I will notify you according to your schedule.")
        self.log("🟢 Agent activated with current schedule")
        
    def stop_agent(self):
        """Stop the routine agent."""
        if not self.agent_active:
            return
            
        self.agent_active = False
        self.status_var.set("🔴 Agent is inactive")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        schedule.clear()
        self.speak("Agent deactivating. Goodbye!")
        self.log("🔴 Agent deactivated")
        
    def on_closing(self):
        """Handle application closing."""
        if self.agent_active:
            self.stop_agent()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = StyledRoutineMateGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
