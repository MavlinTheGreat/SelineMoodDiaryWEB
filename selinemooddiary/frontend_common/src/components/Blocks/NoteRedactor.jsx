import React, { useState, useEffect } from 'react';
import NoteForm from './NoteForm';
import EmotionChoice from './EmotionChoice';
import '../../static/css/calendar.css'
import axios from 'axios';

const NoteRedactor = ({ date, setUsedPart }) => {

  const [loading, setLoading] = useState(true);
  const [activeBlock, setActiveBlock] = useState("noteForm");
  const [emotion, setEmotion] = useState(0);
  const [note, setNote] = useState({});

  useEffect(() => {
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchNote = async () => {
        setLoading(true);
        try {
          
          const response = await axios.get('http://127.0.0.1:8000/api/journal/notes', {
            params: {
              date: date.getFullYear().toString() + "-" + String(date.getMonth() + 1).padStart(2, '0') + "-" + String(date.getDate()).padStart(2, '0'),
            },
            headers: { Authorization: "Bearer " + parsedTokens.access },
          });
          
          if (response.data.length > 0) {
            const noteDate = new Date(response.data[0].date)
            setNote({...response.data[0], date: noteDate})
            setEmotion(note.emotion);
          } else {
            setNote({date: date, content: "", emotion: 0});
          }

          
        } catch (err) {
          alert(err.message);
        } finally {
          setLoading(false);
        }
      };
      
      fetchNote();
    }
  }, [date]);

  const exitRedactor = () => {
    setNote({});
    setEmotion(0);
    setUsedPart("dateList");
  }

  const removeNote = async () => {
    
    const token = localStorage.getItem("authTokens");

    if (token && 'id' in note) {
      const parsedTokens = JSON.parse(token);
      
      try {

        const response = await axios.delete(`http://127.0.0.1:8000/api/journal/notes/${note.id}`, {
            headers: { Authorization: "Bearer " + parsedTokens.access },
        });
      } catch (err) {
        alert(err.message);
      }
    }

    exitRedactor();
  }
  
  const postNote = async (note) => {
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      const headers = {
        'Authorization': "Bearer " + parsedTokens.access,
      };
      
      try {

        const response = 'id' in note ?
          await axios.patch(`http://127.0.0.1:8000/api/journal/notes/${note.id}`, {
            emotion: note.emotion,
            content: note.content,
          } , { headers }) : 
        await axios.post(`http://127.0.0.1:8000/api/journal/notes`,
          {
            date: note.date.getFullYear().toString() + "-" + String(note.date.getMonth() + 1).padStart(2, '0') + "-" + String(note.date.getDate()).padStart(2, '0'),
            emotion: note.emotion,
            content: note.content,
            tags: [],
          },
          { headers });
      } catch (err) {
        alert(err.message);
        alert(note.date.getFullYear().toString() + "-" + String(note.date.getMonth() + 1).padStart(2, '0') + "-" + String(note.date.getDate()).padStart(2, '0'));
      }
    }
    exitRedactor();
  }
  
  const chooseEmotion = (key) => {
    setEmotion(key);
    setNote({...note, emotion: key});
    setActiveBlock("noteForm");
  }

  const componentsMap = {
    'noteForm': <NoteForm note={note} setNote={setNote} setActiveBlock={setActiveBlock} exitRedactor={exitRedactor} removeNote={removeNote} postNote={postNote}/>,
    'emotionChoice': <EmotionChoice chooseEmotion={chooseEmotion}/>,
  }

  return (loading ? <p>Загрузка</p> :
    <div className='note-redactor'>
      {componentsMap[activeBlock] || <div>Страница не найдена</div>}
    </div>
  );
};

export default NoteRedactor;