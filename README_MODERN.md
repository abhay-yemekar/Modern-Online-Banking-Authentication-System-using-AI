# 🚀 Modern Online Banking Authentication System using AI

A **completely modernized** version of the Online Banking Authentication System built with **CustomTkinter** for a polished, professional interface. This system provides **3-factor authentication** using Face Recognition → OTP Verification → Voice Authentication, with optional liveness detection.

## ✨ What's New in the Modern Version

### 🎨 **Modern UI with CustomTkinter**
- **Dark/Light Theme Support** - Switch between themes seamlessly
- **Professional Design** - Clean, modern interface with proper spacing and typography
- **Responsive Layout** - Adapts to different screen sizes
- **Color-Coded Elements** - Intuitive visual feedback for different operations

### 🔄 **Non-Blocking Operations**
- **Threaded Operations** - All long-running tasks run in background threads
- **Real-time UI Updates** - Progress bars, status indicators, and live feedback
- **Smooth User Experience** - No more frozen interfaces during face capture or training

### 🔔 **Toast Notifications**
- **Success/Error Feedback** - Immediate visual confirmation for every operation
- **Queue System** - Multiple notifications handled gracefully
- **Auto-dismiss** - Notifications disappear automatically after appropriate time
- **Type-based Styling** - Different colors for success, error, warning, and info

### 🛡️ **Enhanced Security Features**
- **Input Validation** - Comprehensive form validation with helpful error messages
- **Database Integrity** - Proper SQLite database structure with foreign keys
- **Secure OTP System** - Time-based OTP with expiry and usage tracking
- **Voice Phrase Validation** - Minimum length requirements and similarity scoring

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Modern Main GUI                          │
│              (GUI_master_modern.py)                        │
├─────────────────────────────────────────────────────────────┤
│  📝 Registration  │  📸 Face Data  │  🧠 Training        │
│  🔍 Liveness     │  🔐 Auth Flow  │  📊 Status Panel    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Individual Modernized Modules                  │
├─────────────────┬─────────────────┬───────────────────────┤
│ Registration    │ Voice Verify    │ OTP System           │
│ (registration_  │ (voice_verifi   │ (otp_modern.py)      │
│  modern.py)     │  cation_modern. │                      │
│                 │  py)            │                      │
└─────────────────┴─────────────────┴───────────────────────┘
```

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
# Install the modern requirements
pip install -r requirements_modern.txt

# Or install manually
pip install customtkinter==5.2.0
pip install opencv-contrib-python==4.9.0.80
pip install numpy==1.23.5
pip install pillow==9.5.0
pip install SpeechRecognition==3.10.1
pip install pyttsx3==2.90
pip install pyaudio==0.2.14
```

### 2. **Run the Modern System**
```bash
# Launch the modern main interface
python GUI_master_modern.py

# Or run individual modules
python registration_modern.py      # User registration
python voice_verification_modern.py # Voice verification
python otp_modern.py              # OTP system
```

### 3. **System Requirements**
- **Python**: 3.8+ (3.9+ recommended)
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Hardware**: Webcam, Microphone, 4GB+ RAM
- **Dependencies**: See `requirements_modern.txt`

## 🔐 Authentication Flow

### **Step 1: User Registration**
1. **Launch Registration**: Click "📝 User Registration" from main GUI
2. **Fill Form**: Enter personal details and voice pass phrase
3. **Database Storage**: User data stored securely in SQLite database
4. **Validation**: Real-time form validation with helpful feedback

### **Step 2: Face Data Creation**
1. **Enter User ID**: Provide numeric identifier for the user
2. **Face Capture**: System captures 40 face images from webcam
3. **Real-time Feedback**: Live preview with capture count and face detection
4. **Quality Control**: Automatic face detection and cropping

### **Step 3: Model Training**
1. **Data Processing**: System loads all captured face images
2. **LBPH Training**: Local Binary Pattern Histogram model training
3. **Progress Tracking**: Real-time training progress with status updates
4. **Model Storage**: Trained model saved to `trainingdata.yml`

### **Step 4: Authentication Process**
1. **Face Recognition**: Webcam-based face detection and recognition
2. **OTP Verification**: Generate and verify 6-digit time-based OTP
3. **Voice Authentication**: Speak registered pass phrase for verification
4. **Multi-factor Success**: All three factors must pass for authentication

## 🎯 Key Features

### **🔐 Multi-Factor Authentication**
- **Face Recognition**: LBPH algorithm with confidence scoring
- **OTP System**: 6-digit codes with 5-minute expiry
- **Voice Verification**: Speech recognition with similarity scoring

### **🎨 Modern User Interface**
- **Theme Switching**: Dark, Light, and System themes
- **Toast Notifications**: Non-intrusive feedback system
- **Progress Indicators**: Real-time operation status
- **Responsive Design**: Adapts to different screen sizes

### **⚡ Performance Optimizations**
- **Threaded Operations**: Non-blocking UI during long tasks
- **Efficient Processing**: Optimized face detection and recognition
- **Memory Management**: Proper cleanup and resource management
- **Background Tasks**: Seamless user experience

