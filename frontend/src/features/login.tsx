import { TextField } from "@mui/material";
import { useState } from "react";
import { apiClient } from "../api/client";
import { Typography } from "@mui/material";
import { DebouncedButton } from "../components/DebouncedButton";
import { Link } from "@tanstack/react-router";

enum LoginState {
  NeedsEmail,
  NeedsPasscode,
  NeedsAuth,
  Success,
  Failed,
}

export const AUTH_TOKEN_KEY = "auth_token";

type StateUpdater<T> = (state: T) => void;

export function LoginFlow() {
  const [state, setState] = useState(LoginState.NeedsEmail);
  const [userEmail, setUserEmail] = useState("");

  return (
    <Login
      state={state}
      setState={setState}
      userEmail={userEmail}
      setUserEmail={setUserEmail}
    />
  );
}

function Login({
  state,
  setState,
  userEmail,
  setUserEmail,
}: {
  state: LoginState;
  setState: StateUpdater<LoginState>;
  userEmail: string;
  setUserEmail: StateUpdater<string>;
}) {
  let component = <></>;
  switch (state) {
    case LoginState.NeedsEmail: {
      component = (
        <EmailInput setState={setState} setUserEmail={setUserEmail} />
      );
      break;
    }
    case LoginState.NeedsPasscode: {
      component = <RequestPasscode userEmail={userEmail} setState={setState} />;
      break;
    }
    case LoginState.NeedsAuth: {
      component = <EnterPasscode email={userEmail} setState={setState} />;
      break;
    }
    case LoginState.Success: {
      component = Success(setState);
      break;
    }
    case LoginState.Failed: {
      component = Failed(setState);
      break;
    }
  }
  return component;
}

function EmailInput({
  setState,
  setUserEmail,
}: {
  setState: StateUpdater<LoginState>;
  setUserEmail: StateUpdater<string>;
}) {
  const [inputText, setInputText] = useState("");
  const handleSubmit = async () => {
    await apiClient.registerUser(inputText);
    setUserEmail(inputText);
    setState(LoginState.NeedsPasscode);
  };

  return (
    <>
      <Typography variant="body1" gutterBottom>
        Enter your email address to request a passcode
      </Typography>
      <TextField
        id="standard-basic"
        label="Email Address"
        variant="standard"
        onChange={(e) => setInputText(e.target.value)}
      />
      <DebouncedButton variant="contained" onClick={() => handleSubmit()}>
        Request Password
      </DebouncedButton>
    </>
  );
}

function RequestPasscode({
  userEmail,
  setState,
}: {
  userEmail: string;
  setState: StateUpdater<LoginState>;
}) {
  const requestOtp = async () => {
    await apiClient.requestOtp(userEmail);
    setState(LoginState.NeedsAuth);
  };
  return (
    <>
      <Typography>
        If you havent already done so, you will need to accept the email
        subscription request from AWS SNS
      </Typography>
      <DebouncedButton variant="contained" onClick={requestOtp}>
        Get Login Code
      </DebouncedButton>
    </>
  );
}

function EnterPasscode({
  email,
  setState,
}: {
  email: string;
  setState: StateUpdater<LoginState>;
}) {
  const [passCode, setPassCode] = useState("");
  const sendLogin = async () => {
    const loginResponse = await apiClient.login(email, passCode);
    if (loginResponse.auth_token) {
      window.localStorage.setItem(AUTH_TOKEN_KEY, loginResponse.auth_token);
      setState(LoginState.Success);
    } else {
      setState(LoginState.Failed);
    }
  };
  return (
    <>
      <TextField
        id="standard-basic"
        label="Passcode"
        variant="standard"
        onChange={(e) => setPassCode(e.target.value)}
      />
      <DebouncedButton variant="contained" onClick={sendLogin}>
        Login
      </DebouncedButton>
    </>
  );
}

function Success(_: StateUpdater<LoginState>) {
  const pageContent = (
    <>
      <p>You are now logged in</p>
      <Link href="/">Return Home</Link>
    </>
  );
  return pageContent;
}

function Failed(_: StateUpdater<LoginState>) {
  return (
    <>
      <p>Login Failed!</p>
    </>
  );
}
