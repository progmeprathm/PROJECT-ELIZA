import React, { useState, useEffect } from 'react';

interface Document {
  id: string;
  title: string;
  content: string;
  source_url: string;
}

export default function Knowledge() {
  const [docs, setDocs] = useState<Document[]>([]);
  const [query, setQuery] = useState('');
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);

  const searchKnowledge = (q: string) => {
    fetch(`http://localhost:8001/api/knowledge?q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(data => {
        setDocs(data);
        if (data.length > 0 && !selectedDoc) {
          setSelectedDoc(data[0]);
        }
      })
      .catch(err => console.error(err));
  };

  useEffect(() => {
    searchKnowledge(query);
  }, [query]);

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Knowledge Base</h1>
        <p className="text-md-sys-color-secondary">Structured documentation and contextual indexing.</p>
      </header>

      <div className="flex gap-8 h-full min-h-0">
        {/* Sidebar */}
        <div className="w-[300px] bg-md-sys-color-surface-variant rounded-xl border border-md-sys-color-outline-variant p-4 flex flex-col">
          <div className="mb-4">
            <input 
              type="text" 
              placeholder="Search knowledge..." 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-md-sys-color-surface border border-md-sys-color-outline-variant rounded p-2 text-sm focus:outline-none focus:border-md-sys-color-primary"
            />
          </div>
          <div className="flex-1 overflow-y-auto">
            <ul className="flex flex-col gap-1">
              {docs.map(doc => (
                <li 
                  key={doc.id}
                  onClick={() => setSelectedDoc(doc)}
                  className={`${selectedDoc?.id === doc.id ? 'font-bold text-md-sys-color-primary bg-md-sys-color-primary-container/10' : 'text-md-sys-color-secondary hover:bg-md-sys-color-surface'} px-3 py-2 rounded cursor-pointer transition-colors whitespace-nowrap overflow-hidden text-ellipsis`}
                >
                  {doc.title}
                </li>
              ))}
              {docs.length === 0 && (
                <li className="text-md-sys-color-secondary px-3 py-2 text-sm italic">No results found</li>
              )}
            </ul>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 bg-md-sys-color-surface p-8 rounded-xl border border-md-sys-color-outline-variant overflow-y-auto prose prose-invert max-w-none">
          {selectedDoc ? (
            <>
              <h1 className="text-3xl font-bold mb-4 border-b border-md-sys-color-outline-variant pb-2">{selectedDoc.title}</h1>
              <p className="text-md-sys-color-secondary mb-4 text-sm font-mono tracking-widest">ID: {selectedDoc.id}</p>
              
              <div className="whitespace-pre-wrap text-md-sys-color-on-surface">
                {selectedDoc.content || 'No content provided.'}
              </div>
            </>
          ) : (
            <div className="text-md-sys-color-secondary h-full flex items-center justify-center">
              Select a document to view its contents
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
