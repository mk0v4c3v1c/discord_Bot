import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import { listenToUpdates } from '../services/socket';
import GuildStatus from '../components/GuildStatus';
import FeatureStatusCard from '../components/FeatureStatusCard';
import UserManagement from '../components/UserManagement';
import LogViewer from '../components/LogViewer';
import BotControls from '../components/BotControls';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const [users, setUsers] = useState([]);
  const [stocks, setStocks] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [guilds, setGuilds] = useState(0);
  const [features, setFeatures] = useState([
  { name: 'AI Chat', active: true },
  { name: 'Economy', active: true },
  { name: 'Music', active: false }
]);

const [botStatus, setBotStatus] = useState({
  uptime: '2h 45m',
  memory: '256'
});


  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));

    fetch('/api/stocks')
      .then(res => res.json())
      .then(data => setStocks(data));
  }, []);

    useEffect(() => {
    listenToUpdates((data) => {
      if (data.type === 'guild_update') setGuilds(data.count);
    });
  }, []);

 useEffect(() => {
    listenToUpdates((data) => {
      if (data.type === 'guild_update') setGuilds(data.count);
    });
  }, []);

  const userData = {
    labels: users.map(user => user.username),
    datasets: [
      {
        label: 'XP',
        data: users.map(user => user.xp),
        backgroundColor: 'rgba(99, 102, 241, 0.5)',
      },
      {
        label: 'Level',
        data: users.map(user => user.level),
        backgroundColor: 'rgba(16, 185, 129, 0.5)',
      }
    ]
  };

  const stockData = {
    labels: stocks.map(stock => stock.symbol),
    datasets: [
      {
        label: 'Price',
        data: stocks.map(stock => stock.price),
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
      }
    ]
  };

  return (
    <div className="p-6">
      <div className="flex mb-6">
        <button
          className={`px-4 py-2 mr-2 ${activeTab === 'overview' ? 'bg-indigo-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`px-4 py-2 mr-2 ${activeTab === 'users' ? 'bg-indigo-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={`px-4 py-2 ${activeTab === 'stocks' ? 'bg-indigo-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveTab('stocks')}
        >
          Stock Market
        </button>
      </div>
      //admin
      <button
        className={`px-4 py-2 mr-2 ${activeTab === 'admin' ? 'bg-indigo-600 text-white' : 'bg-gray-200'}`}
        onClick={() => setActiveTab('admin')}
      >
      Admin
      </button>

      {activeTab === 'overview' && (
        <div>
          <h2 className="text-xl font-bold mb-4">Server Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-white p-4 rounded shadow">
              <h3 className="font-semibold mb-2">Top Users by XP</h3>
              <div className="h-64">
                <Bar data={userData} />
              </div>
            </div>
            <div className="bg-white p-4 rounded shadow">
              <h3 className="font-semibold mb-2">Stock Prices</h3>
              <div className="h-64">
                <Line data={stockData} />
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div>
          <h2 className="text-xl font-bold mb-4">User Management</h2>
          <div className="bg-white rounded shadow overflow-hidden">
            <table className="min-w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Level</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">XP</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Coins</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {users.map(user => (
                  <tr key={user.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {user.avatar && (
                          <img
                            className="h-10 w-10 rounded-full"
                            src={`https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`}
                            alt=""
                          />
                        )}
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{user.username}</div>
                          <div className="text-sm text-gray-500">{user.discriminator}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{user.level}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{user.xp}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{user.coins}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'admin' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <BotControls botStatus={botStatus} onCommand={() => fetchStatus()} />
            <FeatureStatusCard features={features} />
        </div>
        <UserManagement users={users} />
        <LogViewer />
        </div>
      )}

      {activeTab === 'stocks' && (
        <div>
          <h2 className="text-xl font-bold mb-4">Stock Market</h2>
          <div className="bg-white rounded shadow overflow-hidden">
            <table className="min-w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Symbol</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Volatility</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {stocks.map(stock => (
                  <tr key={stock.symbol}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{stock.symbol}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{stock.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">${stock.price.toFixed(2)}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{(stock.volatility * 100).toFixed(1)}%</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}