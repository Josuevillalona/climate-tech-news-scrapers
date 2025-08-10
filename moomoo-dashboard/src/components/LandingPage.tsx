'use client';

import { useState } from 'react';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

interface LandingPageProps {
  onEnterDashboard: () => void;
}

export default function LandingPage({ onEnterDashboard }: LandingPageProps) {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background GIF */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/moomoo-climate-cow.gif"
          alt="MooMoo Climate Background"
          fill
          className="object-cover"
          priority
        />
      </div>

      {/* Button positioned next to the cow */}
      <div className="relative z-10 min-h-screen flex items-center justify-center">
        <div className="absolute bottom-20 right-20">
          <Button
            onClick={onEnterDashboard}
            className="bg-gradient-to-r from-orange-400 to-red-500 hover:from-orange-500 hover:to-red-600 text-white font-bold py-4 px-8 rounded-2xl text-lg shadow-2xl transform transition-all duration-300 hover:scale-105"
          >
            <span className="flex items-center space-x-3">
              <span>Enter Dashboard</span>
              <ArrowRight className="h-5 w-5" />
            </span>
          </Button>
        </div>
      </div>
    </div>
  );
}
