'use client'

import { useForm } from "react-hook-form";

const SignUp = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = () => {};
  
  
  return (
    <div className="max-w-80 mx-auto">
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-2 mt-10">
        <h2 className="font-medium mx-auto">Create an account</h2>
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
  );
};

export default SignUp;
