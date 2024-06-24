import { useMutation } from "@tanstack/react-query";
import { useDispatch } from "react-redux";
import { NOTIFICATION_BAD, NOTIFICATION_GOOD } from "../../../const";
import { addNewNotification } from "../../../setup/store/reducers/notificationSlice";
import { signUp } from "../api/signUp";


export function useSignUpMutation() {
  const dispatch = useDispatch();
  return useMutation({
    mutationFn: async (data) => {
      return await signUp(data);
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
    onSuccess: (data, userData) => {
      dispatch(
        addNewNotification({
          message: `Аккаунт ${userData.username} создан`,
          type: NOTIFICATION_GOOD,
          duration: 3000,
        })
      );
    },
  });
}
