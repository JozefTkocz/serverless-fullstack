import { TextField } from "@mui/material";
import { useState } from "react";
import { apiClient } from "../api/client";
import { Typography } from "@mui/material";
import { DebouncedButton } from "../components/DebouncedButton";
// import { useQuery } from "@tanstack/react-query";

enum LoginState {
  NeedsEmail,
  NeedsPasscode,
  NeedsAuth,
  Success,
  Failed,
}

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
      component = <RequestPasscode setState={setState} />;
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
        Enter some stuff in here.
      </Typography>
      <TextField
        id="standard-basic"
        label="Email Address"
        variant="standard"
        onChange={(e) => setInputText(e.target.value)}
      />
      <DebouncedButton variant="contained" onClick={() => handleSubmit()}>
        Click me!
      </DebouncedButton>
    </>
  );
}

function RequestPasscode({ setState }: { setState: StateUpdater<LoginState> }) {
  const requestOtp = async () => {
    await apiClient.requestOtp("jozeftkocz@gmail.com");
    setState(LoginState.NeedsAuth);
  };
  return (
    <DebouncedButton variant="contained" onClick={requestOtp}>
      Get Login Code
    </DebouncedButton>
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
    const loggedIn: boolean = await apiClient.login(email, passCode);
    console.log(loggedIn);
    if (loggedIn) {
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
  console.log("success");
  return <p>Success</p>;
}

function Failed(_: StateUpdater<LoginState>) {
  console.log("failed");
  return <p>Failure</p>;
}
