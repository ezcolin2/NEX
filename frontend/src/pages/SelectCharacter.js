import React, { useEffect, useState } from 'react';
import './SelectCharacter.css';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

function SelectCharacter() {
  const navigate = useNavigate();
  const location = useLocation();
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const novelId = searchParams.get("novel");
    console.log("Novel ID from URL:", novelId);

    const getCharacter = () => {
      axios.get(`http://localhost:5000/novels/${novelId}`) // Update endpoint based on your API structure
        .then(response => {
          console.log(response);
          setCharacters(response.data.characters); // Assuming your API response has a 'characters' property
        })
        .catch(error => {
          console.error('Error fetching characters:', error);
        });
    };

    getCharacter(); // Call the function to fetch characters
  }, [location.search]);

  const goChat = (novelid, character_id) => {
    navigate(`/chat?novelid=${novelid}&character_id=${character_id}`);
  };

  return (
    <div className="container">
      <div className="header">
        <h1><a href="/">NEX</a></h1>
      </div>
      <div className="select_container">
        <h1 className="select_header">SELECT CHARACTER</h1>
        <div className="character_container">
          {characters.map((character, index) => (
            <div key={index} className="character_card" onClick={() => goChat(character.novel.$oid, character._id.$oid)}>
              <img src='person.png' alt={character.name} />
              <p className='charac_name'>{character.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SelectCharacter;
