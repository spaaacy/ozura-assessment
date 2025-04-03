"use client";

import NavBar from "@/components/NavBar";
import { useSession } from "next-auth/react";
import { useState } from "react";
import "react-credit-cards-2/dist/es/styles-compiled.css";
import toast from "react-hot-toast";
import Cards from "react-credit-cards-2";

const Tokenize = () => {
  const { data: session } = useSession();
  const [token, setToken] = useState("");
  const [cardDetails, setCardDetails] = useState();

  const onSubmit = async (e) => {
    if (!session) return;
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/detokenize`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session?.accessToken}`,
        },
        body: JSON.stringify({
          token,
        }),
      });
      if (response.status === 200) {
        const { card_details } = await response.json();
        setCardDetails(card_details);
        toast.success("Card detokenized successfully!");
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
        cardDetails ? (
          <Cards
            number={cardDetails.card_number}
            expiry={cardDetails.expiry_date}
            cvv={cardDetails.cvv}
            name={cardDetails.name}
          />
        ) : (
          <div className="flex flex-col items-center w-90 mx-auto gap-4 bg-gradient-to-r from-emerald-500 to-emerald-900 rounded py-4 px-8">
            <label htmlFor="token" className="text-semibold">
              Detokenize
            </label>
            <input
              type="text"
              id="token"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Enter token"
              className="p-2 text-sm w-full rounded focus:ring-0 focus:outline-none bg-gray-50/20"
            />
            <button
              type="button"
              onClick={() => onSubmit()}
              className="text-gray-200 text-sm rounded bg-black py-2 hover:text-gray-200 w-full"
            >
              Detokenize
            </button>
          </div>
        )
      ) : (
        <h1 className=" text-xl">Login to get started</h1>
      )}
    </main>
  );
};

export default Tokenize;
