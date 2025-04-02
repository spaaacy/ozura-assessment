import Image from "next/image";
import Link from "next/link";

const NavBar = () => {
  return (
    <nav className="flex justify-between px-20 py-10">
      <Link href={"/"}>
        <Image src={"/logo.svg"} alt="logo" height={30.88} width={120} />
      </Link>
      <h1 className="text-3xl font-bold">Card Tokenizer</h1>
    </nav>
  );
};

export default NavBar;
