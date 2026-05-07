import "./globals.css";
import type { ReactNode } from "react";

export const metadata = { title: "Prediction Market Engine", description: "Institutional trading desk for Polymarket automation" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
