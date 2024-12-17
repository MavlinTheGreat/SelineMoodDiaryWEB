import React, { useState, useEffect } from 'react';
//import DateList from './DateList';
import '../../static/css/calendar.css'

const EmotionChoice = ({ chooseEmotion }) => {
  
  const emotionEmojiList = React.useContext(EmotionContext);
  const [isHovered, setIsHovered] = useState(emotionEmojiList.map(() => false));

  const handleMouseEnter = (index) => {
    setIsHovered((prev) => prev.map((val, i) => (i === index ? true : val)));
  };

  const handleMouseLeave = (index) => {
    setIsHovered((prev) => prev.map((val, i) => (i === index ? false : val)));
  };

  const angleStep = 360 / emotionEmojiList.length;

  return (
    <div className="emotion-choice">
      <div className="center-item">Как ты себя чувствуешь сегодня?</div> 
      {emotionEmojiList.map((emotion, index) => {
        const angle = index * angleStep;
        return (
          <div className='image-contaner'>
            <img 
              key={emotion.key}
              className="circle-item"
              src={emotion.imagesrc}
              style={{ 
                transform: `translate(-50%, -50%) rotate(${angle}deg) translate(120px) rotate(-${angle}deg)` 
              }}
              onMouseEnter={() => handleMouseEnter(index)} 
              onMouseLeave={() => handleMouseLeave(index)}
            />
            {isHovered[index] && (
            <div className="emotion-tooltip">
              {emotionEmojiList.name}
            </div>
          )}
          </div>
        );
      })}
    </div>
  );
};

export default EmotionChoice;