import React, { useEffect, useState } from 'react';
import './Chat.css';

function Chat() {
  const [novelText, setNovelText] = useState(''); // 소설 텍스트 상태
  const [userInput, setUserInput] = useState(''); // 사용자 입력 상태
  
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

  // 사용자가 질문을 보내는 함수
  const handleSendQuestion = () => {
    setNovelText('');
    // 여기에서 사용자 입력에 대한 로직을 추가할 수 있습니다.
    console.log('User Question:', userInput);

    // 여기에서 소설 등장인물의 대답을 생성하는 로직을 추가할 수 있습니다.
    const characterResponse = '소설 등장인물의 대답...';

    // 소설 텍스트에 사용자 입력과 등장인물의 대답을 추가
    setNovelText(prevText => prevText + `\n\n${userInput}\n${characterResponse}`);

    // 사용자 입력 초기화
    setUserInput('');
  };

  return (
    <div className="chat_container">
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
          <button className='btn_submit' onClick={handleSendQuestion}><img className='icon_send' src='send.png' alt="send" /></button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
