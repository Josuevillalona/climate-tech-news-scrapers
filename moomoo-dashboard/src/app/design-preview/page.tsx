'use client';

import DesignSystem from "@/components/ui/design-system";

export default function DesignPreviewPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Design System Preview</h1>
            <p className="text-lg text-gray-600">
              Testing the new yellow active state (#F7D774) with dark gray text (Gray 900) for sidebar navigation
            </p>
          </div>
          
          <DesignSystem />
        </div>
      </div>
    </div>
  );
}
