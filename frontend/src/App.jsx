import { useEffect, useRef, useState } from 'react'
import { extractCode } from './api'
import './App.css'
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter'
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs'

function App() {
  const [imageUploaded, setimageUploaded ]= useState(null)
  const [result, setResult ]= useState(null)
  const [language, setlanguage ]= useState('')
  const[loading,setLoading]=useState(false)
  const[copied,setCopied]=useState(false)
  const resultRef=useRef(null)
  
  useEffect(()=>{
    if(resultRef.current){
      resultRef.current.scrollIntoView({behavior:'smooth'})
    }
  },[result])

async function handleExtract(){
  setLoading(true)
  const data = await extractCode(imageUploaded)
  console.log(data)
  setlanguage(data.language)
  setResult(data.code)
  setLoading(false)
}

async function handleCopy() {
  try{
    navigator.clipboard.writeText(result)
    setCopied(true)
    
  } 
  catch(e){console.log(e)}
}

async function handleReset() {
    setimageUploaded(null)
    setResult(null)
    setlanguage('')
    setLoading(false)
    setCopied(false)
    
  
}

  return (
    <div className="container mt-5">
      {/*heading*/}
      <div className="text-center mb-4">
        <h1 className="app-title">Snap2Code</h1>
        <h3 className="app-subtitle"> Converts code to copiable text</h3>
      </div>

      <div className='text-center mb-3'>
        <input type='file' accept='image/*' style={{display:'none'}} id='fileinput' 
              onChange={(e)=> 
              {const file=e.target.files[0] 
              setimageUploaded(file)}}></input>
        <button className="upload-btn" onClick={()=>document.getElementById('fileinput').click()}>Upload image</button>
        {/*image preview*/} <br></br>
        {imageUploaded && 
        <div className="preview-box">
          <h5 className="preview-label">Image Preview</h5> <br></br>
          <img src={URL.createObjectURL(imageUploaded)} alt="preview" className='img-fluid mt-3' style={{maxHeight:"300px"}}></img>
        </div>  }
      </div>

      <div className="extract-btn">
        <button onClick={handleExtract} disabled={loading}/* loading is true which means it is already extract and that this button should not work after clicked */ >
        {loading? "Extracting...":"Extract Code"}</button>
      </div>
      
    {result &&(
        <div className="result-box" ref={resultRef}>
          <span className="language-tag">Language:{language}</span>
          <p className="result-label">Extracted Code</p>
          {/*extracted code box*/ }
         <SyntaxHighlighter language={language.toLowerCase()} style={atomOneDark}>{result}</SyntaxHighlighter>

     <button className="copy-btn" onClick={handleCopy}>
      {copied? "Copied":"Copy to Clipboard"}</button>
         
      <button className="copy-btn mx-3" onClick={handleReset}>Reset</button>   
        </div>
    )}
        
     
      
    </div>
  )
}

export default App
