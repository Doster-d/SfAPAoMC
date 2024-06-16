import { useMutation } from "@tanstack/react-query";
import { signUp } from "../api/signUp";

export function useSignUpMutation() {
    return useMutation({
      mutationFn: async (data) => {
        return await signUp(data);
      },
      onError: (error) => {
        console.log(error);
      },
      onSuccess: (data) => {
          console.log(data);
      }
    });
  }
  