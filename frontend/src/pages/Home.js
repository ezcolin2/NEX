import React from 'react';
import './Home.css'

function Home() {
  return (
    <div className="container">
      <div className="header">
        <h1><a href="/">NEX</a></h1>
      </div>
      <div className="adg_info">
        <h2>Novel Expedition</h2>
        <p>Upload a novel and take a trip into it</p>
        <a href="/selectnovel"><button>Get Started</button></a>
      </div>
    </div>
  );
}

export default Home;