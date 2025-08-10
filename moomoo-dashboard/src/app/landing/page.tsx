'use client';

import { useRouter } from 'next/navigation';
import LandingPage from '@/components/LandingPage';

export default function Landing() {
  const router = useRouter();

  const handleEnterDashboard = () => {
    router.push('/');
  };

  return <LandingPage onEnterDashboard={handleEnterDashboard} />;
}
