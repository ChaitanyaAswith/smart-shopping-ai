// src/components/Recommendations.js

import React, { useState, useEffect } from "react";
import axios from "axios";

function Recommendations({ customerId }) {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    if (customerId) {
      axios.get(`http://localhost:8000/recommend/${customerId}`)
        .then(response => {
          setRecommendations(response.data.recommendations); // Assuming response contains recommendations
        })
        .catch(error => {
          console.error("Error fetching recommendations:", error);
        });
    }
  }, [customerId]);

  return (
    <div>
      <h2>Recommendations</h2>
      {recommendations.length > 0 ? (
        <ul>
          {recommendations.map((product) => (
            <li key={product.id}>
              {product.name} - {product.category} - ${product.price}
            </li>
          ))}
        </ul>
      ) : (
        <p>No recommendations available.</p>
      )}
    </div>
  );
}

export default Recommendations;
