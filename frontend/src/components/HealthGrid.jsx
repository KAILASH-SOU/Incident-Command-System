import React from 'react';
import { Server, Database, Globe, Shield } from 'lucide-react';

const HealthGrid = () => {
  const nodes = [
    { name: 'auth-service', status: 'critical', icon: <Shield size={20} /> },
    { name: 'payment-gateway', status: 'degraded', icon: <Globe size={20} /> },
    { name: 'user-db', status: 'healthy', icon: <Database size={20} /> },
    { name: 'frontend-proxy', status: 'healthy', icon: <Server size={20} /> }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {nodes.map(node => (
        <div key={node.name} className="bg-slate-800 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center gap-3 transition-transform hover:scale-105 shadow-lg">
          <div className={`p-3 rounded-full ${
            node.status === 'healthy' ? 'bg-emerald-500/20 text-emerald-400' :
            node.status === 'degraded' ? 'bg-yellow-500/20 text-yellow-400' :
            'bg-red-500/20 text-red-400 animate-pulse'
          }`}>
            {node.icon}
          </div>
          <div className="text-center">
            <h3 className="font-medium text-sm text-slate-200">{node.name}</h3>
            <p className={`text-xs uppercase tracking-wider font-semibold mt-1 ${
              node.status === 'healthy' ? 'text-emerald-500' :
              node.status === 'degraded' ? 'text-yellow-500' :
              'text-red-500'
            }`}>{node.status}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default HealthGrid;
