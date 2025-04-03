"use client";

import NavBar from "@/components/NavBar";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { Toaster } from "react-hot-toast";

export default function Page() {
  const { data: session } = useSession();

  return (
    <main className="min-h-screen bg-gradient-to-br from-zinc-900 via-[#1F1C27] to-zinc-900 text-white flex flex-col ">
      <NavBar />
      <div className="text-center mt-20">
        <h1 className="text-5xl font-bold mb-6 text-gray-100">Card Tokenizer</h1>
        <p className="text-lg text-gray-300 mb-10">Securely tokenize and detokenize your card information with ease.</p>
        <div className="flex gap-8 justify-center">
          <Link
            href="/tokenize"
            className="relative px-8 py-4 bg-gradient-to-r from-purple-700 to-pink-700 text-white font-semibold rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition-transform duration-300"
          >
            Tokenize
          </Link>
          <Link
            href="/detokenize"
            className="relative px-8 py-4 bg-gradient-to-r from-indigo-700 to-blue-700 text-white font-semibold rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition-transform duration-300"
          >
            Detokenize
          </Link>
        </div>
      </div>
      <Toaster />
    </main>
  );
}
