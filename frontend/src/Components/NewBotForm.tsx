import React, { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';

const BotForm = () => {
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


  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log({
      chatbotName,
      chatbotDomain,
      chatbotAnswers,
      chatbotRestrictions,
      selectedFiles
    });
    // Reset form fields
    setChatbotName('');
    setChatbotDomain('');
    setChatbotAnswers('');
    setChatbotRestrictions('');
    setSelectedFiles([]);
  };

  return (
    <div>
      <Typography variant="h6">Bot Configuration</Typography>
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
