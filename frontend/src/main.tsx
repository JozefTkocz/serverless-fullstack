import { StrictMode, useState } from "react";
// import App from "./App";
// import "./index.css";
import ReactDOM from "react-dom/client";
import { RouterProvider, createRouter } from "@tanstack/react-router";
// Import the generated route tree
import { routeTree } from "./routeTree.gen";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import { apiClient } from "./api/client";

type CurrentUser = {
  email: string;
  token: string;
};

type CurrentUserContextType = {
  currentUser: CurrentUser;
  fetchCurrentUser: () => Promise<void>;
};

// Handle the current user using a context
export const CurrentUserContext =
  React.createContext<CurrentUserContextType | null>(null);

export const CurrentUserProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [currentUser, setCurrentUser] = useState<CurrentUser>({
    email: "",
    token: "",
  });

  const fetchCurrentUser = async () => {
    const response = await apiClient.checkLogin();
    console.log(response);
    setCurrentUser({ email: "logged in", token: "good" });
  };

  return (
    <CurrentUserContext.Provider value={{ currentUser, fetchCurrentUser }}>
      {children}
    </CurrentUserContext.Provider>
  );
};

export const useCurrentUser = (): CurrentUserContextType => {
  const context = React.useContext(CurrentUserContext);
  if (!context) {
    throw new Error("useCurrentUser must be used within a CurrentUserProvider");
  }
  return context;
};

// Create a new router instance
const router = createRouter({ routeTree });

// Register the router instance for type safety
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

// Create a client
const queryClient = new QueryClient();

// Render the app
const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <StrictMode>
      <CurrentUserProvider>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
        </QueryClientProvider>
      </CurrentUserProvider>
    </StrictMode>
  );
}
