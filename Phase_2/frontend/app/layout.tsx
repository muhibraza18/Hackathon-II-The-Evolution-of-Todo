import type { Metadata } from "next";
import ClientWrapper from './ClientWrapper';
import "./globals.css";

export const metadata: Metadata = {
  title: "Todo App - Foundation Setup",
  description: "Todo Full-Stack Web Application - Foundation Phase",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`antialiased`}>
        <ClientWrapper>
          {children}
        </ClientWrapper>
      </body>
    </html>
  );
}
