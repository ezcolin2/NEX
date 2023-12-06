import React, { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import './NovelInput.css'
import axios from "axios"
import { useNavigate } from "react-router-dom"

function NovelInput() {
  const navigate = useNavigate();
  const [myFiles, setMyFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const onDrop = useCallback(acceptedFiles => {
    setMyFiles([...myFiles, ...acceptedFiles])
  }, [myFiles])

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
  })

  const removeFile = file => () => {
    const newFiles = [...myFiles]
    newFiles.splice(newFiles.indexOf(file), 1)
    setMyFiles(newFiles)
  }

  const uploadFile = () => {
    setIsLoading(true);
    const formData = new FormData();
  
    myFiles.forEach((file) => {
      formData.append(`file`, file);
    });
    console.log(formData);
  
    axios.post('http://localhost:5000/files', formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then(response => {
        console.log('Upload successful:', response.data);
        const documentUuid = response.data.documentUuid;
        axios.get(`http://localhost:5000/files/${documentUuid}/process`)
        .then(getResponse => {
          console.log('GET request successful:', getResponse.data);
          setIsLoading(false);
          alert("업로드 성공!");
          navigate('/selectnovel');
        })
        .catch(getError => {
          console.error('Error in GET request:', getError);
        });
      })
      .catch(error => {
        alert("업로드 실패!");
        setIsLoading(false);
        console.error('Error uploading file:', error);
      });
  };
  

  const files = myFiles.map(file => (
    <li key={file.path}>
      {file.path}
      <img className="btn_remove" onClick={removeFile(file)} src="remove.png" alt="remove file" width={20} />
    </li>
  ))

  return (
    <div className="container">
      <div className="header">
        <h1><a href="/">NEX</a></h1>
      </div>
      <div className="nex_container">
        <section className="upload_container">
          <div {...getRootProps({ className: "dropzone" })}>
            <input className="input" {...getInputProps()} />
            <p>Drag & drop any file here or browse file from device</p>
          </div>
          <aside>
            <ul>{files}</ul>
          </aside>
        </section>
        <button onClick={uploadFile} type="button" className="upload_button"> Upload </button>
        {isLoading && <div className="loader"></div>}
      </div>

    </div>
  );
}

export default NovelInput;