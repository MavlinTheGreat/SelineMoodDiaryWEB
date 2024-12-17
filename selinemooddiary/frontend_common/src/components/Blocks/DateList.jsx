import React, { useState, useEffect } from 'react';
import '../../static/css/calendar.css'

const DateList = ({ makeNoteForDay }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [daysInMonth, setDaysInMonth] = useState([]);

  useEffect(() => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const daysArray = Array.from({ length: daysInMonth }, (_, i) => i + 1);
    const offsetDays = Array.from({ length: firstDay }, () => null);
    setDaysInMonth([...offsetDays, ...daysArray]);
  }, [currentDate]);

  const goToPreviousMonth = () => {
    setCurrentDate(prevDate => new Date(prevDate.getFullYear(), prevDate.getMonth() - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(prevDate => new Date(prevDate.getFullYear(), prevDate.getMonth() + 1, 1));
  };

  const getMonthName = (monthIndex) => {
    const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    return monthNames[monthIndex];
  };

  return (
    <div className="date-list">
      <div className="date-list-header">
        <button onClick={goToPreviousMonth}>&lt;</button>
        <h2>{getMonthName(currentDate.getMonth())} {currentDate.getFullYear()}</h2>
        <button onClick={goToNextMonth}>&gt;</button>
      </div>
      
      <div className="date-list-grid">
        {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day, index) => (
          <div key={index} className="calendar-day-name">{day}</div>
        ))}
        
        {daysInMonth.map((day, index) => (
          <div
            key={index}
            className={`calendar-day ${day ? '' : 'empty'}`}
            onClick={() => makeNoteForDay(year=currentDate.getFullYear, month=currentDate.getMonth, day=day)}
          >
            {day}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DateList;