import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { AlertProvider } from "@/contexts/AlertContext";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Moo Climate - Investment Intelligence",
  description: "AI-powered climate tech investment discovery platform",
};

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
        <AlertProvider>
          {children}
        </AlertProvider>
      </body>
    </html>
  );
}
