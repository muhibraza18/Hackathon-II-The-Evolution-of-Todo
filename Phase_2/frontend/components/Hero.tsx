'use client';

import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const Hero = () => {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();

  const handleGoToTasks = () => {
    router.push('/tasks');
  };

  return (
    <div className="relative bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 py-20 sm:py-24 lg:py-32 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-emerald-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-green-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Icon */}
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-emerald-500 to-green-600 rounded-3xl mb-8 shadow-2xl transform hover:scale-105 transition-transform duration-300">
            <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight mb-6">
            <span className="block text-gray-900">Organize Your Life with</span>
            <span className="block bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
              Taskify
            </span>
          </h1>
          
          <p className="mt-6 max-w-2xl mx-auto text-xl sm:text-2xl text-gray-600 leading-relaxed">
            The modern task management solution that helps you stay organized, focused, and productive. Achieve more with less stress.
          </p>

          <div className="mt-12 flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
            {isAuthenticated ? (
              <button
                onClick={handleGoToTasks}
                className="group inline-flex items-center justify-center px-8 py-4 text-lg font-bold rounded-xl text-white bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-200"
              >
                Go to Tasks
                <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            ) : (
              <>
                <Link
                  href="/signup"
                  className="group inline-flex items-center justify-center px-8 py-4 text-lg font-bold rounded-xl text-white bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-200"
                >
                  Get Started
                  <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </Link>
                <Link
                  href="/login"
                  className="inline-flex items-center justify-center px-8 py-4 text-lg font-bold rounded-xl text-emerald-700 bg-white hover:bg-gray-50 shadow-lg hover:shadow-xl border-2 border-emerald-200 transform hover:-translate-y-1 transition-all duration-200"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>

          {/* Stats or features preview */}
          <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-emerald-100">
              <div className="text-3xl font-bold text-emerald-600 mb-2">Simple</div>
              <p className="text-gray-600">Easy to use interface</p>
            </div>
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-green-100">
              <div className="text-3xl font-bold text-green-600 mb-2">Fast</div>
              <p className="text-gray-600">Lightning quick performance</p>
            </div>
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-teal-100">
              <div className="text-3xl font-bold text-teal-600 mb-2">Secure</div>
              <p className="text-gray-600">Your data is protected</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;