import { useState } from 'react';
import './App.css';

function MyButton({count, handleClick}) {
  return (
    <button onClick={handleClick}>I have been clicked {count} times</button>
  )
}


function Parent() {
  const [count, setCount] = useState(0);
  
  function handleClick() {
    setCount(count + 1)
  }

  return (
    <>
      <h1>Counters that update together</h1>
      <MyButton count={count} handleClick={handleClick} />
      <MyButton count={count} handleClick={handleClick} />
    </>
  )

}



function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Parent />
      </header>
    </div>
  );
}

export default App;
