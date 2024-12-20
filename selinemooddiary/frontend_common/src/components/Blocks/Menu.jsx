import React from 'react';
import SectionButton from './SectionButton';
import '../../static/css/menu.css'
import BlockImageLightTheme from '../../assets/images/menuImages/Light_theme.png';
import BlockImageSettings from '../../assets/images/menuImages/Settings.png';

function Menu({ sectionList, changeSectionKey, setSettings }) {
  return (
    <div className='main-menu'>
        <h1>Меню</h1>
        <div className='separator'></div>
        <div className='separator'></div>
        {sectionList.map((section) => 
            <SectionButton key={section.id} imagesrc={section.imagesrc} sectionName={section.name} sectionKey={section.key} changeSectionKey={changeSectionKey}/>
        )}
        <div className='bottom-menu-block'>
          <button>
            <img src={BlockImageLightTheme}/>
          </button>
          <button onClick={() => setSettings(true)}>
            <img src={BlockImageSettings}/>
          </button>
        </div>
    </div>
  );
}

export default Menu;