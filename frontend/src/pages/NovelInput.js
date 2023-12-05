import React, { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import './NovelInput.css'

function NovelInput() {
  const [myFiles, setMyFiles] = useState([])

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
    console.log(myFiles);
  }

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
      </div>

    </div>
  );
}

export default NovelInput;