import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "https://muhib-dev-hackathon-2-phase-2.hf.space",
  // For now, we'll use a simple setup without advanced plugins
});

// Export authentication functions
export const { signIn, signUp, signOut, getSession } = authClient;





// import { createAuthClient } from "better-auth/client";

// export const authClient = createAuthClient({
//   baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
//   // For now, we'll use a simple setup without advanced plugins
// });

// // Export authentication functions
// export const { signIn, signUp, signOut, getSession } = authClient;