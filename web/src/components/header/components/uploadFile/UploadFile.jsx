import { useState } from "react";
import "./style.scss";
import { useForm } from "react-hook-form";
import { useUploadFileMutation } from "./hooks/useUploadFileMutation";
import { useNavigate } from "react-router-dom";
function UploadFile({addNotification}) {
  const [drop, setDrop] = useState(false);
  const [fileName, setFileName] = useState(undefined)
  const uploadFileMutation = useUploadFileMutation(addNotification)
  const navigate = useNavigate()
  const handleFile = async (file) => {
    console.log(file);
    if(file.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        addNotification("Не правильный тип файла", 'bad', 5000)
        return;
    }
    addNotification("Файл добавлен", 'good', 5000)
    setFileName(file.name)
    const response = await uploadFileMutation.mutateAsync(file)
    addNotification("Данные обрабатываются. Пожалуйста подождите, это может занять продолжительное время.", 'good', 5000)
    await addNotification('Данные обработаны', 'good', 3000)
    console.log('Response:', response);
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
    handleFile(e.target.files[0])
  }
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
            <span className="upload-form__span">{fileName ? uploadFileMutation.isPending ? 'Обработка...' : 'Файл загружен' : 'Загузить файлы'}</span>
            <input
              id="upload-input"
              className="upload-form__input"
              type="file"
              onChange={handleFileChange}
              disabled={uploadFileMutation.isPending}
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            />
            <span className="upload-form__add-span">{fileName ? fileName : 'Формат .xlxs'}</span>
          </>
        )}
      </label>
    </form>
  );
}

export default UploadFile;
