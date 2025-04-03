"use client";

import { SessionProvider } from "next-auth/react";
import React from "react";

const ContextWrapper = ({children}) => {
  return (
    <SessionProvider>
        {children}
    </SessionProvider>
  );
};

export default ContextWrapper;
