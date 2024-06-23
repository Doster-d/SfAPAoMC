import { useMutation } from "@tanstack/react-query";
import { uploadFile } from "../api/uploadFile";
import { useSelector, useDispatch } from "react-redux";
import { downloadFile } from "../api/downloadFile";
import { useNavigate } from "react-router-dom";
import { addNewNotification } from "../../../../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_BAD, NOTIFICATION_GOOD } from "../../../../../const";

export function useUploadFileMutation() {
  const dispatch = useDispatch();
  const { userId, accessToken } = useSelector((state) => state.user);
  const navigate = useNavigate();
  return useMutation({
    mutationFn: async (data) => await uploadFile(data, accessToken, userId),
    onError: (error) => {
      console.log(error);
      dispatch(
        addNewNotification({
          message: error.response?.data?.detail
            ? error.response.data.detail
            : "Что-то пошло не так...",
          type: NOTIFICATION_BAD,
          duration: 5000,
        })
      );
    },
    onSuccess: async (data) => {
      dispatch(
        addNewNotification({
          message: `Файл ${data.data.filename} обработан`,
          type: NOTIFICATION_GOOD,
          duration: 3000,
        })
      );
      const response = await downloadFile(data.data.fileId);
      navigate(`/file/${data.data.fileId}`);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `Обработанный_${data.data.filename}`; // Замените на нужное имя файла и расширение
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      console.log(data);
    },
  });
}
