import { useMutation } from "@tanstack/react-query";
import { signUp } from "../api/signUp";

export function useSignUpMutation(addNotification) {
  return useMutation({
    mutationFn: async (data) => {
      return await signUp(data);
    },
    onError: (error) => {
      console.log(error);
      addNotification("Что-то пошло не так!", "bad", 3000);
    },
    onSuccess: (data, userData) => {
      console.log(data);
      addNotification(`Аккаунт ${userData.username} создан` , "good", 3000);
    },
  });
}
