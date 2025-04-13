import React from "react";
import { ActiveUser } from "../instances/user";

interface AvatarProps {
    onClick?: () => void;
}



const Avatar: React.FC<AvatarProps> = ({ onClick }) => {
    const userData = ActiveUser.getUser();

    return (
        <div
            className="flex -space-x-1 overflow-hidden cursor-pointer"
            onClick={onClick}
            data-cy={"avatar"}
        >
            <div
                className="flex size-10 rounded-full bg-sky-500 dark:bg-sky-700 items-center justify-center text-white"
            >
                {userData?.email
                ? userData.email.slice(0, 2).toUpperCase()
                : "UN"}
            </div>
        </div>
    )
}

export default Avatar;
