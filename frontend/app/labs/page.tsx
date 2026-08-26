"use client";

import LabSearch from "@/components/LabSearch";
import Link from "next/link";

export default function LabsPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-[#212121] transition-colors duration-300">
      <header className="bg-white dark:bg-[#171717] border-b border-[#E5E7EB] dark:border-[#3F3F46] px-4 py-3 transition-colors duration-300">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="text-gray-500 dark:text-[#A1A1AA] hover:text-gray-700 dark:hover:text-[#ECECEC] transition-colors">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 12H5M12 19l-7-7 7-7" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
            <div>
              <h1 className="text-base font-semibold text-gray-900 dark:text-[#ECECEC]">BIS-Recognized Testing Labs</h1>
              <p className="text-xs text-gray-400 dark:text-[#71717A]">Search by category or city</p>
            </div>
          </div>
        </div>
      </header>
      <main className="px-4 py-6">
        <LabSearch />
      </main>
    </div>
  );
}
