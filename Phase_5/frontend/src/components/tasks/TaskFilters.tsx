'use client';

import { useState } from 'react';
import { TaskFilters as TaskFiltersType } from '../../services/tasks';

interface TaskFiltersProps {
  filters: TaskFiltersType;
  setFilters: (filters: TaskFiltersType) => void;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({ filters, setFilters }) => {
  const [searchQuery, setSearchQuery] = useState(filters.search || '');
  const [showFilters, setShowFilters] = useState(false);

  const handleSearchChange = (value: string) => {
    setSearchQuery(value);
    setFilters({ ...filters, search: value || undefined });
  };

  const toggleCompleted = () => {
    setFilters({ ...filters, completed: filters.completed === undefined ? true : filters.completed ? undefined : false });
  };

  const setPriority = (priority: 'low' | 'medium' | 'high' | 'urgent' | undefined) => {
    setFilters({ ...filters, priority });
  };

  const setSortBy = (sortBy: 'created_at' | 'updated_at' | 'due_date' | 'priority') => {
    setFilters({ ...filters, sort_by: sortBy, sort_order: filters.sort_order || 'desc' });
  };

  const toggleSortOrder = () => {
    setFilters({ ...filters, sort_order: filters.sort_order === 'asc' ? 'desc' : 'asc' });
  };

  const hasActiveFilters = filters.completed !== undefined || filters.priority || filters.sort_by;

  const clearFilters = () => {
    setSearchQuery('');
    setFilters({});
  };

  return (
    <div className="task-filters">
      <div className="filters-main">
        {/* Search */}
        <div className="search-box">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
            placeholder="Search tasks..."
            aria-label="Search tasks"
          />
          {searchQuery && (
            <button
              onClick={() => handleSearchChange('')}
              className="clear-search"
              aria-label="Clear search"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          )}
        </div>

        {/* Filter Toggle */}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`filter-toggle ${showFilters ? 'active' : ''}`}
          aria-label={showFilters ? 'Hide filters' : 'Show filters'}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
          </svg>
          <span>Filters</span>
          {hasActiveFilters && <span className="filter-badge">{
            [filters.completed !== undefined, filters.priority, filters.sort_by].filter(Boolean).length
          }</span>}
        </button>
      </div>

      {/* Expanded Filters */}
      {showFilters && (
        <div className="filters-expanded">
          {/* Status Filter */}
          <div className="filter-group">
            <label className="filter-label">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 11 12 14 22 4"></polyline>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
              </svg>
              Status
            </label>
            <div className="filter-buttons">
              <button
                onClick={() => setFilters({ ...filters, completed: filters.completed === false ? undefined : false })}
                className={`filter-chip ${filters.completed === false ? 'active' : ''}`}
              >
                <span className="chip-dot pending"></span>
                Pending
              </button>
              <button
                onClick={() => setFilters({ ...filters, completed: filters.completed === true ? undefined : true })}
                className={`filter-chip ${filters.completed === true ? 'active' : ''}`}
              >
                <span className="chip-dot completed"></span>
                Completed
              </button>
            </div>
          </div>

          {/* Priority Filter */}
          <div className="filter-group">
            <label className="filter-label">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              Priority
            </label>
            <div className="filter-buttons">
              {(['low', 'medium', 'high', 'urgent'] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => setPriority(filters.priority === p ? undefined : p)}
                  className={`filter-chip priority-chip priority-${p} ${filters.priority === p ? 'active' : ''}`}
                >
                  <span className={`chip-dot priority-${p}`}></span>
                  {p.charAt(0).toUpperCase() + p.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Sort */}
          <div className="filter-group">
            <label className="filter-label">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="8" y1="6" x2="21" y2="6"></line>
                <line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line>
                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                <line x1="3" y1="18" x2="3.01" y2="18"></line>
              </svg>
              Sort By
            </label>
            <div className="filter-buttons">
              <button
                onClick={() => setSortBy('created_at')}
                className={`filter-chip ${filters.sort_by === 'created_at' ? 'active' : ''}`}
              >
                Created Date
              </button>
              <button
                onClick={() => setSortBy('due_date')}
                className={`filter-chip ${filters.sort_by === 'due_date' ? 'active' : ''}`}
              >
                Due Date
              </button>
              <button
                onClick={() => setSortBy('priority')}
                className={`filter-chip ${filters.sort_by === 'priority' ? 'active' : ''}`}
              >
                Priority
              </button>
              <button
                onClick={toggleSortOrder}
                className="sort-order-btn"
                aria-label={`Sort ${filters.sort_order === 'asc' ? 'descending' : 'ascending'}`}
                title={`Sort ${filters.sort_order === 'asc' ? 'descending' : 'ascending'}`}
              >
                {filters.sort_order === 'asc' ? (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="18 15 12 9 6 15"></polyline>
                    </svg>
                    <span>Asc</span>
                  </>
                ) : (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                    <span>Desc</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Clear All Filters */}
          {hasActiveFilters && (
            <div className="filter-group clear-group">
              <button onClick={clearFilters} className="clear-filters">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  <line x1="10" y1="11" x2="10" y2="17"></line>
                  <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
                Clear All Filters
              </button>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .task-filters {
          margin-bottom: 24px;
        }

        .filters-main {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        /* Search Box */
        .search-box {
          flex: 1;
          min-width: 250px;
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 12px 16px;
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          transition: all 0.2s ease;
          position: relative;
        }

        .search-box:focus-within {
          border-color: #0f172a;
          box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.08);
        }

        .search-box svg {
          color: #94a3b8;
          flex-shrink: 0;
        }

        .search-box input {
          flex: 1;
          border: none;
          outline: none;
          font-size: 0.9rem;
          background: transparent;
          color: #1e293b;
          font-family: inherit;
        }

        .search-box input::placeholder {
          color: #94a3b8;
        }

        .clear-search {
          background: transparent;
          border: none;
          color: #94a3b8;
          padding: 4px;
          cursor: pointer;
          border-radius: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
        }

        .clear-search:hover {
          background-color: #f1f5f9;
          color: #64748b;
        }

        /* Filter Toggle Button */
        .filter-toggle {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 12px 18px;
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          font-size: 0.9rem;
          font-weight: 500;
          color: #475569;
          cursor: pointer;
          transition: all 0.2s ease;
          position: relative;
          white-space: nowrap;
        }

        .filter-toggle:hover {
          background-color: #f8fafc;
          border-color: #cbd5e1;
        }

        .filter-toggle.active {
          background-color: #0f172a;
          border-color: #0f172a;
          color: white;
        }

        .filter-toggle span {
          display: none;
        }

        @media (min-width: 640px) {
          .filter-toggle span {
            display: inline;
          }
        }

        .filter-badge {
          min-width: 20px;
          height: 20px;
          background-color: #ef4444;
          color: white;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.7rem;
          font-weight: 600;
          padding: 0 6px;
        }

        .filter-toggle.active .filter-badge {
          background-color: white;
          color: #0f172a;
        }

        /* Expanded Filters */
        .filters-expanded {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 20px;
          padding: 20px;
          margin-top: 12px;
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .filter-group {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .filter-label {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 0.75rem;
          font-weight: 600;
          color: #64748b;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .filter-label svg {
          color: #94a3b8;
        }

        .filter-buttons {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        /* Filter Chips */
        .filter-chip {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 8px 14px;
          background-color: #f8fafc;
          border: 1px solid #e2e8f0;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 500;
          color: #475569;
          cursor: pointer;
          transition: all 0.2s ease;
          white-space: nowrap;
        }

        .filter-chip:hover {
          background-color: #f1f5f9;
          border-color: #cbd5e1;
          transform: translateY(-1px);
        }

        .filter-chip.active {
          background-color: #0f172a;
          color: white;
          border-color: #0f172a;
          font-weight: 600;
        }

        /* Priority Chips */
        .priority-chip.active.priority-low {
          background-color: #10b981;
          border-color: #10b981;
        }

        .priority-chip.active.priority-medium {
          background-color: #f59e0b;
          border-color: #f59e0b;
        }

        .priority-chip.active.priority-high {
          background-color: #f97316;
          border-color: #f97316;
        }

        .priority-chip.active.priority-urgent {
          background-color: #ef4444;
          border-color: #ef4444;
        }

        /* Chip Dots */
        .chip-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          flex-shrink: 0;
        }

        .chip-dot.pending {
          background-color: #f59e0b;
        }

        .chip-dot.completed {
          background-color: #10b981;
        }

        .chip-dot.priority-low {
          background-color: #10b981;
        }

        .chip-dot.priority-medium {
          background-color: #f59e0b;
        }

        .chip-dot.priority-high {
          background-color: #f97316;
        }

        .chip-dot.priority-urgent {
          background-color: #ef4444;
        }

        .filter-chip.active .chip-dot {
          background-color: white;
        }

        /* Sort Order Button */
        .sort-order-btn {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 8px 12px;
          background: transparent;
          border: 1px solid #e2e8f0;
          border-radius: 20px;
          cursor: pointer;
          color: #64748b;
          font-size: 0.85rem;
          font-weight: 500;
          transition: all 0.2s ease;
        }

        .sort-order-btn:hover {
          background-color: #f1f5f9;
          border-color: #cbd5e1;
          transform: translateY(-1px);
        }

        .sort-order-btn span {
          font-size: 0.8rem;
        }

        /* Clear Filters */
        .clear-group {
          grid-column: 1 / -1;
          align-items: flex-start;
        }

        .clear-filters {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 16px;
          background: transparent;
          border: 1px solid #e2e8f0;
          border-radius: 10px;
          font-size: 0.85rem;
          font-weight: 500;
          color: #64748b;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .clear-filters:hover {
          background-color: #fef2f2;
          color: #dc2626;
          border-color: #fecaca;
          transform: translateY(-1px);
        }

        /* Responsive */
        @media (max-width: 768px) {
          .filters-expanded {
            grid-template-columns: 1fr;
          }

          .search-box {
            min-width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default TaskFilters;