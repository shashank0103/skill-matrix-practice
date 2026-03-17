import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [questions, setQuestions] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("https://skill-matrix-practice.onrender.com/upload", formData);
    setSkills(res.data.skills);

    const q = await axios.post("https://skill-matrix-practice.onrender.com/generate", {
      skills: res.data.skills,
    });

    setQuestions(q.data.questions);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Resume Analyzer</h2>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Analyze</button>

      <h3>Skills:</h3>
      <p>{skills.join(", ")}</p>

      <h3>Questions:</h3>
      <pre>{questions}</pre>
    </div>
  );
}

export default App;
