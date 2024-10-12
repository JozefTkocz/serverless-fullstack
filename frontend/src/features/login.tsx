import { Button, TextField } from "@mui/material";
import { useState } from "react";
import { apiClient } from "../api/client";
import { Typography } from "@mui/material";

enum LoginState {
  NeedsEmail,
  NeedsPasscode,
  Success,
  Failed,
}

type StateUpdater<T> = (state: T) => void;

export function LoginFlow() {
  const [state, setState] = useState(LoginState.NeedsEmail);

  return <Login state={state} setState={setState} />;
}

function Login({
  state,
  setState,
}: {
  state: LoginState;
  setState: StateUpdater<LoginState>;
}) {
  let component = <></>;
  switch (state) {
    case LoginState.NeedsEmail: {
      component = <EmailInput setState={setState} />;
      break;
    }
    case LoginState.NeedsPasscode: {
      component = <OneTimeCodeEntry _setState={setState} />;
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

function EmailInput({ setState }: { setState: StateUpdater<LoginState> }) {
  const [userEmail, setUserEmail] = useState("");
  const handleSubmit = async () => {
    await apiClient.registerUser(userEmail);
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
        onChange={(e) => setUserEmail(e.target.value)}
      />
      <Button variant="contained" onClick={() => handleSubmit()}>
        Get Login Code
      </Button>
    </>
  );
}

function OneTimeCodeEntry({
  _setState,
}: {
  _setState: StateUpdater<LoginState>;
}) {
  console.log("one time code");
  const requestOtp = async () => {
    await apiClient.requestOtp("jozeftkocz@gmail.com");
  };
  return (
    <Button variant="contained" onClick={requestOtp}>
      Get Login Code
    </Button>
  );
}

function Success(_: StateUpdater<LoginState>) {
  console.log("success");
  return <p>Some text</p>;
}

function Failed(_: StateUpdater<LoginState>) {
  console.log("failed");
  return <p>Some text</p>;
}
