import React from 'react';
import './YourComponent.css';

const YourComponent = () => {
  return (
    <div className="your-component">
      <h1>Welcome to Our Photography Website</h1>
      <img 
        src="/images/photographer.jpg" 
        alt="A photographer holding a camera." 
        className="responsive-image" 
      />
      <p>We capture moments that last a lifetime.</p>
    </div>
  );
}

export default YourComponent;