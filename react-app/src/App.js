// import React from 'react';

// const App = () => {
//     return (
//         <h1>App</h1>
//     )
// }
// export default App;

// import React, { useState } from 'react';


// const ChatBot = () => {
//     const [chatMessages, setChatMessages] = useState([
//         { text: "Hi! I'm your AI-Generative Chatbot", sender: 'bot' }
//     ]);
//     const [userInput, setUserInput] = useState('');

//     const handleUserInput = (e) => {
//         setUserInput(e.target.value);
//     }

//     const handleSubmit = (e) => {
//         e.preventDefault();

//         setChatMessages([...chatMessages, { text: userInput, sender: 'user' }]);
//         setUserInput('');

//         const fetchBotResponse = async () => {
//             try {
//                 const response = await fetch(`/get?msg=${userInput}`);
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 const data = await response.json();
//                 setChatMessages([...chatMessages, { text: data, sender: 'bot' }]);
//             } catch (error) {
//                 console.error('Error fetching bot response:', error);
//             }
//         }

//         fetchBotResponse();
//     }

//     return (
//         <div>
//             <h1 align="center"><b>AI-Gen ChatBot</b></h1>
//             <h4 align="center"><b>Please start your personalized interaction with the chatbot</b></h4>
//             <div className="boxed">
//                 <div id="chatbox">
//                     {chatMessages.map((message, index) => (
//                         <p key={index} className={message.sender === 'bot' ? 'botText' : 'userText'}>
//                             <span>{message.text}</span>
//                         </p>
//                     ))}
//                 </div>
//                 <div id="userInput">
//                     <form onSubmit={handleSubmit}>
//                         <input 
//                             id="textInput" 
//                             type="text" 
//                             name="msg" 
//                             placeholder="Message" 
//                             value={userInput}
//                             onChange={handleUserInput}
//                         />
//                     </form>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default ChatBot;

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      sender: 'user',
      text: input,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');

    try {
      const response = await axios.get(`http://127.0.0.1:5000/get?msg=${input}`);
      const botMessage = {
        sender: 'bot',
        text: response.data,
      };

      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message to backend:', error);
      const errorMessage = {
        sender: 'bot',
        text: 'An error occurred. Please try again later.',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
   
      <h1>Your Agent Chat Bot</h1>
        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
