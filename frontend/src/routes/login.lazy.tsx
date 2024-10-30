import { createLazyFileRoute } from "@tanstack/react-router";
import { LoginFlow } from "../features/login";

export const Route = createLazyFileRoute("/login")({
  component: Login,
});

function Login() {
  return LoginFlow();
}
