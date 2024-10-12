import { Button, ButtonProps, CircularProgress } from "@mui/material";
import React, { ReactNode, useState } from "react";

export function DebouncedButton({
  children,
  ...props
}: ButtonProps & { children: ReactNode }) {
  const [isLoading, setIsLoading] = useState(false);

  const { onClick } = props;
  const handleClick = async (
    event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
  ) => {
    setIsLoading(true);
    if (onClick) {
      await onClick(event);
    }
    setIsLoading(false);
  };

  return (
    <>
      {!isLoading ? (
        <Button {...{ ...props, onClick: handleClick }}>{children}</Button>
      ) : (
        <CircularProgress />
      )}
    </>
  );
}
