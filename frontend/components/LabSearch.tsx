"use client";

import React, { useState, useEffect } from "react";
import { searchLabs, Lab } from "@/lib/api";

const CATEGORIES = [
  "All",
  "Electrical",
  "Electronic",
  "Food",
  "Textiles",
  "Toys",
  "Steel",
  "Cement",
  "Plastics",
  "Chemicals",
  "Metals",
  "Leather",
];

export default function LabSearch() {
  const [category, setCategory] = useState("");
  const [city, setCity] = useState("");
  const [labs, setLabs] = useState<Lab[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);

  const doSearch = async () => {
    setLoading(true);
    try {
      const res = await searchLabs(
        category.toLowerCase() === "all" ? "" : category.toLowerCase(),
        city
      );
      setLabs(res.labs);
      setTotal(res.total);
    } catch {
      setLabs([]);
      setTotal(0);
    }
    setLoading(false);
  };

  useEffect(() => {
    doSearch();
  }, []);

  return (
    <div className="max-w-4xl mx-auto">
      {/* Search filters */}
      <div className="bg-white dark:bg-[#2A2A2A] rounded-xl border border-[#E5E7EB] dark:border-[#3F3F46] p-4 mb-6 transition-colors duration-300">
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-medium text-gray-500 dark:text-[#A1A1AA] mb-1">City</label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="e.g. Mumbai, Delhi, Chennai..."
              className="w-full border border-[#E5E7EB] dark:border-[#3F3F46] rounded-lg px-3 py-2 text-sm bg-gray-50 dark:bg-[#303030]
                         text-gray-700 dark:text-[#ECECEC] placeholder-gray-400 dark:placeholder-[#71717A]
                         focus:outline-none focus:ring-1 focus:ring-gray-300 dark:focus:ring-[#52525B] transition-all"
            />
          </div>
          <button
            onClick={doSearch}
            className="px-5 py-2 bg-gray-900 dark:bg-[#ECECEC] text-white dark:text-[#171717] text-sm font-medium rounded-lg
                       hover:bg-gray-800 dark:hover:bg-[#D4D4D8] transition-colors btn-press"
          >
            Search
          </button>
        </div>
        <div className="flex flex-wrap gap-1.5 mt-3">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => {
                setCategory(cat === "All" ? "" : cat);
                setLoading(true);
                searchLabs(
                  cat === "All" ? "" : cat.toLowerCase(),
                  city
                ).then((res) => {
                  setLabs(res.labs);
                  setTotal(res.total);
                  setLoading(false);
                });
              }}
              className={`px-2.5 py-1 rounded-full text-xs font-medium transition-colors btn-press ${
                (category === "" && cat === "All") || category === cat
                  ? "bg-gray-900 dark:bg-[#ECECEC] text-white dark:text-[#171717]"
                  : "bg-gray-100 dark:bg-[#303030] text-gray-600 dark:text-[#A1A1AA] hover:bg-gray-200 dark:hover:bg-[#3F3F46]"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      <div className="text-sm text-gray-500 dark:text-[#A1A1AA] mb-3">
        {loading ? "Searching..." : `${total} lab${total !== 1 ? "s" : ""} found`}
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        {labs.map((lab, i) => (
          <div
            key={i}
            className="bg-white dark:bg-[#2A2A2A] rounded-xl border border-[#E5E7EB] dark:border-[#3F3F46] p-4 transition-all duration-200 hover:shadow-sm"
          >
            <div className="flex items-start justify-between gap-2 mb-2">
              <h3 className="font-semibold text-gray-800 dark:text-[#ECECEC] text-sm leading-tight">{lab.name}</h3>
              <span className="shrink-0 text-[10px] bg-gray-100 dark:bg-[#3F3F46] text-gray-600 dark:text-[#A1A1AA] px-2 py-0.5 rounded-full font-medium">
                {lab.accreditation}
              </span>
            </div>
            <p className="text-xs text-gray-500 dark:text-[#71717A] mb-2">
              {lab.address}, {lab.city}, {lab.state}
            </p>
            {lab.phone && (
              <p className="text-xs text-gray-500 dark:text-[#71717A] mb-2">{lab.phone}</p>
            )}
            <div className="flex flex-wrap gap-1.5">
              {lab.categories.map((cat) => (
                <span
                  key={cat}
                  className="px-2 py-0.5 bg-gray-100 dark:bg-[#303030] text-gray-600 dark:text-[#A1A1AA] text-[10px] rounded-full"
                >
                  {cat}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {labs.length === 0 && !loading && (
        <div className="text-center py-12 text-gray-400 dark:text-[#71717A]">
          <p className="text-lg mb-2">No labs found</p>
          <p className="text-sm">Try a different city or category filter</p>
        </div>
      )}
    </div>
  );
}
