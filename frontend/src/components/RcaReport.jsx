import React from 'react';
import { FileText, CheckCircle2 } from 'lucide-react';

const RcaReport = () => {
  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl overflow-hidden backdrop-blur-sm">
      <div className="p-4 border-b border-slate-700 flex justify-between items-center bg-slate-800/50">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <FileText className="text-emerald-400" /> RCA Report
        </h2>
        <div className="flex items-center gap-1 text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded text-xs font-semibold">
          <CheckCircle2 size={14} /> 92% Confidence
        </div>
      </div>
      <div className="p-6 prose prose-invert max-w-none">
        <h3 className="text-xl text-slate-100 font-bold mb-4">Auth Service Degradation</h3>
        
        <div className="mb-4">
          <h4 className="text-indigo-300 font-semibold mb-2">Root Cause</h4>
          <p className="text-slate-300 text-sm leading-relaxed">
            A recent database migration executed an <code>ALTER TABLE</code> operation on the <code>users</code> table, triggering a table lock. This exhausted connection pools in the <code>auth-service</code>, resulting in a cascading failure of 5xx errors.
          </p>
        </div>
        
        <div>
          <h4 className="text-indigo-300 font-semibold mb-2">Remediation Steps</h4>
          <ul className="list-disc pl-5 text-sm text-slate-300 space-y-1">
            <li>Kill the blocking database migration transaction.</li>
            <li>Restart <code>auth-service</code> pods to clear dead connections.</li>
            <li>Schedule heavy migrations during maintenance windows.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RcaReport;
