import React, { useState, useEffect } from 'react';
import '../../static/css/calendar.css'
import DateList from './DateList';
import NoteRedactor from './NoteRedactor';

const Calendar = () => {

  const [selectedDate, setSelectedDate] = useState(new Date());
  const [usedPart, setUsedPart] = useState("dateList");
  
  const createNote = (date) => {
    setSelectedDate(date);
    setUsedPart("noteRedactor");
  }

  const componentsMap = {
    'dateList': <DateList createNote={createNote}></DateList>,
    'noteRedactor': <NoteRedactor date={selectedDate} setUsedPart={setUsedPart}/>,
  }

  return (
    <div className='calendar-section'>
      {componentsMap[usedPart] || <div>Страница не найдена</div>}
    </div>
  );
};

export default Calendar;