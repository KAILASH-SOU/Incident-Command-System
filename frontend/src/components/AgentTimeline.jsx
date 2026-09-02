import React, { useState, useEffect } from 'react';
import { Bot, Zap, Clock } from 'lucide-react';

const AgentTimeline = () => {
  const [thoughts, setThoughts] = useState([
    { id: 1, time: '10:00:00', agent: 'LeadOrchestrator', message: 'Incident detected. Initiating diagnostic workflow...' },
    { id: 2, time: '10:00:02', agent: 'LogAnalyzer', message: 'Analyzing burst of 5xx errors in auth-service.' },
    { id: 3, time: '10:00:05', agent: 'MetricsAgent', message: 'High CPU detected on payment-gateway prior to crash.' }
  ]);

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl overflow-hidden backdrop-blur-sm h-full flex flex-col">
      <div className="p-4 border-b border-slate-700 flex justify-between items-center bg-slate-800/50">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <Bot className="text-blue-400" /> Agent Swarm
        </h2>
        <span className="flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-blue-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
        </span>
      </div>
      <div className="p-5 flex-1 overflow-y-auto space-y-6">
        {thoughts.map((thought, index) => (
          <div key={thought.id} className="relative pl-6">
            {index !== thoughts.length - 1 && (
              <div className="absolute left-2.5 top-6 bottom-0 w-px bg-slate-700 -ml-px"></div>
            )}
            <div className="absolute left-0 top-1.5 rounded-full bg-blue-500/20 p-1 border border-blue-500/30">
              <Zap size={10} className="text-blue-400" />
            </div>
            <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-700/50 hover:border-blue-500/30 transition-colors">
              <div className="flex justify-between items-start mb-1">
                <span className="font-semibold text-blue-300 text-sm">{thought.agent}</span>
                <span className="text-xs text-slate-500 flex items-center gap-1"><Clock size={10} /> {thought.time}</span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{thought.message}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentTimeline;
