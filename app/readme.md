Usage
Upload PDF and Create Chatbot:

http
Copy code
POST /upload
Form Data: 
  - file: (PDF File)
  - chatbot_name: (Chatbot Name)
Query Chatbot:

http
Copy code
POST /query_chatbot/<chatbot_name>
JSON Body: 
  - query: (Your Query)
Get Chatbot Details:

http
Copy code
GET /get_chatbot/<chatbot_name>
