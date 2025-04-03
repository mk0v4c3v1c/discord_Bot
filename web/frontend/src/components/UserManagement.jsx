import React, { useState } from 'react';

export default function UserManagement({ users }) {
  const [editingId, setEditingId] = useState(null);
  const [tempRoles, setTempRoles] = useState({});

  const handleEdit = (userId, currentRoles) => {
    setEditingId(userId);
    setTempRoles({ ...tempRoles, [userId]: currentRoles });
  };

  const handleSave = (userId) => {
    // API poziv za čuvanje promena
    fetch(`/api/users/${userId}`, {
      method: 'PATCH',
      body: JSON.stringify({ roles: tempRoles[userId] })
    });
    setEditingId(null);
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <table className="min-w-full">
        {/* Table Header */}
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left">User</th>
            <th className="px-6 py-3 text-left">Roles</th>
            <th className="px-6 py-3 text-left">Actions</th>
          </tr>
        </thead>

        {/* Table Body */}
        <tbody className="divide-y divide-gray-200">
          {users.map(user => (
            <tr key={user.id}>
              <td className="px-6 py-4">
                <div className="flex items-center">
                  <img
                    src={`https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`}
                    className="h-10 w-10 rounded-full mr-3"
                    alt=""
                  />
                  <span>{user.username}</span>
                </div>
              </td>
              <td className="px-6 py-4">
                {editingId === user.id ? (
                  <select
                    value={tempRoles[user.id]}
                    onChange={(e) => setTempRoles({...tempRoles, [user.id]: e.target.value})}
                    className="border rounded p-1"
                  >
                    <option value="member">Member</option>
                    <option value="moderator">Moderator</option>
                    <option value="admin">Admin</option>
                  </select>
                ) : (
                  <span className="capitalize">{user.roles}</span>
                )}
              </td>
              <td className="px-6 py-4">
                {editingId === user.id ? (
                  <button
                    onClick={() => handleSave(user.id)}
                    className="bg-green-500 text-white px-3 py-1 rounded"
                  >
                    Save
                  </button>
                ) : (
                  <button
                    onClick={() => handleEdit(user.id, user.roles)}
                    className="bg-blue-500 text-white px-3 py-1 rounded"
                  >
                    Edit
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}