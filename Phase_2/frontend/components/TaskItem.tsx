'use client';

import { Task } from '../lib/types';
import { updateTask, deleteTask, toggleComplete } from '../lib/api';
import { PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

interface Props {
  task: Task;
  onEdit: (task: Task) => void;
  onUpdate: () => void;
  onDelete: () => void;
}

export default function TaskItem({ task, onEdit, onUpdate, onDelete }: Props) {
  const handleToggle = async () => {
    await toggleComplete(task.id);
    onUpdate();
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      await deleteTask(task.id);
      onDelete();
    }
  };

  return (
    <div className={`p-5 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border-2 ${
      task.completed 
        ? 'bg-gradient-to-br from-gray-50 to-gray-100 border-gray-200 opacity-70' 
        : 'bg-white border-gray-200 hover:border-primary-300'
    }`}>
      <div className="flex justify-between items-start gap-4">
        <div className="flex-1 min-w-0">
          <h3 className={`font-semibold text-lg mb-1 ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
        </div>
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500 border-gray-300 cursor-pointer mt-1"
        />
      </div>
      <div className="flex gap-2 mt-4 pt-3 border-t border-gray-100">
        <button
          onClick={() => onEdit(task)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-all duration-200"
        >
          <PencilIcon className="w-4 h-4" />
          <span>Edit</span>
        </button>
        <button
          onClick={handleDelete}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-all duration-200"
        >
          <TrashIcon className="w-4 h-4" />
          <span>Delete</span>
        </button>
      </div>
    </div>
  );
}