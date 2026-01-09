'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import Hero from '../components/Hero';
import Features from '../components/Features';
import Navbar from '@/components/Navbar';

export default function Home() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();

  const handleGoToTasks = () => {
    router.push('/tasks');
  };

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 pt-16">
        <Hero />
        <Features />
      </main>
    </>
  );
}