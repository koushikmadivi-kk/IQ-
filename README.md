 IQ - AI Voice Assistant
IQ is a desktop AI voice assistant built using Python, OpenAI GPT, Speech Recognition, Text-to-Speech, and PyQt6. It provides an interactive graphical interface inspired by futuristic HUD (Heads-Up Display) systems while allowing users to communicate naturally through voice commands.
The assistant can perform local system operations, answer general questions using OpenAI, remember user information, and provide weather updates through an online weather API.
________________________________________
 Features
 Voice Recognition
•	Listens to the user’s voice using the microphone.
•	Converts speech into text using Google’s Speech Recognition service.
•	Supports natural English voice commands.
________________________________________
 Text-to-Speech
IQ speaks every response using the pyttsx3 speech engine.
Features:
•	Adjustable speaking speed
•	Offline speech synthesis
•	Natural voice output
________________________________________
 AI Conversation
User questions are sent to OpenAI GPT-4o-mini, allowing Jarvis to:
•	Answer general knowledge questions
•	Hold conversations
•	Explain concepts
•	Generate intelligent responses
•	Act like a formal British AI assistant
________________________________________
 Memory System
IQ can remember user information.
Example:
User: Remember my name is John
IQ stores:
{
    "name": "koushik"
}
Later:
User: What is my name?
Jarvis:
Your name is koushik.
The memory is stored locally inside:
memory.json
________________________________________
 Weather Information
Jarvis can retrieve live weather information using the OpenWeather API.
Example:
Weather in London
Jarvis responds with:
The temperature in London is 22°C with scattered clouds.
________________________________________
 Website Launcher
Jarvis can instantly open popular websites.
Supported commands include:
•	Open Google
•	Open YouTube
•	Open Amazon
•	Open WhatsApp
The websites launch automatically in the default browser.
________________________________________
 Local Desktop Commands
Jarvis can control a few desktop applications.
Examples:
•	Open Calculator
•	Open Notepad
These are executed directly using Python system commands.
________________________________________
 Graphical User Interface
The application includes a futuristic interface built with PyQt6.
Features include:
•	Animated circular HUD
•	Neon cyber-themed design
•	Voice interaction button
•	Live conversation console
•	Typing animation for AI responses
•	Responsive interface
________________________________________
 Technologies Used
•	Python
•	PyQt6
•	OpenAI API
•	SpeechRecognition
•	pyttsx3
•	Requests
•	Threading
•	JSON
•	Webbrowser
________________________________________
 Project Structure
jarvis/
│
├── main.py              # Core AI assistant logic
├── jarvis_gui.py        # GUI implementation
├── memory.json          # Stores remembered information
├── key.txt              # OpenAI API key
└── README.md
________________________________________
 Installation
1. Clone the repository
git clone https://github.com/koushikmadivi-kk/jarvis.git
________________________________________
2. Install dependencies
pip install openai
pip install PyQt6
pip install SpeechRecognition
pip install pyttsx3
pip install requests
pip install pyaudio
________________________________________
3. Add your OpenAI API Key
Create or edit:
key.txt
Paste your API key inside the file.
Example:
sk-xxxxxxxxxxxxxxxxxxxxxxxx
________________________________________
4. Run the application
python jarvis_gui.py
________________________________________
 How It Works
1.	User clicks the Speak button.
2.	Jarvis listens through the microphone.
3.	Speech is converted to text.
4.	Jarvis checks whether the command is:
o	a local system command,
o	a memory command,
o	or an AI question.
5.	If it is an AI question, the request is sent to OpenAI.
6.	Jarvis displays the answer with a typing animation.
7.	Jarvis reads the response aloud.
________________________________________
 Example Commands
Open YouTube

Open Amazon

Remember my name is koushik

What is my name?

Weather in Hyderabad

Who invented Python?

Explain Artificial Intelligence.
________________________________________
 Future Improvements
Possible future enhancements include:
•	Email support
•	Music playback
•	Face recognition login
•	Wake word detection (“Hey Jarvis”)
•	Home automation integration
•	File management
•	Calendar and reminders
•	System monitoring
•	Chat history
•	Multi-language support
•	Custom themes
•	Offline AI models
________________________________________
 Learning Objectives
This project demonstrates practical implementation of:
•	Voice Recognition
•	Text-to-Speech
•	API Integration
•	OpenAI GPT Integration
•	GUI Development with PyQt6
•	JSON-based local storage
•	Multithreading
•	Event-driven programming
________________________________________
 Author
Developed as a Python AI Assistant project to explore:
•	Artificial Intelligence
•	Voice Interfaces
•	Desktop Application Development
•	API Integration
•	Human-Computer Interaction
________________________________________
 License
This project is intended for educational and personal learning purposes. You are free to modify and improve it for your own use.
________________________________________
 Project Summary
J.A.R.V.I.S combines voice recognition, artificial intelligence, desktop automation, and a futuristic graphical interface into a single Python application. It demonstrates how modern AI services can be integrated into a desktop assistant capable of understanding speech, responding intelligently, remembering user information, and interacting with the operating system through simple voice commands.
