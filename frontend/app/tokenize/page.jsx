"use client";

import NavBar from "@/components/NavBar";
import { useSession } from "next-auth/react";
import { useState } from "react";
import Cards from "react-credit-cards-2";
import "react-credit-cards-2/dist/es/styles-compiled.css";
import toast, { Toaster } from "react-hot-toast";
import { FaClipboard } from "react-icons/fa";

const Tokenize = () => {
  const { data: session } = useSession();
  const [token, setToken] = useState();

  const [state, setState] = useState({
    number: "",
    expiry: "",
    cvv: "",
    name: "",
    focus: "",
  });

  const handleInputChange = (evt) => {
    const { name, value } = evt.target;

    setState((prev) => ({ ...prev, [name]: value }));
  };

  const handleInputFocus = (evt) => {
    setState((prev) => ({ ...prev, focus: evt.target.name }));
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(token);
    toast.success("Token copied to clipboard!");
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!session) return;
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/tokenize`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session?.accessToken}`,
        },
        body: JSON.stringify({
          card_number: state.number,
          name: state.name,
          cvv: state.cvv,
          expiry: state.expiry,
        }),
      });
      if (response.status === 201) {
        const { token } = await response.json();
        setToken(token);
        toast.success("Card tokenized successfully!");
        setState({ number: "", expiry: "", cvv: "", name: "", focus: "" });
      } else {
        const { error } = await response.json();
        throw error;
      }
    } catch (error) {
      console.error(error);
      toast.error("Oops, something went wrong");
    }
  };

  return (
    <main className="flex flex-col items-center">
      <NavBar />
      {session ? (
        <div className="flex flex-col max-w-90 mx-auto gap-4">
          {token ? (
            <div className="flex flex-col items-center justify-center gap-2 text-white bg-gradient-to-r from-emerald-500 to-emerald-900 rounded py-4 px-8 font-light text-sm text-center">
              <h5 className="font-semibold text-base">Your token is</h5>
              <div className="flex gap-4">
                <p>{token}</p>
                <button
                  onClick={copyToClipboard}
                  className="text-white hover:text-gray-300 focus:outline-none"
                  aria-label="Copy token to clipboard"
                >
                  <FaClipboard />
                </button>
              </div>
            </div>
          ) : (
            <>
              <Cards
                number={state.number}
                expiry={state.expiry}
                cvv={state.cvv}
                name={state.name}
                focused={state.focus}
              />
              <form className="flex flex-col gap-4" onSubmit={onSubmit}>
                <input
                  type="text"
                  name="number"
                  className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none bg-white text-black"
                  placeholder="Card Number"
                  value={state.number}
                  maxLength={16}
                  onChange={handleInputChange}
                  onFocus={handleInputFocus}
                />
                <input
                  type="text"
                  name="name"
                  placeholder="Your Name"
                  className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none bg-white text-black"
                  value={state.name}
                  maxLength={20}
                  onChange={handleInputChange}
                  onFocus={handleInputFocus}
                />
                <input
                  type="text"
                  name="expiry"
                  placeholder="Expiry"
                  className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none bg-white text-black"
                  value={state.expiry}
                  maxLength={4}
                  onChange={handleInputChange}
                  onFocus={handleInputFocus}
                />
                <input
                  type="text"
                  name="cvv"
                  placeholder="CVV"
                  className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none bg-white text-black"
                  value={state.cvv}
                  maxLength={3}
                  onChange={handleInputChange}
                  onFocus={handleInputFocus}
                />
                <button type="submit" className="text-gray-200 text-sm rounded bg-black py-2 hover:text-gray-200">
                  Tokenize
                </button>
              </form>
            </>
          )}
        </div>
      ) : (
        <h1 className=" text-xl">Login to get started</h1>
      )}
      <Toaster />
    </main>
  );
};

export default Tokenize;
