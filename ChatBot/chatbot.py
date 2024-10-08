import tkinter as tk
from tkinter import scrolledtext
import spacy

# Load spaCy model for NLP processing
nlp = spacy.load('en_core_web_sm')

# Predefined responses
responses = {
    "hi": "Hello! How can I help you today?",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "bye": "Goodbye! Have a great day ahead.",
    "what is your name": "I am a simple chatbot created by you.",
    "thank you": "You're welcome!",
    "where are you from": "I am from the depths of your imagination!",
    "tell me a joke": "Why don't skeletons fight each other? They don't have the guts!",
    "who created you": "I was created by a brilliant programmer like yourself!",
    "how old are you": "I am as old as the universe itself... just kidding! I am brand new."
}

# Function to get a bot response based on simple logic and spaCy
def get_bot_response(user_input):
    user_input = user_input.lower().strip()  # Convert to lowercase for matching

    # Check if the input matches a predefined response
    if user_input in responses:
        return responses[user_input]

    # Process the input with spaCy for more advanced responses
    doc = nlp(user_input)

    # Respond based on entity detection
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return f"Nice to meet you, {ent.text}! How can I assist you today?"
        if ent.label_ == "GPE":  # GPE = Countries, cities, states
            return f"Oh, {ent.text} sounds like a wonderful place! What would you like to know?"

    # Respond based on part-of-speech tagging
    for token in doc:
        if token.pos_ == "VERB":
            return f"It sounds like you're talking about {token.text}. Can you tell me more?"

    # Fallback response if no match is found
    return "I'm not sure I understand. Can you clarify that?"

# Function to update the chat window with user and bot messages
def send_message():
    user_message = input_box.get()  # Get user's message
    if user_message:
        # Display user's message in a chat bubble (left side)
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_message + "\n", "user_tag")
        
        # Get bot response and display it in a chat bubble (right side)
        bot_response = get_bot_response(user_message)
        chat_window.insert(tk.END, "Bot: " + bot_response + "\n\n", "bot_tag")

        chat_window.config(state=tk.DISABLED)  # Disable editing of chat window
        chat_window.yview(tk.END)  # Auto scroll to the end

        # Clear the input box
        input_box.delete(0, tk.END)

# Function to bind the Enter key to sending a message
def enter_pressed(event):
    send_message()

# Create the main window for the chatbot
root = tk.Tk()
root.title("Chatbot")

# Set the window size and background color for dark theme
root.geometry("600x600")
root.config(bg='#2c2f33')

# Create a scrollable text area for the chat conversation
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=70, font=("Helvetica", 12), bg='#23272a', fg='#ffffff')
chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create chat tags for user and bot messages with dark theme colors
chat_window.tag_configure("user_tag", foreground="#ffffff", background="#7289da", justify="left", font=("Helvetica", 12, "bold"), lmargin1=10, lmargin2=10, rmargin=10)
chat_window.tag_configure("bot_tag", foreground="#ffffff", background="#43b581", justify="right", font=("Helvetica", 12, "italic"), lmargin1=10, lmargin2=10, rmargin=10)

# Create a text entry box for typing user input
input_frame = tk.Frame(root, bg='#2c2f33')
input_box = tk.Entry(input_frame, font=("Helvetica", 14), width=50, bg='#23272a', fg='#ffffff', insertbackground='white')
input_box.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.X, expand=True)

# Create a "Send" button with dark theme colors
send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Helvetica", 12), bg="#7289da", fg="white", width=8)
send_button.pack(side=tk.RIGHT, pady=10, padx=10)

input_frame.pack(fill=tk.X, padx=10, pady=5)

# Bind the Enter key to the send_message function
root.bind('<Return>', enter_pressed)

# Start the GUI event loop
root.mainloop()
