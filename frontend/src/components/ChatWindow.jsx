function ChatWindow({ messages, loading }) {
  return (
    <div
      className="border rounded p-3 mb-2"
      style={{ height: "350px", overflowY: "auto", background: "#f8f9fa" }}
    >
      {messages.map((m, idx) => (
        <div
          key={idx}
          className={`mb-2 d-flex ${
            m.sender === "user" ? "justify-content-end" : "justify-content-start"
          }`}
        >
          <div
            className={`p-2 rounded ${
              m.sender === "user" ? "bg-primary text-white" : "bg-light"
            }`}
          >
            {m.text}
          </div>
        </div>
      ))}
      {loading && (
      <div className="text-center text-muted mt-2">
         <em>Analyzing data, please wait...</em>
       </div>
      )}
    </div>
  );
}

export default ChatWindow;
