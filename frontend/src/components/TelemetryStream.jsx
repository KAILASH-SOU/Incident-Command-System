import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, XCircle, Info } from 'lucide-react';

const TelemetryStream = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // Simulated stream since we might not have the backend running instantly
    // In production, connect to SSE: new EventSource('http://localhost:8000/api/v1/stream/telemetry')
    const interval = setInterval(() => {
      const levels = ["INFO", "WARN", "ERROR", "FATAL"];
      const services = ["auth-service", "payment-gateway", "user-db"];
      const level = levels[Math.floor(Math.random() * levels.length)];
      
      setLogs(prev => {
        const newLog = {
          id: Date.now(),
          timestamp: new Date().toISOString().substring(11, 19),
          level,
          service: services[Math.floor(Math.random() * services.length)],
          message: level === 'ERROR' ? 'Connection timeout' : 'Request processed successfully'
        };
        return [newLog, ...prev].slice(0, 50);
      });
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);

  const getIcon = (level) => {
    switch (level) {
      case 'INFO': return <Info size={16} className="text-blue-400" />;
      case 'WARN': return <AlertTriangle size={16} className="text-yellow-400" />;
      case 'ERROR': return <XCircle size={16} className="text-red-400" />;
      case 'FATAL': return <XCircle size={16} className="text-red-600 animate-pulse" />;
      default: return <Activity size={16} />;
    }
  };

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl overflow-hidden backdrop-blur-sm">
      <div className="p-4 border-b border-slate-700 flex justify-between items-center bg-slate-800/50">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <Activity className="text-indigo-400" /> Live Telemetry
        </h2>
        <span className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-1 rounded-full animate-pulse">Live</span>
      </div>
      <div className="p-4 h-[300px] overflow-y-auto font-mono text-sm space-y-2 custom-scrollbar">
        {logs.map((log) => (
          <div key={log.id} className="flex gap-3 hover:bg-slate-700/50 p-2 rounded transition-colors group">
            <span className="text-slate-500">{log.timestamp}</span>
            {getIcon(log.level)}
            <span className="font-semibold text-slate-300 w-32 truncate">{log.service}</span>
            <span className="text-slate-400 flex-1 truncate group-hover:text-slate-200 transition-colors">{log.message}</span>
          </div>
        ))}
        {logs.length === 0 && <div className="text-center text-slate-500 mt-10">Awaiting telemetry...</div>}
      </div>
    </div>
  );
};

export default TelemetryStream;
