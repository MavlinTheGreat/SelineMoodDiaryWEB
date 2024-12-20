import React, { useState, useEffect, useRef } from 'react';
import '../../static/css/statistics.css'
import axios from 'axios';

import checkedWeekDay from '../../assets/images/statImages/Check circle.png';
import uncheckedWeekDay from '../../assets/images/statImages/Uncheck circle.png';
import circleDiagram from '../../assets/images/statImages/Circle.png';
import graphDiagram from '../../assets/images/statImages/Graph.png';

import localBackgroundImage from '../../assets/images/4.jpg';

let currentMonday = new Date();

const Statistics = ({}) => {
  
  const [viewedStats, setViewedStats] = useState('circle');
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statImage, setStatImage] = useState({});
  const [stats, setStats] = useState({});
  const [weekDays, setWeekDays] = useState([
    [false, false],
    [false, false],
    [false, false],
    [false, false],
    [false, false],
    [false, false],
    [false, false]
  ]);
    
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
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchNotes = async () => {
        setLoading(true);
        try {
          
          const currentDate = new Date();
    
          const dayOfWeek = currentDate.getDay();
    
          const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
          currentMonday = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            currentDate.getDate() + diffToMonday
          );
    
          const nextMonday = new Date(
            currentMonday.getFullYear(),
            currentMonday.getMonth(),
            currentMonday.getDate() + 7
          );
          
          const response = await axios.get('http://127.0.0.1:8000/api/journal/notes', {
            params: {
              start_date: currentMonday.getFullYear().toString() + "-" + String(currentMonday.getMonth() + 1).padStart(2, '0') + "-" + String(currentMonday.getDate()).padStart(2, '0'),
              end_date: nextMonday.getFullYear().toString() + "-" + String(nextMonday.getMonth() + 1).padStart(2, '0') + "-" + String(nextMonday.getDate() + 1).padStart(2, '0'), 
            },
            headers: { Authorization: "Bearer " + parsedTokens.access },
          });
          
          
          setNotes(response.data);
        } catch (err) {
          alert(err.message);
        }
        setLoading(false);
      };
      
      fetchNotes();

    }
  }, []);

  useEffect(() => {
    setLoading(true);

    notes.map((note) => {
      const noteDate = new Date(note.date);
      const todayDate = new Date();
      setWeekDays(weekDays => weekDays.map((weekday, i) => [i === (Math.floor(Math.abs(noteDate - currentMonday) / (1000 * 60 * 60 * 24))) ? true : weekday[0], i === (Math.floor(Math.abs(todayDate - currentMonday) / (1000 * 60 * 60 * 24))) ? true : weekday[1]]))
    })
    setLoading(false);

  }, [notes]);

  useEffect(() => {
    document.body.style.backgroundImage = `url(${localBackgroundImage})`;
    return () => {
      document.body.style.backgroundImage = '';
    };
  }, []);

  useEffect(() => {
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchStats = async () => {
        setLoading(true);
        try {
          
          const response = await axios.get('http://127.0.0.1:8000/api/stat/strike', {
            headers: { Authorization: "Bearer " + parsedTokens.access },
          });
          
          setStats(response.data);
        } catch (err) {
          alert(err.message);
        }
        setLoading(false);
      };
      
      fetchStats();
    }
  }, [])
  
  useEffect(() => {
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchStatImage = async () => {
        setLoading(true);
        try {
          const response = viewedStats === 'circle' ?
            await axios.get('http://127.0.0.1:8000/api/stat/moodcategory', {
              responseType: 'arraybuffer',
              headers: { Authorization: "Bearer " + parsedTokens.access },
            }) : await axios.get('http://127.0.0.1:8000/api/stat/moodchange', {
              responseType: 'arraybuffer',
              headers: { Authorization: "Bearer " + parsedTokens.access },
            });

          const base64Image = btoa(
            new Uint8Array(response.data)
              .reduce((data, byte) => data + String.fromCharCode(byte), '')
          );

          setStatImage(base64Image);
        } catch (err) {
          alert(err.message);
        }
       setLoading(false);
      };
      
      fetchStatImage();
    }
  }, [viewedStats]);

  return ( loading ? <div className='statistics-section'>{'Загрузка'}</div> :
    <div style={{
      height: componentHeight
    }} className='statistics-section'>
      <div className='stat-buttons'>
        <button onClick={() => setViewedStats('circle')}><img src={circleDiagram}/></button>
        <div className='separator'></div>
        <button onClick={() => setViewedStats('column')}><img src={graphDiagram}/></button>
      </div>
      <div className='numeric-stats'>
        <div className='total-stats'>
          <div className='numeric-stat'>{`Нынешняя: ${stats.strike}`}</div>
          {/*<div className='numeric-stat'>{`Рекорд: `}</div>
          <div className='numeric-stat'>{`Всего: `}</div>*/}
        </div>
        <div className='week-stat'>
          <div>{"Серия ежедневных отметок"}</div>
          <div className='week-days'>
            {weekDays.map((weekday) => weekday[0] ? <div className='week-day'>
              <img src={checkedWeekDay}/>
              {weekday[1] && <div>{'Сегодня'}</div>}
            </div> :
            <div className='week-day'>
              <img src={uncheckedWeekDay}/>
              {weekday[1] && <div>{'Сегодня'}</div>}
            </div>)}
          </div>
        </div>
      </div>
      <div className='stats-picture'>
          <img className='stat-picture-img' src={`data:image/png;base64,${statImage}`} alt="Received" />
      </div>
      <div>
        {/*Object.entries(stats).map(([key, value]) => (
          <p key={key}>
            <strong>{key}:</strong> {String(value)}
          </p>
        ))*/}
      </div>
    </div>
  );
}

export default Statistics;