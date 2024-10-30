import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
// import ".././App.css";
import { Box } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../api/client";

export const Route = createRootRoute({
  component: () => {
    const { isPending } = useQuery({
      queryKey: ["health"],
      queryFn: apiClient.healthCheck,
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
          {isPending && "Loading"}
        </Box>
        <Outlet />
        <TanStackRouterDevtools />
      </>
    );
  },
});
