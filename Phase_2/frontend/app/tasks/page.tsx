'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import TaskTabs from '@/components/TaskTabs';
import Navbar from '@/components/Navbar';

export default function TasksPage() {
  const router = useRouter();

  return (
    <ProtectedRoute>
      <>
        <Navbar />
        <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 pt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            {/* My Tasks Header */}
            <div className="text-center mb-6 sm:mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl mb-4 shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent mb-2">
                My Tasks
              </h1>
              <p className="text-sm sm:text-base text-gray-600">Stay organized and productive</p>
            </div>
            
            <TaskTabs />
          </div>
        </div>
      </>
    </ProtectedRoute>
  );
}