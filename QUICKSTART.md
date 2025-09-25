# 🚗 Car Advisor - Quick Start Guide

Welcome to Car Advisor! This guide will help you get started in just a few minutes.

## 📋 What You'll Need

- **Python 3.8+** installed on your computer
- **OpenAI API Key** (get one free at https://platform.openai.com/api-keys)
- **Internet connection** for AI features

## 🚀 Quick Setup (2 minutes)

### Option 1: Automatic Setup (Recommended)

```bash
# 1. Navigate to the project folder
cd caradvisor

# 2. Run the setup script
python setup.py

# 3. Follow the prompts to enter your OpenAI API key

# 4. Start the app
./run_app.sh        # Mac/Linux
# OR
run_app.bat         # Windows
```

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment template
cp .env.template .env

# 3. Edit .env file and add your OpenAI API key
# Replace 'your_openai_api_key_here' with your actual key

# 4. Run the app
streamlit run app.py
```

## 🎯 First Time Usage

1. **Open your browser** - The app will automatically open at `http://localhost:8501`

2. **Login** - Use password: `senior_car_guide_2024`

3. **Take the Quiz** - Click "Car Finder Quiz" to start

4. **Get Recommendations** - Complete the questionnaire to get AI-powered car recommendations

5. **Compare Cars** - Add cars to comparison and analyze them side-by-side

6. **Ask AI Expert** - Use the chat feature for any car-related questions

## 📖 Key Features Overview

| Feature                | Description                         | How to Access                 |
| ---------------------- | ----------------------------------- | ----------------------------- |
| 🏠 **Home**            | Welcome page and overview           | Always available              |
| 📝 **Car Finder Quiz** | Smart questionnaire for preferences | Sidebar → Car Finder Quiz     |
| 🚗 **Recommendations** | AI-powered car suggestions          | Complete quiz first           |
| ⚖️ **Compare Cars**    | Side-by-side car comparison         | Add cars from recommendations |
| 💬 **AI Expert Chat**  | Interactive car consultation        | Sidebar → Ask AI Expert       |
| ⭐ **Reviews**         | Real user reviews and ratings       | Sidebar → Reviews & Ratings   |
| 📄 **Export**          | Download PDF reports                | Sidebar → Export & Share      |

## 🔧 Customization

### Change Login Password

Edit `.env` file:

```
LOGIN_PASSWORD=your_new_password_here
```

### Enable Debug Mode

Edit `.env` file:

```
DEBUG_MODE=True
```

### Update App Settings

Edit `.env` file:

```
APP_TITLE=Your Custom Title
```

## ❓ Troubleshooting

### App Won't Start

```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Check if port is free
netstat -an | grep 8501
```

### API Key Issues

1. Verify your OpenAI API key is correct
2. Check you have credits in your OpenAI account
3. Ensure the key is properly set in the `.env` file

### Import Errors

```bash
# Clear cache and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### Performance Issues

- Close other applications to free memory
- Use a stable internet connection
- Try refreshing the browser page

## 📱 Browser Compatibility

**Recommended browsers:**

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

**Mobile support:**

- ✅ Works on tablets and mobile devices
- ✅ Responsive design for all screen sizes

## 🔒 Security & Privacy

- **Your data stays local** - No data is sent to external servers except OpenAI for AI features
- **Password protection** - Secure login system
- **API key security** - Stored locally in your `.env` file
- **No tracking** - No analytics or user tracking

## 🆘 Getting Help

### In-App Help

- Use the **AI Expert Chat** for car-related questions
- Check tooltips and help text throughout the app

### Technical Support

- Check the main README.md file for detailed documentation
- Review error messages for specific issues
- Ensure all dependencies are properly installed

### Community

- Share feedback and suggestions
- Report bugs or issues
- Request new features

## 🎉 Tips for Best Experience

1. **Complete the full questionnaire** for the most accurate recommendations
2. **Use specific details** when chatting with the AI expert
3. **Compare multiple cars** before making decisions
4. **Export PDF reports** to share with family/dealers
5. **Update your preferences** as your needs change

## 📋 Sample Workflow

Here's a typical user journey:

```
1. Login to the app
   ↓
2. Take the Car Finder Quiz (5-10 minutes)
   ↓
3. Review AI Recommendations (5+ cars suggested)
   ↓
4. Add 2-3 cars to comparison
   ↓
5. Analyze detailed comparison charts
   ↓
6. Ask AI Expert specific questions
   ↓
7. Read user reviews for shortlisted cars
   ↓
8. Export recommendations as PDF
   ↓
9. Visit dealerships with your report
```

---

**🚗 Ready to find your perfect car? Start the app and take the quiz!**

For more detailed information, see the main [README.md](README.md) file.
