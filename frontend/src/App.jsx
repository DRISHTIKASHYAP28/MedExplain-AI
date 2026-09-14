import { useState } from "react";
import LandingPage from "./components/LandingPage";
import Dashboard from "./components/Dashboard";

function App() {
  const [page, setPage] = useState("landing");

  if (page === "dashboard") {
    return <Dashboard onBack={() => setPage("landing")} />;
  }

  return <LandingPage onGetStarted={() => setPage("dashboard")} />;
}

export default App;