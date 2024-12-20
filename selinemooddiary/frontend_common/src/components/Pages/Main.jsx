import React, { useState, useEffect } from 'react';
import Menu from '../Blocks/Menu';
import Calendar from '../Blocks/Calendar';
import Statistics from '../Blocks/Statistics';
import MentalHealth from '../Blocks/MentalHealth';
import Tasks from '../Blocks/Tasks';
import '../../static/css/main.css'

import SectionImageCalendar from '../../assets/images/sectionImages/Calendar.png';
import SectionImageStatistics from '../../assets/images/sectionImages/Statistics.png';
import SectionImageMentalHealth from '../../assets/images/sectionImages/Mental_health.png';
import SectionImageTasks from '../../assets/images/sectionImages/Tasks.png';

import EmotionEmojiCool from '../../assets/images/emotionEmojis/Emoji_cool.png';
import EmotionEmojiFrown from '../../assets/images/emotionEmojis/Emoji_frown.png';
import EmotionEmojiLove from '../../assets/images/emotionEmojis/Emoji_love.png';
import EmotionEmojiNice from '../../assets/images/emotionEmojis/Emoji_nice.png';
import EmotionEmojiSad from '../../assets/images/emotionEmojis/Emoji_sad.png';
import EmotionEmojiSob from '../../assets/images/emotionEmojis/Emoji_sob.png';

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

const emotionEmojiList = [
  {
    key: 'emotion_Cool',
    imagesrc: EmotionEmojiCool,
    name: 'Круто',
  },
  {
    key: 'emotion_Frowm',
    imagesrc: EmotionEmojiFrown,
    name: 'Плохо',
  },
  {
    key: 'emotion_Love',
    imagesrc: EmotionEmojiLove,
    name: 'В любви',
  },
  {
    key: 'emotion_Nice',
    imagesrc: EmotionEmojiNice,
    name: 'Хорошо',
  },
  {
    key: 'emotion_Sad',
    imagesrc: EmotionEmojiSad,
    name: 'Грустно',
  },
  {
    key: 'emotion_Sob',
    imagesrc: EmotionEmojiSob,
    name: 'Плачу',
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

  const changeSectionKey = (newSectionKey) => {
    setActiveSection(newSectionKey);
  }

  return (
    <div className='main-page'>
      <Menu sectionList={sectionList} changeSectionKey={changeSectionKey}/>
      <div className='active-section'>
        {componentsMap[activeSection] || <div>Страница не найдена</div>}
      </div>
    </div>
  );
}

export default Main;