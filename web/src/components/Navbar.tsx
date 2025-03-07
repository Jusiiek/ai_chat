// Navbar.tsx
import React from "react";

interface NavbarProps {
  children: React.ReactNode;
}

const Navbar: React.FC<NavbarProps> = ({ children }) => {
  return (
    <nav
      className="fixed top-0 left-0 right-0 z-20 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-600 p-4"
    >
      <div className="max-w-screen-xl mx-auto flex justify-between items-center">
        {children}
      </div>
    </nav>
  );
};

export default Navbar;
