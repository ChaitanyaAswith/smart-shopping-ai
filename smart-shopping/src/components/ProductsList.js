import '../App.css';
import React, { useEffect, useState } from "react";
import axios from "axios";

const ProductsList = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    axios
      .get("http://localhost:8000/recommend/1")
      .then((response) => {
        const fetchedProducts = response.data.recommendations;

        const seen = new Set();
        const uniqueProducts = fetchedProducts.filter((product) => {
          if (seen.has(product.id)) return false;
          seen.add(product.id);
          return true;
        });

        setProducts(uniqueProducts);
        setFilteredProducts(uniqueProducts);
      })
      .catch(() => {
        setError("Error fetching products");
      });
  }, []);

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
  
    const filtered = products.filter((product) =>
      product.name.toLowerCase().includes(query.toLowerCase()) ||
      product.description.toLowerCase().includes(query.toLowerCase()) ||
      product.category.toLowerCase().includes(query.toLowerCase())
    );
  
    setFilteredProducts(filtered);
  };
  

  return (
    <div className="container">
      <h2>Recommended Products</h2>

      <input
        type="text"
        placeholder="Search Products"
        value={searchQuery}
        onChange={handleSearch}
        className="search-input"
      />

      {error && <p className="error-message">{error}</p>}

      {/* Only show this section when user types something */}
      {searchQuery.trim() === "" ? (
        <p className="search-placeholder">Start typing to search for products...</p>
      ) : (
        <div className="product-list">
          {filteredProducts.length > 0 ? (
            filteredProducts.map((product) => (
              <div key={product.id} className="product-card">
                <img
                  src={`http://localhost:8000${product.image_url}`}
                  alt={product.name}
                  className="product-image"
                />
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <p>Category: {product.category}</p>
                <p>Price: ${product.price}</p>
                <p>Stock: {product.stock}</p>
              </div>
            ))
          ) : (
            <p>No products found</p>
          )}
        </div>
      )}
    </div>
  );
};

export default ProductsList;


