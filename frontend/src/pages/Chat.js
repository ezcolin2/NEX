import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Chat.css';
import { useLocation } from 'react-router-dom';

function Chat() {
  const [novelText, setNovelText] = useState(''); 
  const [userInput, setUserInput] = useState(''); 
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const novelid = searchParams.get('novelid');
  const characterId = searchParams.get('character_id');
  const [backgroundImageUrl, setBackgroundImageUrl] = useState('nex_background.jpg');
  
  useEffect(() => {
    const text = document.querySelector(".novel_text");

    if (text) {
      text.textContent = "";
      let txtIdx = 0;

      function typing() {
        let txt = novelText[txtIdx++];
        if (txt === undefined) return;
        text.innerHTML += txt === "\n" ? "<br/>" : txt;
        if (txtIdx > novelText.length) {
          txtIdx = 0;
        } else {
          setTimeout(typing, 100);
        }
      }

      typing();
    }
  }, [novelText]);

  const handleSendQuestion = () => {  
    axios.post('http://localhost:5000/chat', {
      novelId: novelid,
      characterId: characterId,
      query: userInput
    })
      .then(response => {
        console.log('Response from server:', response.data);
        const characterResponse = response.data.res;
        const imageUrl = response.data.imageUrl;
        setBackgroundImageUrl(imageUrl);
        setNovelText(prevText => prevText + `\n\n${characterResponse}`);
        setUserInput('');
      })
      .catch(error => {
        console.error('Error sending POST request:', error);
      });
  };

  return (
    <div className="chat_container" style={{ backgroundImage: `url(${backgroundImageUrl})`, backgroundSize: 'cover' }}>
      <div className='chat_box'>
        <div className='chat_text_box'>
          {novelText && <div className="novel_text">{novelText}</div>}
        </div>
        <div className='chat_input'>
          <textarea
            className='chat_input_box'
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Enter your question.."
          />
          <button className='btn_submit' onClick={handleSendQuestion}>
            <img className='icon_send' src='send.png' alt="send" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
