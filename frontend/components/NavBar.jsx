import Image from "next/image";
import Link from "next/link";
import { useSession, signIn, signOut } from "next-auth/react";

const NavBar = () => {
  const { data: session } = useSession();

  return (
    <nav className="flex justify-between px-20 py-10 w-full">
      <div className="flex gap-8 items-center text-sm">
        <Link href={"/"}>
          <Image src={"/logo.svg"} alt="logo" height={30.88} width={120} />
        </Link>
        <Link className="ml-8" href={"/tokenize"}>
          Tokenize
        </Link>
        <Link href={"/detokenize"}>Detokenize</Link>
      </div>
      {session ? (
        <div className="flex gap-2 items-center">
          <p>Welcome, {session.user.name}</p>
          <button
            onClick={() => signOut()}
            className="px-4 py-1 font-semibold text-sm bg-black text-white rounded-full"
          >
            Logout
          </button>
        </div>
      ) : (
        <div>
          <Link href={"/signup"} className="px-4 py-1 text-sm text-white">
            Sign Up
          </Link>
          <button onClick={() => signIn()} className="px-4 py-1 font-semibold text-sm bg-black text-white rounded-full">
            Login
          </button>
        </div>
      )}
    </nav>
  );
};

export default NavBar;
