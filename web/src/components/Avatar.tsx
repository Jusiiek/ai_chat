import React from "react";

interface AvatarProps {
  onClick?: () => void;
  image?: string
}



const Avatar: React.FC<AvatarProps> = ({ image, onClick }) => {
    return (
        <div className="flex -space-x-1 overflow-hidden">
            {
                image ?
                    <img
                        className="inline-block size-10 rounded-full"
                        src="https://images.unsplash.com/photo-1491528323818-fdd1faba62cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                        alt=""
                    />
                    :
                    <div
                        className="flex size-10 rounded-full bg-sky-500 dark:bg-sky-700  items-center justify-center text-white"
                    >
                        JZ
                    </div>
            }
        </div>
    )
}

export default Avatar;
