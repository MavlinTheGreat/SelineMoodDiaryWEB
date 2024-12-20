import React, { useState, useEffect } from 'react';
import Menu from '../Blocks/Menu';
import Calendar from '../Blocks/Calendar';
import Statistics from '../Blocks/Statistics';
import MentalHealth from '../Blocks/MentalHealth';
import Settings from '../Blocks/Settings';
import Tasks from '../Blocks/Tasks';
import '../../static/css/main.css'

import SectionImageCalendar from '../../assets/images/sectionImages/Calendar.png';
import SectionImageStatistics from '../../assets/images/sectionImages/Statistics.png';
import SectionImageMentalHealth from '../../assets/images/sectionImages/Mental_health.png';
import SectionImageTasks from '../../assets/images/sectionImages/Tasks.png';

const sectionList = [
  {
    id: 'section_Calendar',
    key: 'Calendar',
    imagesrc: SectionImageCalendar,
    name: 'Календарь',
  },
  {
    id: 'section_Statistics',
    key: 'Statistics',
    imagesrc: SectionImageStatistics,
    name: 'Статистика',
  },
  {
    id: 'section_MentalHealth',
    key: 'MentalHealth',
    imagesrc: SectionImageMentalHealth,
    name: 'Ментальное здоровье',
  },
  {
    id: 'section_Tasks',
    key: 'Tasks',
    imagesrc: SectionImageTasks,
    name: 'Задачи',
  },
]

const componentsMap = {
  'Calendar': <Calendar/>,
  'Statistics': <Statistics/>,
  'MentalHealth': <MentalHealth/>,
  'Tasks': <Tasks/>,
}

function Main() {
  
  const [activeSection, setActiveSection] = useState('Calendar');
  const [settings, setSettings] = useState(false);

  const changeSectionKey = (newSectionKey) => {
    setActiveSection(newSectionKey);
  }

  return (
    <div className='main-page'>
      <Menu sectionList={sectionList} changeSectionKey={changeSectionKey} setSettings={setSettings}/>
      <div className='active-section'>
        {componentsMap[activeSection] || <div>Страница не найдена</div>}
      </div>
      {settings && <Settings setSettings={setSettings}></Settings>}
    </div>
  );
}

export default Main;