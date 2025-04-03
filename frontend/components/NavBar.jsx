import Image from "next/image";
import Link from "next/link";
import { useSession, signIn, signOut } from "next-auth/react";

const NavBar = () => {
  const { data: session } = useSession();
  
  return (
    <nav className="flex justify-between px-20 py-10">
      <Link href={"/"}>
        <Image src={"/logo.svg"} alt="logo" height={30.88} width={120} />
      </Link>
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
        <button onClick={() => signIn()} className="px-4 py-1 font-semibold text-sm bg-black text-white rounded-full">
          Login
        </button>
      )}
    </nav>
  );
};

export default NavBar;