### **🛡️ Security Enhancements**
- **Input Validation**: Comprehensive form and data validation
- **Database Security**: Proper SQL injection prevention
- **OTP Security**: Time-based expiry and usage tracking
- **Voice Security**: Minimum phrase length and similarity thresholds

## 📁 File Structure

```
Online Banking Authentication System using AI/
├── 🆕 GUI_master_modern.py           # Modern main interface
├── 🆕 registration_modern.py         # Modern user registration
├── 🆕 voice_verification_modern.py   # Modern voice verification
├── 🆕 otp_modern.py                 # Modern OTP system
├── 🆕 requirements_modern.txt        # Modern dependencies
├── 📖 README_MODERN.md              # This file
├── 🔧 GUI_master.py                 # Original interface (backup)
├── 📸 facesData/                    # Face image storage
├── 🧠 trainingdata.yml              # Trained face model
├── 🗄️ face.db                      # User database
├── 🔍 haarcascade_frontalface_default.xml  # Face detection
└── 📚 assets/                       # System assets
```

## 🎮 Usage Examples

### **Starting the System**
```python
# Run the modern main interface
python GUI_master_modern.py
```

### **User Registration Flow**
```python
# Launch registration
python registration_modern.py

# Fill the form with:
# - First Name: John
# - Last Name: Doe
# - Address: 123 Main St
# - Email: john.doe@email.com
# - Mobile: +1234567890
# - Voice Phrase: "My voice is my password"
```

### **Face Data Creation**
```python
# From main GUI, click "📸 Create Face Data"
# Enter User ID: 1
# System will capture 40 face images
# Vary angles and lighting for better training
```

### **Complete Authentication**
```python
# 1. Face Recognition: Look at webcam
# 2. OTP Verification: Enter 6-digit code
# 3. Voice Verification: Speak your phrase
# 4. Success: All factors verified!
```

## 🔧 Configuration

### **Theme Settings**
```python
# Available themes: "System", "Dark", "Light"
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
```

### **Database Configuration**
```python
# Database path and structure
DB_PATH = PROJECT_DIR / "face.db"
# Tables: User, OTP (auto-created)
```

### **Face Recognition Settings**
```python
# Image settings
IMAGE_SIZE = (200, 200)
CAPTURE_COUNT = 40
LBPH_THRESHOLD = 60.0  # Lower is better
```

## 🐛 Troubleshooting

### **Common Issues**

#### **CustomTkinter Not Found**
```bash
pip install customtkinter==5.2.0
```

#### **OpenCV Face Module Missing**
```bash
pip install opencv-contrib-python==4.9.0.80
```

#### **Microphone Access Issues**
- Check microphone permissions
- Ensure PyAudio is installed correctly
- Test with system audio settings

#### **Webcam Not Working**
- Check webcam permissions
- Ensure no other application is using the camera
- Try different camera indices (0, 1, 2)

### **Performance Tips**
- **Face Capture**: Good lighting, varied angles
- **Voice Recording**: Quiet environment, clear speech
- **System Resources**: Close unnecessary applications
- **Database**: Regular cleanup of old OTP records

## 🚀 Future Enhancements

### **Planned Features**
- **Biometric Integration**: Fingerprint and iris recognition
- **Cloud Storage**: Secure cloud-based user data
- **Mobile App**: Companion mobile authentication app
- **API Integration**: RESTful API for external systems
- **Advanced ML**: Deep learning-based face recognition

### **Security Improvements**
- **Encryption**: End-to-end data encryption
- **Audit Logging**: Comprehensive security event logging
- **Rate Limiting**: Brute force attack prevention
- **Multi-device**: Cross-device authentication support

## 🤝 Contributing

### **Development Setup**
```bash
# Clone the repository
git clone <repository-url>
cd "Online Banking Authentication System using AI"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements_modern.txt

# Run tests
python -m pytest tests/
```

### **Code Style**
- **Python**: PEP 8 compliance
- **Documentation**: Comprehensive docstrings
- **Type Hints**: Full type annotation support
- **Error Handling**: Graceful error handling with user feedback

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter Team**: For the amazing modern UI framework
- **OpenCV Contributors**: For robust computer vision capabilities
- **SpeechRecognition**: For accurate voice processing
- **Original Authors**: For the foundational authentication system

## 📞 Support

### **Getting Help**
- **Issues**: Create GitHub issues for bugs and feature requests
- **Documentation**: Check this README and inline code comments
- **Community**: Join our discussion forum for user support

### **System Requirements Check**
```python
# Run system check
python -c "
import customtkinter as ctk
import cv2
import numpy as np
import speech_recognition as sr
print('✅ All dependencies available')
"
```

---

**🎉 Welcome to the Modern Online Banking Authentication System!**

Experience the future of secure authentication with our AI-powered, user-friendly interface. The system combines cutting-edge technology with intuitive design to provide enterprise-grade security for your banking applications.
