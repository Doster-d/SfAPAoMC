import { useMutation } from "@tanstack/react-query";
import { signIn } from "../api/signIn";
import { useDispatch } from "react-redux";
import { setUserData } from "../../../../../setup/store/reducers/userSlice";

export function useSignInMutation(addNotification) {
    const dispatch = useDispatch()
  return useMutation({
    mutationFn: async (data) => {
      return await signIn(data);
    },
    onError: (error) => {
      console.log(error);
      addNotification(error.response.data?.detail ? error.response.data?.detail : 'Что-то пошло не так', "bad", 3000);
    },
    onSuccess: (data) => {
        console.log(data.data);
        addNotification(`Вы вошли в аккаунт ${data.data.username}`, 'good', 3000)
        const expiresDate = new Date();
        expiresDate.setHours(expiresDate.getHours() + 12)
        document.cookie = `user=${JSON.stringify(data.data)};expires=${expiresDate.toUTCString()};`
        console.log(document.cookie);
        dispatch(setUserData(data.data))
    }
  });
}
