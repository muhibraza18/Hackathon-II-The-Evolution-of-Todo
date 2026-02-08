'use client';

interface PriorityBadgeProps {
  priority: 'low' | 'medium' | 'high' | 'urgent';
}

const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority }) => {
  const priorityConfig = {
    low: {
      label: 'Low',
      color: '#10b981',
      bgColor: '#d1fae5',
    },
    medium: {
      label: 'Medium',
      color: '#f59e0b',
      bgColor: '#fef3c7',
    },
    high: {
      label: 'High',
      color: '#f97316',
      bgColor: '#ffedd5',
    },
    urgent: {
      label: 'Urgent',
      color: '#ef4444',
      bgColor: '#fee2e2',
    },
  };

  const config = priorityConfig[priority];

  return (
    <>
      <div
        className="priority-badge"
        style={{
          color: config.color,
          backgroundColor: config.bgColor,
        }}
      >
        {config.label}
      </div>
      <style jsx>{`
        .priority-badge {
          display: inline-flex;
          align-items: center;
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
      `}</style>
    </>
  );
};

export default PriorityBadge;
