import React, { useEffect, useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';

const BotForm = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [chatbotName, setChatbotName] = useState('');
  const [chatbotDomain, setChatbotDomain] = useState('');
  const [chatbotAnswers, setChatbotAnswers] = useState('');
  const [chatbotRestrictions, setChatbotRestrictions] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = target;
    if (files) {
      const fileList = Array.from(files);
      setSelectedFiles(fileList);
    }
  };

  useEffect(() => {
    const storedEmail = localStorage.getItem('email');
    if (storedEmail) {
      setEmail(storedEmail);
    }
    const storedName = localStorage.getItem('name');
    if (storedName) {
      setName(storedName);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('chatbot_name', chatbotName);
    formData.append('domain', chatbotDomain);
    formData.append('allowedAnswers', chatbotAnswers);
    formData.append('restrictedAnswers', chatbotRestrictions);

    selectedFiles.forEach((file) => {
      formData.append('file', file);
    });

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('Form submitted successfully');
        // Reset form fields
        setChatbotName('');
        setChatbotDomain('');
        setChatbotAnswers('');
        setChatbotRestrictions('');
        setSelectedFiles([]);
      } else {
        console.error('Form submission failed');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <div>
      <Typography variant="h6">Bot Configuration </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Chatbot Name"
          value={chatbotName}
          onChange={(e) => setChatbotName(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Domain"
          value={chatbotDomain}
          onChange={(e) => setChatbotDomain(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Allowed Answers"
          value={chatbotAnswers}
          onChange={(e) => setChatbotAnswers(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Restricted Answers"
          value={chatbotRestrictions}
          onChange={(e) => setChatbotRestrictions(e.target.value)}
          fullWidth
          margin="normal"
        />
        <input
          type="file"
          accept="application/pdf"
          multiple
          onChange={handleFileChange}
          style={{ margin: '20px 0' }}
        />
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
      </form>
    </div>
  );
};

export default BotForm;
