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
          <div className="max-w-5xl mx-auto py-8 sm:px-6 lg:px-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl mb-4 shadow-lg transform hover:scale-105 transition-transform duration-300">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent mb-2">
                My Tasks
              </h1>
              <p className="text-gray-600 text-lg">Stay organized and productive</p>
            </div>
            <TaskTabs />
          </div>
        </div>
      </>
    </ProtectedRoute>
  );
}