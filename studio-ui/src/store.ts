import { create } from 'zustand';

interface TraceEvent {
  content: string;
  module: string;
}

interface AppState {
  goals: any[];
  trace: TraceEvent;
  setGoals: (goals: any[]) => void;
  addGoal: (goal: any) => void;
  setTrace: (trace: TraceEvent) => void;
  connectWebSocket: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  goals: [],
  trace: { content: "Waiting for Kernel...", module: "System" },
  
  setGoals: (goals) => set({ goals }),
  
  addGoal: (goal) => set((state) => ({ goals: [...state.goals, goal] })),
  
  setTrace: (trace) => set({ trace }),
  
  connectWebSocket: () => {
    const ws = new WebSocket('ws://localhost:8001/ws/stream');
    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === 'thought') {
          set({ trace: { content: payload.content, module: payload.module } });
        }
      } catch (e) {
        console.error("Failed to parse WS msg", e);
      }
    };
    ws.onclose = () => {
      console.warn("WebSocket disconnected. Reconnecting in 5s...");
      setTimeout(() => set((state) => ({ ...state, trace: { content: "Reconnecting...", module: "System" } })), 5000);
    };
  }
}));
