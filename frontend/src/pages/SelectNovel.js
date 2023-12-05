import React from "react"
import './SelectNovel.css'
import { useNavigate } from "react-router-dom";

function NovelInput() {
  const navigate = useNavigate();
  const goUpload = () => {
    navigate('/novelinput');
  }
  const navigateToCharacter = (selectedNovel) => {
    navigate(`/selectcharacter?novel=${encodeURIComponent(selectedNovel)}`);
  }
  const novels = [
    "운수 좋은날 1",
    "운수 좋은날 2",
    "운수 좋은날 3",
    "운수 좋은날 4",
    "운수 좋은날 5",
    "운수 좋은날 1",
    "운수 좋은날 2",
    "운수 좋은날 3",
    "운수 좋은날 4",
    "운수 좋은날 5",
    "운수 좋은날 1",
    "운수 좋은날 2",
    "운수 좋은날 3",
    "운수 좋은날 4",
    "운수 좋은날 5",
    "운수 좋은날 1",
    "운수 좋은날 2",
    "운수 좋은날 3",
    "운수 좋은날 4",
    "운수 좋은날 5",
  ];
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
                <li className="novel" onClick={() => navigateToCharacter(novel)} key={index}>{novel}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NovelInput;