import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css';
import Home from './pages/Home';
import NovelInput from "./pages/NovelInput";
import SelectCharacter from "./pages/SelectCharacter";
import Chat from "./pages/Chat";
import SelectNovel from "./pages/SelectNovel";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/selectnovel' element={<SelectNovel />} />
          <Route path='/novelinput' element={<NovelInput />} />
          <Route path='/selectcharacter' element={<SelectCharacter />} />
          <Route path='/chat' element={<Chat />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
