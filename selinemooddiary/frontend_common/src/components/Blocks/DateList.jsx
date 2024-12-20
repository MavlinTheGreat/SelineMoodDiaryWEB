import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../../context/AuthContext';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';
import '../../static/css/calendar.css'

const DateList = ({ createNote }) => {
    
  const {loginUser} = useContext(AuthContext);
  
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [emotions, setEmotions] = useState([]);
  const [notes, setNotes] = useState([]);
  const today = new Date();
  
  useEffect(() => {
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchEmotions = async () => {
        try {
          
          const response = await axios.get('http://127.0.0.1:8000/api/journal/emotions', {
            headers: { Authorization: "Bearer " + parsedTokens.access },
          });
          
          setEmotions(response.data);
        } catch (err) {
          alert(err.message);
        }
      };
      
      fetchEmotions();
    }
  }, []);
  
  useEffect(() => {
    
    const token = localStorage.getItem("authTokens");

    if (token) {
      const parsedTokens = JSON.parse(token);
      
      const fetchNotes = async () => {
        try {
          
          const response = await axios.get('http://127.0.0.1:8000/api/journal/notes', {
            params: {
              start_date: currentDate.getFullYear().toString() + "-" + (currentDate.getMonth() + 1).toString() + "-1",
              end_date: currentDate.getFullYear().toString() + "-" + (currentDate.getMonth() + 1).toString() + "-" + new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate().toString(), 
            },
            headers: { Authorization: "Bearer " + parsedTokens.access },
          });
          
          setNotes(response.data);
        } catch (err) {
          alert(err.message);
        }
      };
      
      fetchNotes();
    }
  }, [currentDate]);

  const daysInMonth = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const days = new Date(year, month + 1, 0).getDate();
    return days;
  };

  const firstDayOffset = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    return new Date(year, month, 1).getDay(); // смещение первого дня месяца
  };

  const handleDayClick = (day) => {
    const date = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      day
    );
    setSelectedDate(date);
    createNote(date);
  };

  const goToPreviousMonth = () => {
    setCurrentDate(
      new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1)
    );
  };

  const goToNextMonth = () => {
    setCurrentDate(
      new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1)
    );
  };

  const renderDays = () => {
    const days = [];
    const totalDays = daysInMonth();
    const offset = firstDayOffset() === 0 ? 6 : firstDayOffset() - 1; // Пн как первый день недели

    // Добавление пустых ячеек
    for (let i = 0; i < offset; i++) {
      days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
    }

    // Добавление дней месяца
    for (let day = 1; day <= totalDays; day++) {
      const isToday =
        day === today.getDate() &&
        currentDate.getMonth() === today.getMonth() &&
        currentDate.getFullYear() === today.getFullYear();

      const isSelected =
        selectedDate &&
        day === selectedDate.getDate() &&
        currentDate.getMonth() === selectedDate.getMonth() &&
        currentDate.getFullYear() === selectedDate.getFullYear();

      let currentNote = {
      };

      try {
        currentNote = notes.find((note) => note.date.split('T')[0] === String(currentDate.getFullYear()) + "-" + String(currentDate.getMonth() + 1).padStart(2, '0') + "-" + String(day).padStart(2, '0'));
      } catch (err) {
        currentNote = {
          emotion: 0
        };
      }

      days.push(
        <div
          key={day}
          className={`calendar-day ${isToday ? "today" : ""} ${
            isSelected ? "selected" : ""
          }`}
          onClick={() => handleDayClick(day)}
        >

          {currentNote && (<img src={emotions.find((emotion) => emotion.id === currentNote.emotion).imageIcon}/>)}
          {day}

        </div>
      );
    }

    return days;
  };

  const getMonthYear = () => {
    let initialMonthYear = currentDate.toLocaleString("default", {
      month: "long",
      year: "numeric",
    })
    return initialMonthYear.charAt(0).toUpperCase() + initialMonthYear.slice(1)
  }

  return (
    <div className="calendar">
      <div className="calendar-header">
        <button onClick={goToPreviousMonth}>&lt;</button>
        <span>
          {getMonthYear()}
        </span>
        <button onClick={goToNextMonth}>&gt;</button>
      </div>
      <div className="calendar-grid">
        {["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"].map((day, index) => (
          <div key={index} className="calendar-day-name">
            {day}
          </div>
        ))}
        {renderDays()}
      </div>
      {/*<div>
        {Object.entries(notes.find((note) => note.date.split('T')[0] === String(currentDate.getFullYear()) + "-" + String(currentDate.getMonth() + 1).padStart(2, '0') + "-01")).map(([key, value]) => 
        <p>{key}: {value}</p>
        )}
      </div>
      <div>
        {notes.map((item) => 
        (<div>
          {Object.entries(item).map(([key, value]) => (
              <p key={key}>
                <strong>{key}:</strong> {value}
              </p>
            ))}
        </div>)
        )}
      </div>*/}
    </div>
  );
};

export default DateList;