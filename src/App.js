import React, { useState } from "react";
import axios from "axios";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const analyzeColor = async () => {
    const formData = new FormData();
    formData.append("file", image);
    const response = await axios.post("http://127.0.0.1:8000/analyze/", formData);
    setResult(response.data);
  };

  return (
    <div className="flex flex-col items-center p-5 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-5">Face Color Palette Analyzer</h1>
      <input type="file" onChange={handleUpload} className="mb-3" />
      {preview && <img src={preview} alt="Preview" className="w-40 h-40 object-cover rounded-lg" />}
      <button onClick={analyzeColor} className="mt-3 px-4 py-2 bg-blue-500 text-white rounded">
        Analyze
      </button>
      {result && (
        <div className="mt-5 text-lg">
          <p>✅ Best Color: <span className="font-bold text-green-600">{result.best_color}</span></p>
          <p>❌ Worst Color: <span className="font-bold text-red-600">{result.worst_color}</span></p>
        </div>
      )}
    </div>
  );
}

export default App;
