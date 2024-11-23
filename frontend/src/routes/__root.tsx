import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
// import ".././App.css";
import { Box } from "@mui/material";
import { createContext } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiClient, AUTH_TOKEN_KEY } from "../api/client";

export type CurrentUser = {
  email: string;
  isLoggedIn: boolean;
};

export const CurrentUserContext = createContext<CurrentUser | undefined>({
  email: "",
  isLoggedIn: false,
});

export const Route = createRootRoute({
  component: () => {
    const { data: currentUser } = useQuery({
      queryKey: [window.localStorage.getItem(AUTH_TOKEN_KEY)],
      queryFn: () => apiClient.checkLogin(),
    });

    return (
      <>
        <Box
          sx={{
            display: "flex",
            direction: "row",
            justifyContent: "space-between",
            width: "100%", // Add this line to make it take full width
          }}
        >
          <Link to="/" className="[&.active]:font-bold">
            Home
          </Link>{" "}
          <Link to="/login" className="[&.active]:font-bold">
            Login
          </Link>
        </Box>

        <CurrentUserContext.Provider value={currentUser}>
          <Outlet />
        </CurrentUserContext.Provider>

        <TanStackRouterDevtools />
      </>
    );
  },
});
