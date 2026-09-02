import React from 'react';
import TelemetryStream from './components/TelemetryStream';
import HealthGrid from './components/HealthGrid';
import AgentTimeline from './components/AgentTimeline';
import RcaReport from './components/RcaReport';

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-50 p-6 font-sans">
      <header className="mb-8 border-b border-slate-700 pb-4">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
          SentinelCore
        </h1>
        <p className="text-slate-400 mt-1">Incident Command & Root Cause Analysis</p>
      </header>
      
      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <HealthGrid />
          <TelemetryStream />
          <RcaReport />
        </div>
        <div className="space-y-6">
          <AgentTimeline />
        </div>
      </main>
    </div>
  );
}

export default App;
