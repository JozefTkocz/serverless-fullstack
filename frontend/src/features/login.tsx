import { Button, TextField } from "@mui/material";
import { useState } from "react";
import { apiClient } from "../api/client";

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
  const [userEmail, setUserEmal] = useState("");
  const handleSubmit = async () => {
    console.log(apiClient.url);
    await apiClient.requestOtp(userEmail);
    setState(LoginState.NeedsPasscode);
  };

  return (
    <>
      <TextField
        id="standard-basic"
        label="Email Address"
        variant="standard"
        onChange={(e) => setUserEmal(e.target.value)}
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
  return <TextField id="standard-basic" label="Standard" variant="standard" />;
}

function Success(_: StateUpdater) {
  console.log("success");
  return <p>Some text</p>;
}

function Failed(_: StateUpdater) {
  console.log("failed");
  return <p>Some text</p>;
}
