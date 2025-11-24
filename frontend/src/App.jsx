import { useState } from "react";
import ChatInput from "./components/ChatInput";
import ChatWindow from "./components/ChatWindow";
import AnalysisResult from "./components/AnalysisResult";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metric, setMetric] = useState("price"); 

  const handleSend = async (text) => {
    if (!text.trim()) return;

    const userMsg = { sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      console.log("FRONTEND metric sending:", metric);

      const res = await axios.post(
        "http://localhost:8000/api/analyze/",
        {
          query: text,
          metric: metric, 
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = res.data;
      const botMsg = {
        sender: "bot",
        text: data.summary,
      };

      setMessages((prev) => [...prev, botMsg]);
      setAnalysis({
        chartData: data.chartData,
        tableData: data.tableData,
        metric: data.metric,
        areas: data.areas,
      });
    } catch (err) {
      console.error(err);
      const botMsg = {
        sender: "bot",
        text: "Sorry, kuch error aagaya data analyze karte time.",
      };
      setMessages((prev) => [...prev, botMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-4">
      <h2 className="mb-3">Real Estate Analysis Chatbot</h2>
      <div className="mb-3 d-flex align-items-center gap-2">
        <span>Metric:</span>
        <select
          className="form-select"
          style={{ width: "220px" }}
          value={metric}
          onChange={(e) => setMetric(e.target.value)}
        >
          <option value="price">Price (total sales)</option>
          <option value="demand">Demand (total sold)</option>
        </select>
      </div>

      <div className="row">
        <div className="col-md-5 mb-3">
          <ChatWindow messages={messages} loading={loading} />
          <ChatInput onSend={handleSend} />
        </div>
        <div className="col-md-7">
          <AnalysisResult analysis={analysis} />
        </div>
      </div>
    </div>
  );
}

export default App;
