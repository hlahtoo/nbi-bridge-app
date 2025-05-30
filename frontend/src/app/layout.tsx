// Root layout component that sets up global fonts, metadata, and base HTML structure for the Next.js app
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Load Geist Sans font and assign it to a CSS variable
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// Load Geist Mono font and assign it to a CSS variable
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Metadata for the HTML head (used by Next.js)
export const metadata: Metadata = {
  title: "NBI Bridge Map",
  description: "Interactive Map for NBI Bridge Inventory",
};

// Main layout component that wraps all pages
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
