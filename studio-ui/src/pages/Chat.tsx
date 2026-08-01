import React, { useState } from 'react';

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Welcome to the legacy conversational interface.' }
  ]);
  const [input, setInput] = useState('');

  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;
    
    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await fetch('http://localhost:8001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'system', content: data.response }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'system', content: "Error connecting to ECOS Kernel." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Legacy Chat</h1>
        <p className="text-md-sys-color-secondary">Standard conversational interface for direct querying.</p>
      </header>

      <div className="flex-1 bg-md-sys-color-surface border border-md-sys-color-outline-variant rounded-xl flex flex-col overflow-hidden">
        
        <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[70%] p-4 rounded-xl ${m.role === 'user' ? 'bg-md-sys-color-primary text-md-sys-color-on-primary' : 'bg-md-sys-color-surface-variant border border-md-sys-color-outline-variant'}`}>
                {m.content}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSend} className="p-4 bg-md-sys-color-surface-variant border-t border-md-sys-color-outline-variant flex gap-4">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Send a message to ELIZA..." 
            className="flex-1 bg-md-sys-color-surface border border-md-sys-color-outline-variant rounded-lg p-3 text-sm focus:outline-none focus:border-md-sys-color-primary"
          />
          <button type="submit" className="bg-md-sys-color-primary text-md-sys-color-on-primary px-6 py-3 rounded-lg font-bold hover:opacity-90 transition-opacity">
            Send
          </button>
        </form>

      </div>
    </div>
  );
}
