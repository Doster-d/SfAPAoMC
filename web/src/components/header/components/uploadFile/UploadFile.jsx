import { useState } from "react";
import "./style.scss";
import { useForm } from "react-hook-form";
import { useUploadFileMutation } from "./hooks/useUploadFileMutation";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { addNewNotification } from "../../../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_BAD, NOTIFICATION_GOOD } from "../../../../const";
function UploadFile({ toggleDownloadOpen }) {
  const [drop, setDrop] = useState(false);
  const dispatch = useDispatch();
  const [fileName, setFileName] = useState(undefined);
  const uploadFileMutation = useUploadFileMutation();
  const handleFile = async (file) => {
    console.log(file);
    if (
      file.type !==
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ) {
      dispatch(
        addNewNotification({
          message: "Не правильный тип файла",
          type: NOTIFICATION_BAD,
          duration: 5000,
        })
      );
      return;
    }
    dispatch(
      addNewNotification({
        message: "Файл добавлен",
        type: NOTIFICATION_GOOD,
        duration: 5000,
      })
    );
    setFileName(file.name);
    dispatch(
      addNewNotification({
        message:
          "Данные обрабатываются. Пожалуйста подождите, это может занять продолжительное время.",
        type: NOTIFICATION_GOOD,
        duration: 5000,
      })
    );

    const response = await uploadFileMutation.mutateAsync(file);
    toggleDownloadOpen();
    console.log("Response:", response);
  };
  const onDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDrop(false);
  };

  const onDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDrop(true);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setDrop(false);

    handleFile(droppedFile);
  };
  const handleFileChange = (e) => {
    e.preventDefault();
    setDrop(false);

    console.log(e);
    handleFile(e.target.files[0]);
  };
  return (
    <form
      className="upload-form"
      onDrop={handleDrop}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
    >
      <label
        htmlFor="upload-input"
        className={
          drop
            ? "upload-form__label upload-form__label--dropping"
            : "upload-form__label"
        }
      >
        {!drop && (
          <>
            <span className="upload-form__span">
              {fileName
                ? uploadFileMutation.isPending
                  ? "Обработка..."
                  : "Файл загружен"
                : "Загузить файлы"}
            </span>
            <input
              id="upload-input"
              className="upload-form__input"
              type="file"
              onChange={handleFileChange}
              disabled={uploadFileMutation.isPending}
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            />
            <span className="upload-form__add-span">
              {fileName ? fileName : "Формат .xlxs"}
            </span>
          </>
        )}
      </label>
    </form>
  );
}

export default UploadFile;
