import React, { useState, useEffect, useContext, useRef } from 'react';
import AuthContext from '../../context/AuthContext'
import closeImg from '../../assets/images/close.png';

function Settings({ setSettings }) {
    
  const {logoutUser} = useContext(AuthContext);

  const selfRef = useRef(null);
  
  const [leftMove, setLeftMove] = useState("");
  const [topMove, setTopMove] = useState("");

  useEffect(() => {
    const updateBodyHeight = () => {
      if (selfRef.current) {
        const bodyHeight = document.body.offsetHeight;
        const bodyWidth = document.body.offsetWidth;
        const selfHeight = selfRef.current.offsetWidth;
        const selfWidth = selfRef.current.offsetHeight;
        setTopMove(`calc((${bodyHeight}px - ${selfHeight}px) / 2)`);
        setLeftMove(`calc((${bodyWidth}px - ${selfWidth}px) / 2)`);
      }
    };

    updateBodyHeight();
    window.addEventListener('resize', updateBodyHeight);

    return () => window.removeEventListener('resize', updateBodyHeight);
  }, []);

  return (
    <div
      className='settings-menu'
      ref={selfRef}
      style={{
        top: topMove,
        left: leftMove,
      }}
    >
        <div className='settings-header'>
          <h1>Настройки</h1>
          <button onClick={() => setSettings(false)}><img src={closeImg}/></button>
        </div>
        <div className='separator'></div>
        <div className='separator'></div>
        <button className='logout-button' onClick={() => logoutUser()}>Выйти из аккаунта</button>
    </div>
  );
}

export default Settings;