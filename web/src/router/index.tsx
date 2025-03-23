import { Navigate, Routes, Route, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

import { ActiveUser } from "../instances/user";
import {
  Login,
  Register
} from "../pages";
import React from "react";


function AnimatedPage({ children }: {children: React.ReactNode}) {
    const breathingVariants = {
        initial: {
            scale: 0.9,
            opacity: 0
            },
        animate: {
            scale: [0.9, 1, 0.9],
            opacity: 1,
            transition: {
                duration: 2,
                ease: "easeInOut"
            }
        },
        exit: {
            scale: 0.9,
            opacity: 0,
            transition: { duration: 0.5 }
        }
    };

    return (
        <motion.div
            variants={breathingVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className={"h-screen w-screen flex items-center justify-center"}
        >
            {children}
        </motion.div>
    );
}

const ProtectedRoute: React.FC = () => {
    const location = useLocation();
    const userToken = ActiveUser.getToken();

    if (!userToken) return <Navigate to="/auth/login" state={{ from: location }} replace />;
    return <Navigate to="/" replace />;
};

export default ProtectedRoute;


export function AiChatRoutes() {
    const location = useLocation();

    return (
        <AnimatePresence mode="wait">
            <Routes location={location} key={location.key}>
                <Route path="/auth/login" element={<AnimatedPage><Login /> </AnimatedPage>} />
                <Route path="/auth/register" element={<AnimatedPage><Register /> </AnimatedPage>} />
                <Route element={<ProtectedRoute />}>

                </Route>
            </Routes>
        </AnimatePresence>

    )
}
