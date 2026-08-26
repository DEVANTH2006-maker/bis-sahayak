"use client";

import React from "react";

interface AboutModalProps {
  open: boolean;
  onClose: () => void;
}

export default function AboutModal({ open, onClose }: AboutModalProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center modal-backdrop" onClick={onClose}>
      <div
        className="bg-white dark:bg-[#2A2A2A] rounded-2xl shadow-2xl w-full max-w-md mx-4 animate-scale-in border border-[#E5E7EB] dark:border-[#3F3F46]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 pt-6 pb-2">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-bis-500 to-bis-600 flex items-center justify-center">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-[#ECECEC]">About BIS Sahayak</h2>
              <p className="text-xs text-gray-400 dark:text-[#71717A]">Version 1.0.0</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-100 dark:hover:bg-[#3F3F46] transition-colors btn-press"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12" strokeLinecap="round" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          <p className="text-sm text-gray-600 dark:text-[#A1A1AA] leading-relaxed mb-4">
            BIS Sahayak is an AI-powered assistant built for the Bureau of Indian Standards (BIS). It helps users:
          </p>

          <ul className="space-y-1.5 mb-4">
            {[
              "Understand Indian Standards (IS)",
              "Find the correct BIS standard",
              "Explain certification procedures",
              "Guide hallmarking requirements",
              "Locate BIS testing laboratories",
              "Answer questions using official BIS documents",
            ].map((feature) => (
              <li key={feature} className="flex items-start gap-2 text-sm text-gray-600 dark:text-[#A1A1AA]">
                <span className="text-gray-400 dark:text-[#71717A] mt-0.5 shrink-0">{"\u2022"}</span>
                {feature}
              </li>
            ))}
          </ul>

          <div className="space-y-2 mb-4">
            <p className="text-xs text-gray-500 dark:text-[#71717A]">
              Powered by Gemini + BIS Knowledge Base
            </p>
            <p className="text-xs text-gray-400 dark:text-[#52525B] leading-relaxed">
              This assistant provides information sourced from official BIS documents. Always verify compliance details at{" "}
              <a href="https://bis.gov.in" target="_blank" rel="noopener noreferrer" className="text-[#3B82F6] hover:underline">
                bis.gov.in
              </a>.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 pb-6 pt-2">
          <button
            onClick={onClose}
            className="w-full py-2.5 rounded-xl bg-gray-100 dark:bg-[#3F3F46] text-gray-700 dark:text-[#ECECEC] text-sm font-medium
                       hover:bg-gray-200 dark:hover:bg-[#52525B] transition-colors btn-press"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
