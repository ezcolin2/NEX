import React from 'react';
import './SelectCharacter.css';
import { useNavigate } from 'react-router-dom';

function SelectCharacter() {
  const navigate = useNavigate();
  const goChat = (name) => {
    navigate(`/chat?name=${name}`);
  }
  const characters = [
    { id: 1, name: "Rick", image: "Rick.jpg" },
    { id: 2, name: "Morty", image: "Rick.jpg" },
    { id: 3, name: "Summer", image: "Rick.jpg" },
    { id: 4, name: "Beth", image: "Rick.jpg" },
    { id: 5, name: "Jerry", image: "Rick.jpg" },
    { id: 6, name: "Abadango", image: "Rick.jpg" },
    { id: 7, name: "Abradolf", image: "Rick.jpg" },
    { id: 8, name: "Adjudicator", image: "Rick.jpg" },
  ];

  const imageGenerator = async () => {
    const response = await fetch(
      "https://api.openai.com/v1/images/generations",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization:
            "Bearer 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",
          "User-Agent": "Chrome",
        },
        body: JSON.stringify({
          prompt: `A photograph of a white Siamese cat.`,
          n: 1,
          size: "512x512",
        }),
      }
    );
    let data = await response.json();
    console.log(data);
  }

  return (
    <div className="container">
      <div className="header">
        <h1><a href="/">NEX</a></h1>
      </div>
      <div className="select_container">
        <h1 className="select_header">SELECT CHARACTER</h1>
        <div className="character_container">
          {characters.map(character => (
            <div key={character.id} className="character_card" onClick={() => goChat(character.name)}>
              <img src={character.image} alt={character.name} />
              <p>{character.name}</p>
            </div>
          ))}
        </div>
        <button onClick={() => {imageGenerator()}}>생성</button>
      </div>
    </div>
  );
}

export default SelectCharacter;
