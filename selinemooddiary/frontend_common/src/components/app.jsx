import React, { useState } from 'react';
import { render } from "react-dom";

function App() {

    const [count, changeCount] = useState(0);

    const plusCount = (e) => {
        changeCount(
            count + 1
        );
    }

    return(
        <div>
            <h1>{ count }</h1>
            <button onClick={(e) => plusCount(e)}>+</button>
        </div>
    );
}

export default App;

const container = document.getElementById("app");
render(<App />, container);