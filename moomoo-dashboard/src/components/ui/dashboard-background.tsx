import React from 'react';

interface DashboardBackgroundProps {
  children: React.ReactNode;
}

export default function DashboardBackground({ children }: DashboardBackgroundProps) {
  return (
    <div className="min-h-screen bg-[#AEE1F6]/20 relative overflow-hidden flex">
      {/* Animated Background Elements - Positioned to avoid sidebar and behind content */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
        {/* Large Pulsing Orbs - Positioned for main content area */}
        <div className="absolute top-16 right-32 w-40 h-40 bg-[#F7D774]/40 rounded-full blur-3xl animate-gentle-pulse"></div>
        <div className="absolute top-1/3 right-16 w-48 h-48 bg-[#2E5E4E]/35 rounded-full blur-3xl animate-gentle-pulse delay-1000"></div>
        <div className="absolute bottom-32 right-1/4 w-44 h-44 bg-[#AEE1F6]/40 rounded-full blur-3xl animate-gentle-pulse delay-2000"></div>
        <div className="absolute top-1/2 right-1/2 w-56 h-56 bg-gradient-to-r from-[#F7D774]/30 to-[#2E5E4E]/25 rounded-full blur-3xl animate-gentle-pulse delay-500"></div>
        
        {/* Top Area Enhanced Orbs */}
        <div className="absolute top-8 right-1/4 w-36 h-36 bg-[#AEE1F6]/35 rounded-full blur-3xl animate-gentle-pulse delay-800"></div>
        <div className="absolute top-12 right-3/4 w-42 h-42 bg-[#2E5E4E]/30 rounded-full blur-3xl animate-gentle-pulse delay-1200"></div>
        <div className="absolute top-20 right-1/2 w-38 h-38 bg-[#F7D774]/35 rounded-full blur-3xl animate-gentle-pulse delay-1800"></div>
        <div className="absolute top-6 right-1/3 w-44 h-44 bg-gradient-to-br from-[#AEE1F6]/30 to-[#F7D774]/25 rounded-full blur-3xl animate-gentle-pulse delay-600"></div>
        <div className="absolute top-14 right-2/3 w-40 h-40 bg-[#2E5E4E]/28 rounded-full blur-3xl animate-gentle-pulse delay-2200"></div>
        
        {/* Mid-Section Large Orbs */}
        <div className="absolute top-1/3 right-1/5 w-50 h-50 bg-[#F7D774]/32 rounded-full blur-3xl animate-gentle-pulse delay-900"></div>
        <div className="absolute top-2/5 right-4/5 w-46 h-46 bg-[#AEE1F6]/38 rounded-full blur-3xl animate-gentle-pulse delay-1400"></div>
        <div className="absolute top-1/2 right-1/4 w-52 h-52 bg-[#2E5E4E]/30 rounded-full blur-3xl animate-gentle-pulse delay-1600"></div>
        <div className="absolute top-3/5 right-3/5 w-48 h-48 bg-gradient-to-tl from-[#F7D774]/28 to-[#AEE1F6]/32 rounded-full blur-3xl animate-gentle-pulse delay-2400"></div>
        
        {/* Bottom Area Large Orbs */}
        <div className="absolute bottom-1/3 right-1/5 w-44 h-44 bg-[#AEE1F6]/36 rounded-full blur-3xl animate-gentle-pulse delay-1100"></div>
        <div className="absolute bottom-1/4 right-3/4 w-50 h-50 bg-[#2E5E4E]/32 rounded-full blur-3xl animate-gentle-pulse delay-1900"></div>
        <div className="absolute bottom-1/5 right-1/2 w-42 h-42 bg-[#F7D774]/38 rounded-full blur-3xl animate-gentle-pulse delay-2100"></div>
        <div className="absolute bottom-16 right-1/3 w-46 h-46 bg-gradient-to-tr from-[#2E5E4E]/30 to-[#AEE1F6]/34 rounded-full blur-3xl animate-gentle-pulse delay-2600"></div>
        
        {/* Additional Scattered Large Orbs */}
        <div className="absolute top-1/4 right-1/6 w-38 h-38 bg-[#F7D774]/34 rounded-full blur-3xl animate-gentle-pulse delay-700"></div>
        <div className="absolute top-3/4 right-2/5 w-40 h-40 bg-[#AEE1F6]/40 rounded-full blur-3xl animate-gentle-pulse delay-1300"></div>
        <div className="absolute bottom-2/5 right-1/6 w-44 h-44 bg-[#2E5E4E]/36 rounded-full blur-3xl animate-gentle-pulse delay-1700"></div>
        <div className="absolute top-1/5 right-4/5 w-36 h-36 bg-gradient-to-bl from-[#F7D774]/32 to-[#2E5E4E]/28 rounded-full blur-3xl animate-gentle-pulse delay-2300"></div>
        
        {/* Additional Medium Orbs */}
        <div className="absolute top-24 right-1/3 w-32 h-32 bg-[#F7D774]/30 rounded-full blur-2xl animate-gentle-pulse delay-1500"></div>
        <div className="absolute top-10 right-20 w-28 h-28 bg-[#AEE1F6]/32 rounded-full blur-2xl animate-gentle-pulse delay-900"></div>
        <div className="absolute top-18 right-1/5 w-30 h-30 bg-[#2E5E4E]/35 rounded-full blur-2xl animate-gentle-pulse delay-1700"></div>
        <div className="absolute bottom-1/4 right-12 w-36 h-36 bg-[#2E5E4E]/30 rounded-full blur-2xl animate-gentle-pulse delay-3000"></div>
        <div className="absolute top-2/3 right-2/3 w-28 h-28 bg-[#AEE1F6]/35 rounded-full blur-2xl animate-gentle-pulse delay-2500"></div>
        
        {/* Mid-Section Medium Orbs */}
        <div className="absolute top-1/3 right-2/3 w-34 h-34 bg-[#F7D774]/32 rounded-full blur-2xl animate-gentle-pulse delay-800"></div>
        <div className="absolute top-2/5 right-1/6 w-30 h-30 bg-[#AEE1F6]/36 rounded-full blur-2xl animate-gentle-pulse delay-1200"></div>
        <div className="absolute top-1/2 right-5/6 w-32 h-32 bg-[#2E5E4E]/34 rounded-full blur-2xl animate-gentle-pulse delay-1600"></div>
        <div className="absolute top-3/5 right-1/4 w-28 h-28 bg-[#F7D774]/38 rounded-full blur-2xl animate-gentle-pulse delay-2000"></div>
        <div className="absolute top-7/12 right-3/4 w-26 h-26 bg-[#AEE1F6]/40 rounded-full blur-2xl animate-gentle-pulse delay-2400"></div>
        
        {/* Bottom Section Medium Orbs */}
        <div className="absolute bottom-1/3 right-3/5 w-30 h-30 bg-[#2E5E4E]/36 rounded-full blur-2xl animate-gentle-pulse delay-1000"></div>
        <div className="absolute bottom-1/5 right-1/6 w-34 h-34 bg-[#F7D774]/34 rounded-full blur-2xl animate-gentle-pulse delay-1400"></div>
        <div className="absolute bottom-2/5 right-4/5 w-28 h-28 bg-[#AEE1F6]/38 rounded-full blur-2xl animate-gentle-pulse delay-1800"></div>
        <div className="absolute bottom-1/6 right-2/3 w-32 h-32 bg-[#2E5E4E]/32 rounded-full blur-2xl animate-gentle-pulse delay-2200"></div>
        <div className="absolute bottom-1/4 right-1/2 w-26 h-26 bg-[#F7D774]/40 rounded-full blur-2xl animate-gentle-pulse delay-2600"></div>
        
        {/* Additional Scattered Medium Orbs */}
        <div className="absolute top-1/6 right-2/5 w-24 h-24 bg-[#AEE1F6]/42 rounded-full blur-2xl animate-gentle-pulse delay-600"></div>
        <div className="absolute top-5/6 right-1/5 w-28 h-28 bg-[#2E5E4E]/38 rounded-full blur-2xl animate-gentle-pulse delay-1100"></div>
        <div className="absolute bottom-3/5 right-2/3 w-30 h-30 bg-[#F7D774]/36 rounded-full blur-2xl animate-gentle-pulse delay-1500"></div>
        <div className="absolute top-1/8 right-5/6 w-26 h-26 bg-[#AEE1F6]/44 rounded-full blur-2xl animate-gentle-pulse delay-1900"></div>
        <div className="absolute bottom-1/8 right-1/4 w-24 h-24 bg-[#2E5E4E]/40 rounded-full blur-2xl animate-gentle-pulse delay-2300"></div>
        
        {/* Subtle Pattern Overlay - Only on main content area */}
        <div className="absolute top-0 right-0 bottom-0 left-64 md:left-64 opacity-10">
          <div className="w-full h-full" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%232E5E4E' fill-opacity='0.4'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            backgroundSize: '60px 60px'
          }}></div>
        </div>
        
        {/* Floating Elements - Positioned for main content */}
        <div className="absolute top-20 right-1/4 w-4 h-4 bg-[#F7D774]/40 rounded-full animate-float delay-300"></div>
        <div className="absolute bottom-1/3 right-20 w-3 h-3 bg-[#2E5E4E]/50 rounded-full animate-float delay-700"></div>
        <div className="absolute top-1/2 right-1/3 w-5 h-5 bg-[#AEE1F6]/40 rounded-full animate-float delay-1100"></div>
        <div className="absolute top-1/4 right-16 w-3 h-3 bg-[#F7D774]/50 rounded-full animate-float delay-1400"></div>
        <div className="absolute bottom-1/2 right-2/3 w-4 h-4 bg-[#2E5E4E]/40 rounded-full animate-float delay-1800"></div>
        
        {/* Top Area Small Floating Elements */}
        <div className="absolute top-8 right-1/5 w-3 h-3 bg-[#AEE1F6]/45 rounded-full animate-float delay-200"></div>
        <div className="absolute top-12 right-1/2 w-2 h-2 bg-[#F7D774]/50 rounded-full animate-float delay-500"></div>
        <div className="absolute top-6 right-3/4 w-4 h-4 bg-[#2E5E4E]/45 rounded-full animate-float delay-800"></div>
        <div className="absolute top-18 right-1/3 w-3 h-3 bg-[#AEE1F6]/40 rounded-full animate-float delay-1000"></div>
        <div className="absolute top-14 right-2/3 w-2 h-2 bg-[#F7D774]/55 rounded-full animate-float delay-1300"></div>
        <div className="absolute top-10 right-4/5 w-3 h-3 bg-[#2E5E4E]/50 rounded-full animate-float delay-1600"></div>
        
        {/* Mid-Section Floating Elements */}
        <div className="absolute top-1/3 right-1/8 w-4 h-4 bg-[#F7D774]/45 rounded-full animate-float delay-400"></div>
        <div className="absolute top-2/5 right-3/8 w-3 h-3 bg-[#AEE1F6]/50 rounded-full animate-float delay-600"></div>
        <div className="absolute top-1/2 right-5/8 w-2 h-2 bg-[#2E5E4E]/55 rounded-full animate-float delay-900"></div>
        <div className="absolute top-3/5 right-7/8 w-5 h-5 bg-[#F7D774]/40 rounded-full animate-float delay-1200"></div>
        <div className="absolute top-7/12 right-1/6 w-3 h-3 bg-[#AEE1F6]/48 rounded-full animate-float delay-1500"></div>
        <div className="absolute top-5/8 right-1/2 w-4 h-4 bg-[#2E5E4E]/42 rounded-full animate-float delay-1700"></div>
        
        {/* Bottom Section Floating Elements */}
        <div className="absolute bottom-1/4 right-1/8 w-3 h-3 bg-[#AEE1F6]/52 rounded-full animate-float delay-250"></div>
        <div className="absolute bottom-1/5 right-3/8 w-4 h-4 bg-[#F7D774]/48 rounded-full animate-float delay-550"></div>
        <div className="absolute bottom-1/3 right-5/8 w-2 h-2 bg-[#2E5E4E]/58 rounded-full animate-float delay-850"></div>
        <div className="absolute bottom-2/5 right-7/8 w-3 h-3 bg-[#AEE1F6]/45 rounded-full animate-float delay-1150"></div>
        <div className="absolute bottom-1/6 right-1/4 w-5 h-5 bg-[#F7D774]/42 rounded-full animate-float delay-1450"></div>
        <div className="absolute bottom-1/8 right-3/4 w-3 h-3 bg-[#2E5E4E]/48 rounded-full animate-float delay-1750"></div>
        
        {/* Additional Scattered Small Elements */}
        <div className="absolute top-1/8 right-1/3 w-2 h-2 bg-[#F7D774]/60 rounded-full animate-float delay-100"></div>
        <div className="absolute top-7/8 right-2/3 w-3 h-3 bg-[#AEE1F6]/55 rounded-full animate-float delay-350"></div>
        <div className="absolute bottom-7/8 right-1/6 w-4 h-4 bg-[#2E5E4E]/45 rounded-full animate-float delay-650"></div>
        <div className="absolute top-3/8 right-5/6 w-2 h-2 bg-[#F7D774]/58 rounded-full animate-float delay-950"></div>
        <div className="absolute bottom-3/8 right-1/12 w-3 h-3 bg-[#AEE1F6]/50 rounded-full animate-float delay-1250"></div>
        <div className="absolute top-5/8 right-11/12 w-4 h-4 bg-[#2E5E4E]/40 rounded-full animate-float delay-1550"></div>
        
        {/* Drifting Elements - Main content area focused */}
        <div className="absolute top-1/4 right-1/2 w-6 h-6 bg-[#F7D774]/30 rounded-full animate-drift"></div>
        <div className="absolute bottom-1/4 right-1/4 w-4 h-4 bg-[#2E5E4E]/40 rounded-full animate-drift delay-1500"></div>
        <div className="absolute top-1/3 right-3/4 w-5 h-5 bg-[#AEE1F6]/35 rounded-full animate-drift delay-2200"></div>
        <div className="absolute bottom-1/3 right-1/3 w-3 h-3 bg-[#F7D774]/40 rounded-full animate-drift delay-3000"></div>
        
        {/* Additional Drifting Elements Throughout */}
        <div className="absolute top-1/6 right-1/4 w-7 h-7 bg-[#AEE1F6]/32 rounded-full animate-drift delay-500"></div>
        <div className="absolute top-1/5 right-3/5 w-5 h-5 bg-[#2E5E4E]/38 rounded-full animate-drift delay-800"></div>
        <div className="absolute top-2/5 right-1/6 w-6 h-6 bg-[#F7D774]/35 rounded-full animate-drift delay-1200"></div>
        <div className="absolute top-3/5 right-5/6 w-4 h-4 bg-[#AEE1F6]/42 rounded-full animate-drift delay-1800"></div>
        <div className="absolute bottom-2/5 right-2/5 w-8 h-8 bg-[#2E5E4E]/30 rounded-full animate-drift delay-2400"></div>
        <div className="absolute bottom-1/5 right-4/5 w-5 h-5 bg-[#F7D774]/38 rounded-full animate-drift delay-2800"></div>
        <div className="absolute bottom-1/6 right-1/6 w-6 h-6 bg-[#AEE1F6]/36 rounded-full animate-drift delay-3200"></div>
        
        {/* Micro Drifting Elements for Extra Detail */}
        <div className="absolute top-1/8 right-2/3 w-3 h-3 bg-[#F7D774]/45 rounded-full animate-drift delay-400"></div>
        <div className="absolute top-3/8 right-1/8 w-4 h-4 bg-[#AEE1F6]/40 rounded-full animate-drift delay-1000"></div>
        <div className="absolute top-5/8 right-7/8 w-3 h-3 bg-[#2E5E4E]/48 rounded-full animate-drift delay-1600"></div>
        <div className="absolute top-7/8 right-3/8 w-5 h-5 bg-[#F7D774]/42 rounded-full animate-drift delay-2000"></div>
        <div className="absolute bottom-7/8 right-5/8 w-3 h-3 bg-[#AEE1F6]/44 rounded-full animate-drift delay-2600"></div>
        <div className="absolute bottom-5/8 right-1/8 w-4 h-4 bg-[#2E5E4E]/36 rounded-full animate-drift delay-3400"></div>
        <div className="absolute bottom-3/8 right-7/8 w-6 h-6 bg-[#F7D774]/33 rounded-full animate-drift delay-3800"></div>
      </div>
      
      {/* Content wrapper with higher z-index to appear above background */}
      <div className="relative z-10 w-full">
        {children}
      </div>
    </div>
  );
}
