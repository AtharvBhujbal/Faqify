import React, { useEffect, useState } from 'react';
import LanguageSelector from './language';

function FAQ() {
    const [faqs, setFaqs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [language, setLanguage] = useState('en');

    const fetchFaqs = () => {
        setLoading(true);
        setError(null);
        fetch(`http://localhost:5000/api/faqs/?lang=${language}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setFaqs(data.faqs);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    };

    useEffect(() => {
        fetchFaqs();
    }, [language]); // Automatically refresh FAQs when language changes

    if (loading) return <p>Loading FAQs...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">FAQs</h1>
            <div className="mb-4">
                <LanguageSelector setLang={setLanguage} />
            </div>
            <button onClick={fetchFaqs} className="mb-4 px-4 py-2 bg-blue-500 text-white rounded">
                Refresh
            </button>
            <ul className="space-y-2">
                {faqs.map((faq) => (
                    <ol key={faq.id} className="border p-3 rounded-lg shadow-sm">
                        <h4 className="font-semibold text-lg">{faq[1]}</h4>
                        <p className="text-gray-700 mt-1">{faq[2]}</p>
                    </ol>
                ))}
            </ul>
        </div>
    );
}

export default FAQ;
