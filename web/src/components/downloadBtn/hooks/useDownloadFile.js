import { useMutation } from "@tanstack/react-query";
import { downloadFile } from "../../../api/downloadFile";
import { useDispatch } from "react-redux";
import { addNewNotification } from "../../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_BAD } from "../../../const";

export function useDownloadFile() {
  const dispatch = useDispatch();
  return useMutation({
    mutationFn: async (fileId) => await downloadFile(fileId),
    onError: () => {
      dispatch(
        addNewNotification({
          message: "Не удалось скачать файл",
          type: NOTIFICATION_BAD,
          duration: 5000,
        })
      );
    },
  });
}
