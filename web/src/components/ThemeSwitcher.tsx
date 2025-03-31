import React, { useEffect, useState } from 'react';

import { Icon } from '../components';

interface ThemeSwitcherProps {
    className?: string
}

const ThemeSwitcher: React.FC<ThemeSwitcherProps> = ({className}) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (!localStorage.theme) {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
      setIsDarkMode(true);
      return
    }
    if (localStorage.theme === "dark") {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
      setIsDarkMode(true);
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.theme = "light";
      setIsDarkMode(false);
    }
  }, []);

  const toggleTheme = () => {
    if (!localStorage.theme) {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
      setIsDarkMode(true);
      return
    }
    if (localStorage.theme === "dark") {
      document.documentElement.classList.remove("dark");
      localStorage.theme = "light";
      setIsDarkMode(false);
    } else {
      document.documentElement.classList.add("dark");
      localStorage.theme = "dark";
      setIsDarkMode(true);
    }
  };

  return (
    <button
      onClick={toggleTheme}
      className={`px-4 py-2 rounded-md transition-colors duration-200 bg-gray-800 dark:bg-yellow-400 text-white ${className}`}
    >
      {
        isDarkMode ?
            <Icon name={"sun"} />
            :
            <Icon name={"moon"} />
      }
    </button>
  );
};

export default ThemeSwitcher;
