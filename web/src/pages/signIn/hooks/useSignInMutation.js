import { useMutation } from "@tanstack/react-query";
import { useDispatch } from "react-redux";
import { addNewNotification } from "../../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_BAD, NOTIFICATION_GOOD } from "../../../const";
import { setUserData } from "../../../setup/store/reducers/userSlice";
import { signIn } from "../api/signIn";

export function useSignInMutation() {
    const dispatch = useDispatch();
    return useMutation({
      mutationFn: async (data) => {
        return await signIn(data);
      },
      onError: (error) => {
        dispatch(
          addNewNotification({
            message: error.response.data?.detail
              ? error.response.data?.detail
              : "Что-то пошло не так",
            type: NOTIFICATION_BAD,
            duration: 5000,
          })
        );
      },
      onSuccess: (data) => {
        dispatch(
          addNewNotification({
            message: `Вы вошли в аккаунт ${data.data.username}`,
            type: NOTIFICATION_GOOD,
            duration: 3000,
          })
        );
  
        const expiresDate = new Date();
        expiresDate.setHours(expiresDate.getHours() + 12);
        document.cookie = `user=${JSON.stringify(
          data.data
        )};expires=${expiresDate.toUTCString()};`;
        dispatch(setUserData(data.data));
      },
    });
  }