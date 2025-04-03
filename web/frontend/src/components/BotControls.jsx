import React, { useState } from 'react';

export default function BotControls({ botStatus, onCommand }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleCommand = async (command) => {
    setIsLoading(true);
    try {
      await fetch(`/api/bot/${command}`, { method: 'POST' });
      onCommand();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-bold text-lg mb-3">Bot Controls</h3>
      <div className="grid grid-cols-2 gap-4">
        <button
          onClick={() => handleCommand('restart')}
          disabled={isLoading}
          className="bg-yellow-500 text-white p-2 rounded disabled:opacity-50"
        >
          {isLoading ? 'Processing...' : 'Soft Restart'}
        </button>
        <button
          onClick={() => handleCommand('update')}
          disabled={isLoading}
          className="bg-blue-500 text-white p-2 rounded disabled:opacity-50"
        >
          {isLoading ? 'Updating...' : 'Update Cogs'}
        </button>
        <button
          onClick={() => handleCommand('stop')}
          disabled={isLoading}
          className="bg-red-500 text-white p-2 rounded disabled:opacity-50 col-span-2"
        >
          {isLoading ? 'Stopping...' : 'Emergency Stop'}
        </button>
      </div>
      <div className="mt-4 p-3 bg-gray-50 rounded">
        <p className="font-semibold">Current Status:</p>
        <p>Uptime: {botStatus.uptime}</p>
        <p>Memory: {botStatus.memory} MB</p>
      </div>
    </div>
  );
}