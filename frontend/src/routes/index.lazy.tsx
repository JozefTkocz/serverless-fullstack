import { Button } from "@mui/material";
import { createLazyFileRoute } from "@tanstack/react-router";
import { apiClient } from "../api/client";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  console.log("cookies");
  console.log(document.cookie);
  const onClick = async () => {
    apiClient.check();
  };
  return (
    <div className="p-2">
      <h3>Tumpr 2.0</h3>
      <Button onClick={onClick}>Check the thing</Button>
    </div>
  );
}
