import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BIS Sahayak — AI Assistant for Indian Standards",
  description:
    "AI-powered assistant for Indian Standards (IS) and BIS services. Get accurate, source-backed answers about certification, hallmarking, testing labs, and more.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen antialiased transition-colors duration-300" style={{ background: 'var(--background)', color: 'var(--foreground)' }}>{children}</body>
    </html>
  );
}
