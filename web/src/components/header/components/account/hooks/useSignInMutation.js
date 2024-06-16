import { useMutation } from "@tanstack/react-query";
import { signIn } from "../api/signIn";

export function useSignInMutation() {
  return useMutation({
    mutationFn: async (data) => {
      return await signIn(data);
    },
    onError: (error) => {
      console.log(error);
    },
    onSuccess: (data) => {
        console.log(data);
    }
  });
}
