import React from "react";
import { Navigate, Routes, Route, useLocation, Outlet } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

import { ActiveUser } from "../instances/user";
import {
    Login,
    Register,
    Home
} from "../pages";
import { PATHS } from "../router/routes";


function AnimatedPage({ children }: {children: React.ReactNode}) {
    const breathingVariants = {
        initial: {
            scale: 0.9,
            opacity: 0
            },
        animate: {
            scale: [0.9, 1, 0.9, 1],
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
            className={"h-full w-full"}
        >
            {children}
        </motion.div>
    );
}

const ProtectedRoute: React.FC = () => {
    const location = useLocation();
    const user = ActiveUser.getUser();

    if (!user && !location.pathname.includes("/auth")) {
        ActiveUser.clear();
        return <Navigate to={PATHS.LOGIN} state={{ from: location }} replace />;
    }

    if (user && location.pathname.includes("/auth")) {
        return <Navigate to={PATHS.HOME} replace />;
    }
    return <Outlet />;
};

export function AiChatRoutes() {
    const location = useLocation();

    const routeConfig = {
        auth: {
            path: "/auth",
            children: {
                login: {
                    path: "login",
                    element: <Login />
                },
                register: {
                    path: "register",
                    element: <Register />
                }
            }
        },
        main: {
            path: "/",
            children: {
                home: {
                    index: true,
                    element: <Home />
                }
            }
        }
    };

    return (
        <AnimatePresence mode="wait">
            <Routes location={location} key={location.key}>
                <Route element={<ProtectedRoute />}>
                    {Object.entries(routeConfig).map(([key, route]) => (
                        <Route key={key} path={route.path}>
                            {route.children && Object.entries(route.children).map(([childKey, child]) => (
                                <Route
                                    key={childKey}
                                    path={child.path}
                                    index={child.index}
                                    element={<AnimatedPage>{child.element}</AnimatedPage>}
                                />
                            ))}
                        </Route>
                    ))}
                </Route>
            </Routes>
        </AnimatePresence>
    );
}