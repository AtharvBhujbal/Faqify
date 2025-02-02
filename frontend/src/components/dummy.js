import React from 'react'

function DummyData() {
    return (
        <div>
            <button onClick={() => fetch('http://localhost:5000/api/dummy-data', { method: 'POST' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .catch(error => console.error('There was a problem with the fetch operation:', error))}>
                Create Dummy Data
            </button>
        </div>
    );
}

export default DummyData;