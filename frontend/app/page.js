"use client";

import CardInput from "@/components/CardInput";
import NavBar from "@/components/NavBar";
import SignIn from "@/components/SignIn";
import SignUp from "@/components/SignUp";


export default function Home() {

  return (
    <main>
      <NavBar />
      {/* <CardInput/> */}
      {/* <SignIn/> */}
      <SignUp/>
    </main>
  );
}
