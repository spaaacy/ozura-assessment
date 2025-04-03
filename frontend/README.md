# Tokenization Service

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

This project requires the following environment variables to be set in a `.env` file at the root of the project:

```properties
NEXT_PUBLIC_BACKEND_URL=http://localhost:8080
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=324bd8c227e8074689c2b8f224d7fb10c47aa4e77590274cad048fa01f908456
```

- `NEXT_PUBLIC_BACKEND_URL`: The base URL for the backend API.
- `NEXTAUTH_URL`: The URL of the Next.js application.
- `NEXTAUTH_SECRET`: A secret key used for NextAuth authentication.
