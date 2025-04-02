import { useState } from "react";
import Cards from "react-credit-cards-2";
import "react-credit-cards-2/dist/es/styles-compiled.css";

const CardInput = () => {
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

  const onSubmit = () => {};

  return (
    <div className="flex flex-col max-w-90 mx-auto gap-4">
      <Cards number={state.number} expiry={state.expiry} cvv={state.cvv} name={state.name} focused={state.focus} />
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
    </div>
  );
};

export default CardInput;
