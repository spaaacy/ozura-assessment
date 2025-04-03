"use client";

import NavBar from "@/components/NavBar";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import toast, { Toaster } from "react-hot-toast";

const SignUp = () => {
  const { data: session } = useSession();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const router = useRouter();

  useEffect(() => {
    if (session) router.push("/");
  }, [session]);

  const onSubmit = async (data, e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.status === 201) {
        toast.success("Login to continue");
        setTimeout(() => {
          router.push("/api/auth/signin");
        }, 1000);
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
    <main>
      <NavBar />
      <div className="max-w-80 mx-auto">
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-2 mt-10">
          <h2 className="font-medium mx-auto">Create an account</h2>
          <label htmlFor="name" className="text-sm">
            Name
          </label>
          <input
            id="name"
            {...register("name", { required: "Name is required" })}
            type="text"
            className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none"
            aria-invalid={errors.name ? "true" : "false"}
          />
          {errors.name && (
            <p role="alert" className="text-xs text-red-500">
              {errors.name?.message}
            </p>
          )}
          <label htmlFor="email" className="text-sm">
            Email
          </label>
          <input
            id="email"
            {...register("email", { required: "Email is required" })}
            type="text"
            className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none"
            aria-invalid={errors.email ? "true" : "false"}
          />

          {errors.email && (
            <p role="alert" className="text-xs text-red-500">
              {errors.email?.message}
            </p>
          )}
          <label htmlFor="password" className="text-sm">
            Password
          </label>
          <input
            id="password"
            {...register("password", { required: "Password is required" })}
            type="password"
            className="p-2 text-sm border border-gray-400 rounded focus:ring-0 focus:outline-none"
            aria-invalid={errors.password ? "true" : "false"}
          />
          {errors.password && (
            <p role="alert" className="text-xs text-red-500">
              {errors.password?.message}
            </p>
          )}
          <button type="submit" className="text-gray-200 text-sm rounded bg-black py-2 hover:text-gray-200 mt-2">
            Sign up
          </button>
        </form>
      </div>
      <Toaster />
    </main>
  );
};

export default SignUp;
