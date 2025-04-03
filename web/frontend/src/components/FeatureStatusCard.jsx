import React from 'react';

export default function FeatureStatusCard({ features }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-bold text-lg mb-3">Active Features</h3>
      <div className="space-y-2">
        {features.map((feature, index) => (
          <div key={index} className="flex items-center">
            <span className={`h-3 w-3 rounded-full mr-2 ${feature.active ? 'bg-green-500' : 'bg-red-500'}`}></span>
            <span>
              {feature.name} - {feature.active ? 'Online' : 'Offline'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}