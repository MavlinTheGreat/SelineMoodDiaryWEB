import React from 'react';

function SectionButton({ imagesrc, sectionName, sectionKey, changeSectionKey }) {
  return (
    <button className='section-button' onClick={() => changeSectionKey(sectionKey)}>
        <img src={imagesrc} />
        <h2>{sectionName}</h2>
    </button>
  );
}

export default SectionButton;