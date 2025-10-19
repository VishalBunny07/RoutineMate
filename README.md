# RoutineMate 🤖

Your personal routine assistant that helps you stay on track with daily habits through voice notifications and desktop reminders.

## ✨ Features

- **Voice Notifications**: Text-to-speech announcements for all routine reminders
- **Desktop Notifications**: Visual pop-up reminders on your screen
- **Automated Scheduling**: Set-and-forget daily routine management
- **Personalized Messages**: Customizable greetings and reminders
- **Comprehensive Coverage**: Morning, lunch, work, evening, and bedtime routines
- **Hydration Reminders**: Hourly water intake notifications
- **Easy Control**: Simple start/stop with keyboard interrupt

### Prerequisites
Make sure you have Python 3.6+ installed on your system.

## 📅 Default Schedule

| Time | Activity | Description |
|------|----------|-------------|
| 7:00 AM | Morning Routine | Wake-up call with morning tasks |
| 12:30 PM | Lunch Reminder | Break time for meal |
| 1:30 PM | Work Reminder | Get back to productive work |
| 6:00 PM | Evening Routine | Wind down and reflection time |
| 10:30 PM | Bedtime Reminder | Sleep preparation routine |
| Every Hour | Water Reminder | Stay hydrated throughout the day |

## GUI Based
**New GUI based using tikinter added and can be customized the schedule with logs**
**Here are the image of GUI**


*1. Default entered Routine*
<img width="1366" height="768" alt="Screenshot (238)" src="https://github.com/user-attachments/assets/9d707931-0e52-4775-aef5-5ad8663ab6b3" />

*2. Schedule update routine*
<img width="1366" height="768" alt="Screenshot (239)" src="https://github.com/user-attachments/assets/91830802-5993-4a51-9cfd-650c44a0874a" />


## 🖥️ Usage

1. **Start the agent**: Run the Python script
2. **Listen for reminders**: RoutineMate will speak and show notifications at scheduled times
3. **Stop the agent**: Press `Ctrl+C` to deactivate

The agent runs continuously in the background and will automatically trigger reminders based on your system time.

## 📦 Dependencies

- **schedule**: Task scheduling library
- **pyttsx3**: Text-to-speech conversion
- **plyer**: Cross-platform desktop notifications

### Notifications Not Showing
- Check if notifications are enabled in your system settings
- On Linux, you might need to install `notify-send`

### Permission Issues
- Run with appropriate permissions for audio and notifications
- Some systems may require administrator privileges

1. **Report bugs** by creating an issue
2. **Suggest features** for new routine types
3. **Submit pull requests** with improvements
4. **Share your custom routines** with the community

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's scheduling and text-to-speech capabilities
- Inspired by the need for better daily routine management
- Thanks to the open-source community for the amazing libraries

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review existing issues for solutions

---

**Made with ❤️ for better daily habits**

*Stay consistent, stay healthy with RoutineMate!*
