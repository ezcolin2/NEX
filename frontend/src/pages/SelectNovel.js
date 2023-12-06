import React, { useEffect, useState } from "react"
import './SelectNovel.css'
import { useNavigate } from "react-router-dom";
import axios from "axios";

function NovelInput() {
  const navigate = useNavigate();
  const goUpload = () => {
    navigate('/novelinput');
  }
  const navigateToCharacter = (selectedNovel) => {
    navigate(`/selectcharacter?novel=${encodeURIComponent(selectedNovel)}`);
  }
  const [novels, setNovels] = useState([]);
  useEffect(() => {
    axios.get('http://localhost:5000/novels') // Replace with your actual API endpoint
      .then(response => {
        setNovels(response.data.novels);
      })
      .catch(error => {
        console.error('Error fetching novel list:', error);
      });
  }, []); // Empty dependency array to run the effect only once when the component mounts
   

  return (
    <div className="container">
      <div className="header">
        <h1><a href="/">NEX</a></h1>
      </div>
      <div className="select_novel_container">
        <div className="generate_container">
          <button className="btn_upload" onClick={goUpload}>Upload Novel</button>
        </div>
        <div className="novel_list_container">
          <h1 className="list_header">Novel List</h1>
          <div className="novellist">
            <ul className="novel_list">
              {novels.map((novel, index) => (
                <li className="novel" onClick={() => navigateToCharacter(novel._id.$oid)} key={index}>{novel.name}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NovelInput;