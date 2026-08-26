"use client";

import React, { useState, useRef, useEffect } from "react";

const LANGUAGES = [
  { code: "auto", label: "Auto Detect" },
  { code: "en", label: "English" },
  { code: "hi", label: "\u0939\u093F\u0928\u094D\u0926\u0940" },
  { code: "bn", label: "\u09AC\u09BE\u0982\u09B2\u09BE" },
  { code: "ta", label: "\u0BA4\u0BAE\u0BBF\u0BB4\u0BCD" },
  { code: "te", label: "\u0C24\u0C46\u0C32\u0C41\u0C17\u0C41" },
  { code: "mr", label: "\u092E\u0930\u093E\u0920\u0940" },
  { code: "gu", label: "\u0A97\u0AC1\u0A9C\u0AB0\u0ABE\u0A9F\u0AC0" },
  { code: "kn", label: "\u0C95\u0CA8\u0CCD\u0CA8\u0CBE" },
  { code: "ml", label: "\u0D2E\u0D32\u0D2F\u0D3E\u0D33\u0D02" },
  { code: "pa", label: "\u0A2A\u0A70\u0A1C\u0A3E\u0A2C\u0A40" },
  { code: "ur", label: "\u0627\u0631\u062F\u0648" },
];

interface LanguageToggleProps {
  language: string;
  onChange: (lang: string) => void;
}

export default function LanguageToggle({ language, onChange }: LanguageToggleProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const selected = LANGUAGES.find((l) => l.code === language) || LANGUAGES[0];

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 text-sm bg-gray-100 dark:bg-[#2A2A2A] border border-[#E5E7EB] dark:border-[#3F3F46] rounded-full px-3 py-1.5
                   text-gray-700 dark:text-[#ECECEC] hover:bg-gray-200 dark:hover:bg-[#3F3F46] transition-colors cursor-pointer btn-press"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-400 dark:text-[#71717A]">
          <circle cx="12" cy="12" r="10" />
          <path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" />
        </svg>
        <span className="text-xs font-medium">{selected.label}</span>
        <svg
          width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
          className={`text-gray-400 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-[#2A2A2A] border border-[#E5E7EB] dark:border-[#3F3F46] rounded-xl shadow-lg
                        py-1.5 z-50 animate-fade-in max-h-80 overflow-y-auto">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => {
                onChange(lang.code);
                setOpen(false);
              }}
              className={`w-full flex items-center justify-between px-3 py-2 text-sm transition-colors text-left ${
                language === lang.code
                  ? "bg-gray-100 dark:bg-[#3F3F46] text-gray-900 dark:text-[#ECECEC] font-medium"
                  : "text-gray-700 dark:text-[#ECECEC] hover:bg-gray-50 dark:hover:bg-[#303030]"
              }`}
            >
              <span>{lang.label}</span>
              {language === lang.code && (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-gray-500 dark:text-[#A1A1AA]">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
