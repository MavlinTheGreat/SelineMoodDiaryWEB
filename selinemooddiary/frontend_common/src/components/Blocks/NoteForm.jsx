import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import closeImg from '../../assets/images/close.png';
import '../../static/css/calendar.css'

const NoteForm = ({ note, setNote, setActiveBlock, exitRedactor, postNote, removeNote }) => {

  const [loading, setLoading] = useState(true);
  const [emotions, setEmotions] = useState([]);
  const textareaRef = useRef(null);
      
  if (note.emotion == 0) {
    setActiveBlock("emotionChoice");
  }
  
  const [componentHeight, setComponentHeight] = useState("");
  const [componentWidth, setComponentWidth] = useState("");

  useEffect(() => {
    const updateBodyHeight = () => {
      const bodyHeight = document.body.style.height;
      setComponentHeight(`calc(${bodyHeight} - 8rem)`);
      setComponentWidth(`calc((${bodyHeight} - 8rem) / 1.3)`);
    };

    // Устанавливаем высоту при загрузке и при изменении размера окна
    updateBodyHeight();
    window.addEventListener('resize', updateBodyHeight);

    return () => window.removeEventListener('resize', updateBodyHeight);
  }, []);

  useEffect(() => {
    if (!loading && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [loading]);

  useEffect(() => {
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchEmotions = async () => {
        setLoading(true);
        try {
          
          const response = await axios.get('http://127.0.0.1:8000/api/journal/emotions', {
            headers: { Authorization: "Bearer " + parsedTokens.access },
          });
          
          setEmotions(response.data);
        } catch (err) {
          alert(err.message);
        } finally {
          setLoading(false);
        }
      };
      
      fetchEmotions();
    }
  }, []);
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    postNote(note);
  }

  return ( loading ? <p>Загрузка</p> :
    <div
      style={{
        height: componentHeight,
        width: componentWidth
      }}
      className='note-form-container'
    >
      <div className='note-form-header'>
        <div>
          {note.date.toLocaleString("default", {
            day: "numeric",
            month: "long",
          })}
        </div>
        {note.emotion != 0 && (<div className='emotion-partition'>
           <img
            src={emotions.find((emotion) => emotion.id === note.emotion).imageIcon}
            onClick={() => setActiveBlock("emotionChoice")}
          />
          {emotions.find((emotion) => emotion.id === note.emotion).name}
        </div>)}
        <button onClick={() => exitRedactor()}><img src={closeImg}/></button>
      </div>
      <form className='note-form' onSubmit={handleSubmit}>
          <div className='note-form-textarea'><label htmlFor='textarea'><textarea
            id="textarea"
            ref={textareaRef}
            value={note.content}
            onChange={(e) => setNote({...note, content: e.target.value})}
          /></label>
          </div>
          <div className='form-buttons'>
            <button type='button' onClick={() => removeNote(note)}>{'Удалить'}</button>
            <button type="submit">{'Сохранить'}</button>
          </div>
      </form>
    </div>
  );
};

export default NoteForm;