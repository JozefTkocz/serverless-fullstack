import { Button, Typography } from "@mui/material";
import { createLazyFileRoute } from "@tanstack/react-router";
import { apiClient } from "../api/client";
import { useContext } from "react";
import { CurrentUserContext } from "./__root";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  const onClick = async () => {
    apiClient.checkLogin();
  };

  const user = useContext(CurrentUserContext);
  console.log("///");
  console.log(user);
  return (
    <div className="p-2">
      {user && <Typography>Hello {user.email}</Typography>}
      <Button onClick={onClick}>Check login</Button>
    </div>
  );
}
