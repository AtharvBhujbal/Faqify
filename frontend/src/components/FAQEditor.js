import React, { useState } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import LanguageSelector from './language';

export default function FAQEditor() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [lang, setLang] = useState('en');
  const handleSave = () => {
    const faqData = {
      question,
      answer,
      lang
    };
    fetch('http://localhost:5000/api/create-faq', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(faqData),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div className="p-4 max-w-2xl mx-auto bg-white shadow-md rounded-xl">
      <h2 className="text-2xl font-bold mb-4">Create FAQ</h2>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your question"
        className="w-full p-2 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <ReactQuill
        value={answer}
        onChange={setAnswer}
        className="mb-4"
        theme="snow"
      />
      <LanguageSelector setLang={setLang} />  
      <button
        onClick={handleSave}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-300"
      >
        Save FAQ
      </button>
    </div>
  );
}
