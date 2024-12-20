import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../../static/css/calendar.css'

const EmotionChoice = ({ chooseEmotion }) => {
  
  const [emotions, setEmotions] = useState([]);

  const [componentHeight, setComponentHeight] = useState("");
  const [imageSize, setImageSize] = useState("");
  const [imageMove, setImageMove] = useState("");
  const [translateDistance, setTranslateDistance] = useState("");

  useEffect(() => {
    const updateBodyHeight = () => {
      const bodyHeight = document.body.style.height;
      setComponentHeight(`calc(${bodyHeight} - 12rem)`);
      setImageSize(`calc((${bodyHeight}) / 8)`);
      setImageMove(`calc(50% - (${imageSize} / 2)`);
      setTranslateDistance(`calc((${bodyHeight} - 14rem) / 2.5)`);
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
  
  const [isHovered, setIsHovered] = useState([]);

  const handleMouseEnter = (index) => {
    setIsHovered((prev) => prev.map((val, i) => (i === index ? true : val)));
  };

  const handleMouseLeave = (index) => {
    setIsHovered((prev) => prev.map((val, i) => (i === index ? false : val)));
  };

  useEffect(() => {
    setIsHovered(new Array(emotions.length).fill(false));
  }, [emotions.length]);

  const angleStep = 360 / emotions.length;

  return (
    <div
      style={{
        height: componentHeight,
        width: componentHeight
      }}
      className="emotion-choice"
    >
      <div className="center-item">Как ты себя чувствуешь?</div> 
      {emotions.map((emotion, index) => {
        const angle = index * angleStep;
        return (
          <div 
            key={emotion.id} 
            className='image-container'
            style={{ 
              position: 'absolute', 
              left: imageMove, 
              top: imageMove, 
              transform: `rotate(${angle}deg) translate(${translateDistance}) rotate(-${angle}deg)`,
              width: imageSize,
              height: imageSize
            }}
          >
            <img 
              className="circle-item"
              src={emotion.imageIcon}
              onMouseEnter={() => handleMouseEnter(index)} 
              onMouseLeave={() => handleMouseLeave(index)}
              onClick={() => chooseEmotion(emotion.id)}
            />
            {isHovered[index] && (
              <div className="emotion-tooltip">
                {emotion.name}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default EmotionChoice;
