import { Button } from "@mui/material";
import { createLazyFileRoute } from "@tanstack/react-router";
import { apiClient } from "../api/client";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  const onClick = async () => {
    apiClient.checkLogin();
  };
  return (
    <div className="p-2">
      <h3>Tumpr 2.0</h3>
      <Button onClick={onClick}>Check login</Button>
    </div>
  );
}
