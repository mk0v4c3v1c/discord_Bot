import { useEffect, useState } from 'react';
import { listenToUpdates } from '../services/socket';

export default function GuildStatus() {
  const [guilds, setGuilds] = useState(0);

  useEffect(() => {
    listenToUpdates((data) => {
      if (data.type === 'guild_update') {
        setGuilds(data.count);
      }
    });
  }, []);

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-bold text-lg mb-2">Server Status</h3>
      <div className="flex items-center">
        <span className="h-3 w-3 bg-green-500 rounded-full mr-2"></span>
        <span>Active in {guilds} servers</span>
      </div>
    </div>
  );
}