"use client";

import React from "react";
import { ChatMode } from "@/lib/api";

interface QuickActionsProps {
  onSelect: (mode: ChatMode, prompt: string) => void;
}

const ACTIONS = [
  {
    mode: "recommend" as ChatMode,
    icon: "\uD83D\uDD0D",
    label: "Find My Standard",
    prompt: "What BIS standard applies to my product?",
  },
  {
    mode: "certify" as ChatMode,
    icon: "\uD83D\uDCCB",
    label: "Certification Steps",
    prompt: "Explain the BIS certification process step by step.",
  },
  {
    mode: "hallmark" as ChatMode,
    icon: "\uD83D\uDC8D",
    label: "Hallmarking Help",
    prompt: "How do I get BIS hallmarking for gold jewellery?",
  },
  {
    mode: "lab" as ChatMode,
    icon: "\uD83D\uDD2C",
    label: "Find a Lab",
    prompt: "Find the nearest BIS-approved testing laboratory.",
  },
];

export default function QuickActions({ onSelect }: QuickActionsProps) {
  return (
    <div className="grid grid-cols-2 gap-2.5 max-w-lg mx-auto">
      {ACTIONS.map((action) => (
        <button
          key={action.mode}
          onClick={() => onSelect(action.mode, action.prompt)}
          className="flex items-center gap-2.5 p-3.5 rounded-xl border border-gray-200 dark:border-[#3F3F46]
                     bg-gray-50 dark:bg-[#2A2A2A] transition-lift btn-press cursor-pointer
                     hover:bg-gray-100 dark:hover:bg-[#303030]"
        >
          <span className="text-lg">{action.icon}</span>
          <span className="text-sm font-medium text-gray-700 dark:text-[#ECECEC]">{action.label}</span>
        </button>
      ))}
    </div>
  );
}
