import React, { useState, useEffect } from 'react';
import '../../static/css/calendar.css'
import DateList from './DateList';
{/*import NoteRedactor from './NoteRedactor';*/}

const Calendar = () => {
  
  const createNote = () => {
    alert("Запись пока не создаётся, но я крут");
  }

  return (
    <div className='calendar-section'>
      <DateList createNote={createNote}></DateList>
    </div>
  );
};

export default Calendar;