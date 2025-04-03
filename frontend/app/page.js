'use client'

import Home from "@/components/Home";
import { SessionProvider } from "next-auth/react";
import React from "react";

const Page = () => {
  return (
    <SessionProvider>
      <Home />
    </SessionProvider>
  );
};

export default Page;
