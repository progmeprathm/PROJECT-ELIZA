import React, { useState, useEffect } from 'react';

interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  
  useEffect(() => {
    fetch('http://localhost:8001/api/projects')
      .then(res => res.json())
      .then(data => setProjects(data))
      .catch(err => console.error(err));
  }, []);

  const createProject = () => {
    fetch('http://localhost:8001/api/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'New Project', description: 'A newly created project' })
    })
    .then(res => res.json())
    .then(data => setProjects([...projects, data]))
    .catch(err => console.error(err));
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto animate-[fadeIn_0.3s_ease-out] h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Projects Federation</h1>
        <p className="text-md-sys-color-secondary">Isolated workspaces mapped to different codebases or initiatives.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {projects.map(proj => (
          <div key={proj.id} className="bg-md-sys-color-surface-variant p-6 rounded-xl border-2 border-md-sys-color-primary cursor-pointer">
            <div className="flex justify-between items-start mb-4">
              <span className="material-symbols-outlined text-4xl text-md-sys-color-primary">rocket_launch</span>
              <span className="bg-md-sys-color-primary text-md-sys-color-on-primary px-3 py-1 text-xs rounded-full font-bold">{proj.status?.toUpperCase() || 'ACTIVE'}</span>
            </div>
            <h2 className="text-xl font-bold mb-2">{proj.name}</h2>
            <p className="text-md-sys-color-secondary text-sm mb-4">{proj.description}</p>
            <div className="text-xs font-mono text-md-sys-color-tertiary">{proj.id}</div>
          </div>
        ))}

        <div onClick={createProject} className="bg-md-sys-color-surface p-6 rounded-xl border border-md-sys-color-outline-variant border-dashed cursor-pointer hover:border-md-sys-color-secondary transition-colors flex flex-col items-center justify-center text-md-sys-color-secondary min-h-[200px]">
          <span className="material-symbols-outlined text-4xl mb-2">add_circle</span>
          <h2 className="font-bold">Create New Project</h2>
        </div>
      </div>
    </div>
  );
}
