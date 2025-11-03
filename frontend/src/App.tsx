import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/Home";
import PlayerPage from "./pages/Player";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Default route — home */}
        <Route path="/" element={<HomePage />} />

        {/* Dynamic route — player profile */}
        <Route path="/player/:name" element={<PlayerPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
