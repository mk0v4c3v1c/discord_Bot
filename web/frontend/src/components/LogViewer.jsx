import React, { useState, useEffect } from 'react';

export default function LogViewer() {
  const [logs, setLogs] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch(`/api/logs?filter=${filter}`)
      .then(res => res.json())
      .then(data => setLogs(data));
  }, [filter]);

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-bold text-lg">System Logs</h3>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="border rounded p-1"
        >
          <option value="all">All</option>
          <option value="error">Errors</option>
          <option value="warning">Warnings</option>
          <option value="info">Info</option>
        </select>
      </div>
      <div className="h-96 overflow-y-auto font-mono text-sm">
        {logs.map((log, index) => (
          <div
            key={index}
            className={`p-2 border-b ${log.level === 'error' ? 'bg-red-50' : log.level === 'warning' ? 'bg-yellow-50' : ''}`}
          >
            <span className="text-gray-500">[{new Date(log.timestamp).toLocaleString()}]</span>
            <span className={`ml-2 font-semibold ${log.level === 'error' ? 'text-red-600' : log.level === 'warning' ? 'text-yellow-600' : 'text-gray-600'}`}>
              {log.level.toUpperCase()}:
            </span>
            <span className="ml-2">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}