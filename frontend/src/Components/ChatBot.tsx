import React, { useState } from 'react';
import './styles/Chatinterface.css';
import { query } from 'firebase/firestore';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [botName, setBotName] = useState('Configuration'); 

  const sendMessage = async () => {
    if (input.trim()) {
      const userMessage: Message = { sender: 'user', text: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      try {
        const response = await fetch(`http://127.0.0.1:5000/query_chatbot/${botName}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: input }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const botMessage: Message = { sender: 'bot', text: data.response };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error('Error fetching response:', error);
        const errorMessage: Message = { sender: 'bot', text: 'Error fetching response from the server.' };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }

      setInput('');
    }
  };

  return (
    <div className="chat-container">
      <div className="bot-name-input">
        <input
          type="text"
          value={botName}
          onChange={(e) => setBotName(e.target.value)}
          placeholder="Enter bot name..."
        />
        <br />
      </div>
      <div className="messages-container">
        {messages.map((msg, index) => (
          // eslint-disable-next-line react/no-array-index-key
          <div key={`${msg.sender}-${index}`} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
        />
        <button type="button" onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatInterface;
