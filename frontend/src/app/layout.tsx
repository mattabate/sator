import React from 'react';
import './globals.css';

export const metadata = {
  title: "Puslr",
  description: '',
  thumbnail: '/logo.png', // Path to the logo image
  favicon: '/favicon.ico', // Path to the favicon image
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="title" content={metadata.title} />
        <meta name="description" content={metadata.description} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={metadata.title} />
        <meta name="twitter:description" content={metadata.description} />
        <meta name="twitter:image" content={metadata.thumbnail} />
        <meta property="og:title" content={metadata.title} />
        <meta property="og:description" content={metadata.description} />
        <meta property="og:image" content={metadata.thumbnail} />
        <meta property="og:image:alt" content="Logo" />
        <link rel="icon" href={metadata.favicon} />
      </head>
      <body className="flex flex-col bg-white min-content">
        <div className="flex-col bg-white min-content">
          <div className="flex-grow">{children}</div>
        </div>
      </body>
    </html>
  );
}
