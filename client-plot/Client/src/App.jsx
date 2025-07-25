import { BrowserRouter, Routes, Route} from "react-router-dom";
import { Inicio } from "./pages/inicio";
import SP500 from "./pages/grafica";
import DownJones from "./pages/downJones";

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Inicio />} />
          <Route path="/DownJones" element={<DownJones />} />
          <Route path="/SP500" element={<SP500 />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App