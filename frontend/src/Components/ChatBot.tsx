import React, { useState, useEffect, useRef } from 'react';
import './styles/Chatinterface.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:5000');

    ws.current.onmessage = (event: MessageEvent) => {
      const message: Message = JSON.parse(event.data);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: message.text }
      ]);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const sendMessage = () => {
    if (input.trim() && ws.current) {
      const message: Message = { sender: 'user', text: input };
      setMessages((prevMessages) => [...prevMessages, message]);
      ws.current.send(JSON.stringify(message));
      setInput('');
    }
  };

  return (
    <div className="chat-container">
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