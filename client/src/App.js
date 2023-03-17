import React, { useState, useEffect } from 'react';
import './App.css';

function App() {

  const [data, setData] = useState('Initializing...');

  useEffect(() => {
    const sse = new EventSource('/stream');
    
    function handleStream(e) {
      console.log(e)
      setData(e.data)
    }
    sse.onmessage = (e) => {handleStream(e)};

    sse.onerror = e => {
      sse.close()
    }

    return () => {
      sse.close();
    };
  }, );

  return (
    <div className="App">
      {data}
    </div>
  );
}

export default App;
