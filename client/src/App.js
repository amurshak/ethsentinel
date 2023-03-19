import React, { useState, useEffect } from 'react';
import './App.css';


function App() {

  const [data, setData] = useState([]);

  useEffect(() => {
    //Server-Send Event Source
    const sse = new EventSource('/stream');

    //Parse stream data and update
    function handleStream(e) {
      const newData = JSON.parse(e.data)

      setData(newData)
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
          <table>
            <thead>
              <tr>
                <th>Block</th>
                <th>To</th>
                <th>From</th>
                <th>Value (ETH)</th>
                <th>Value (USD)</th>

              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={index}>
                  <td>{item.Block}</td>
                  <td>{item.To}</td>
                  <td>{item.From}</td>
                  <td>{item.Eth}</td>
                  <td>{item.Usd}</td>
                </tr>
              ))}
            </tbody>
    </table>
    </div>
  );
}

export default App;
